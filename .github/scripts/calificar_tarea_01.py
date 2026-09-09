"""Califica la entrega de la Tarea 01 de un PR y registra el resultado.

Corre desde .github/workflows/calificar_tarea_01.yml, disparado por un comentario
en un PR. Dos comandos:

    /validar    revisa que la entrega tenga la forma correcta. NO califica, no toca
                la hoja y NO consume intento. Se puede usar cuantas veces se quiera.
    /calificar  califica y registra. Consume uno de los tres intentos.

SEGURIDAD — las tres reglas que hacen esto seguro en un repo público:

1. El disparador es `issue_comment`, así que el workflow que corre es el de `main`,
   no el de la rama del alumno. Nadie puede editar el YAML en su PR para robar el
   secret.
2. NUNCA se hace checkout ni se ejecuta el código del PR. Solo se baja UN archivo
   (`predicciones.csv`) y se parsea como datos.
3. Nada de lo que se imprime incluye valores de `y_test`. Los logs de un repo
   público son públicos.

Calificación:
    mse_ref  = MSE de la regresión lineal con las 12 variables crudas (la da el oráculo)
    mse_meta = 1.10 * MSE del modelo verdadero
    calif    = clip(5 + 5 * (mse_ref - mse_alumno) / (mse_ref - mse_meta), 5, 10)

Intentos: 3 por variante. Un CSV con formato inválido NO consume intento, y
tampoco lo consume un comentario fuera de la ventana de entregas.
"""

import base64
import csv
import io
import json
import math
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

import gspread

REPO = os.environ["REPO"]
PR = os.environ["PR_NUMERO"]
COMENTARISTA = os.environ["COMENTARISTA"]
COMENTARIO = os.environ.get("COMENTARIO", "/calificar")
PROFESOR_GH = "nasaul"
LIMITE_INTENTOS = 3

# Ventana de entregas, en variables del repo para poder extender el plazo sin commit:
#   TAREA_01_APERTURA  ISO local, opcional. Vacía = abierta desde siempre.
#   TAREA_01_CIERRE    ISO local, requerida. Ausente o ilegible = CERRADA (fail-safe:
#                      más vale que nadie entregue que calificar fuera de plazo).
# Las dos se interpretan en hora de Ciudad de México, no en UTC del runner.
# El profesor está exento de la ventana para poder probar el pipeline.
ZONA = ZoneInfo("America/Mexico_City")
N_TEST = 400
PATRON = re.compile(r"^entregas/tarea-01/(v[0-9a-f]{8})/predicciones\.csv$")


DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def momento(nombre):
    """Lee una variable de fecha del repo. Devuelve None si está vacía o mal escrita."""
    crudo = os.environ.get(nombre, "").strip()
    if not crudo:
        return None
    try:
        return datetime.fromisoformat(crudo).replace(tzinfo=ZONA)
    except ValueError:
        print(f"AVISO: {nombre}={crudo!r} no es una fecha ISO válida y se ignora")
        return None


def en_español(f):
    hora = f.strftime("%I:%M %p").lstrip("0").replace("AM", "am").replace("PM", "pm")
    return f"{DIAS[f.weekday()]} {f.day} de {MESES[f.month - 1]} a las {hora}"


def revisa_ventana():
    """Cierra la puerta fuera de la ventana de entregas. Devuelve el texto del cierre."""
    apertura, cierre = momento("TAREA_01_APERTURA"), momento("TAREA_01_CIERRE")
    ahora = datetime.now(ZONA)

    if cierre is None:
        termina("Las entregas de la Tarea 01 están cerradas (no hay fecha límite "
                "configurada). Este comentario no consumió ningún intento.")
    if apertura and ahora < apertura:
        termina(f"La Tarea 01 abre el {en_español(apertura)}. "
                "Este comentario no consumió ningún intento.")
    if ahora > cierre:
        termina(f"El plazo de la Tarea 01 cerró el {en_español(cierre)} "
                f"(hora de Ciudad de México) y ya no se aceptan entregas. "
                "Este comentario no consumió ningún intento.")
    return en_español(cierre)


def gh(*args, entrada=None):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, input=entrada)
    if r.returncode:
        sys.exit(f"fallo `gh {' '.join(args)}`: {r.stderr.strip()}")
    return r.stdout


def comenta(texto):
    gh("api", f"repos/{REPO}/issues/{PR}/comments", "-f", f"body={texto}")


def termina(texto, codigo=0):
    """Comenta y termina. Sin registrar nada: no consume intento."""
    comenta(texto)
    print(texto.replace("\n", " ")[:300])
    sys.exit(codigo)


def datos_del_pr():
    pr = json.loads(gh("api", f"repos/{REPO}/pulls/{PR}"))
    return pr["user"]["login"], pr["head"]["sha"]


def archivo_de_entrega(head_sha):
    """La única fuente de la variante es la RUTA del archivo, no texto libre del PR."""
    nombres = json.loads(gh("api", f"repos/{REPO}/pulls/{PR}/files", "--paginate"))
    encontrados = [(m.group(1), m.group(0)) for f in nombres
                   if (m := PATRON.match(f["filename"]))]
    if not encontrados:
        termina("No encontré tu entrega.\n\nEl archivo debe estar exactamente en "
                "`entregas/tarea-01/<tu-id-de-variante>/predicciones.csv` "
                "(el id empieza con `v` y lo calcula tu notebook a partir de tu clave única).")
    if len({v for v, _ in encontrados}) > 1:
        termina(f"Tu PR toca {len(encontrados)} variantes distintas. Entrega solo la tuya.")
    return encontrados[0]


def baja_predicciones(ruta, head_sha):
    r = json.loads(gh("api", f"repos/{REPO}/contents/{ruta}?ref={head_sha}"))
    return base64.b64decode(r["content"]).decode("utf-8", errors="replace")


def parsea(texto):
    """Devuelve 400 floats o termina explicando el problema. No consume intento."""
    filas = [f for f in csv.reader(io.StringIO(texto)) if f and any(c.strip() for c in f)]
    if not filas:
        termina("Tu `predicciones.csv` está vacío.")
    if len(filas[0]) != 1:
        termina(f"Tu `predicciones.csv` tiene {len(filas[0])} columnas y debe tener exactamente 1 "
                "(solo la predicción, un renglón por fila de `test.csv`, en el mismo orden).")

    valores, encabezado = [], None
    for i, fila in enumerate(filas):
        try:
            valores.append(float(fila[0]))
        except ValueError:
            if i == 0:
                encabezado = fila[0]
                continue
            termina(f"El renglón {i + 1} de tu `predicciones.csv` no es un número: `{fila[0][:40]}`")

    if len(valores) != N_TEST:
        termina(f"Tu `predicciones.csv` trae {len(valores)} predicciones y deben ser "
                f"exactamente {N_TEST}, en el mismo orden que los renglones de `test.csv`."
                + (f"\n\n(Detecté `{encabezado}` como encabezado y no lo conté.)" if encabezado else ""))
    if malos := [i for i, v in enumerate(valores) if not math.isfinite(v)]:
        n, renglon = len(malos), malos[0] + 1 + bool(encabezado)
        cuenta = f"{n} predicciones que son" if n > 1 else "1 predicción que es"
        termina(f"Tienes {cuenta} NaN o infinito (la primera en el renglón {renglon}).")
    return valores


def califica(mse, mse_ref, mse_meta):
    """5 al igualar el baseline lineal crudo, 10 al llegar al modelo bien especificado.

    Piso en 5: entregar algo que corre garantiza 5. Techo en 10: `mse_meta` trae un
    10% de holgura sobre el oráculo para que el 10 no dependa de la suerte del ruido.
    """
    bruta = 5 + 5 * (mse_ref - mse) / (mse_ref - mse_meta)
    return round(min(10.0, max(5.0, bruta)), 1)


def hojas():
    cred = json.loads(os.environ["GSHEETS_SA_JSON"])
    gc = gspread.service_account_from_dict(cred)
    return (gc.open_by_key(os.environ["GSHEETS_ORACULO_ID"]),
            gc.open_by_key(os.environ["GSHEETS_CALIF_ID"]))


def columna_de(oraculo, variante):
    """Índice de la variante en el oráculo. Lee SOLO el renglón 1: nunca las respuestas."""
    encabezados = oraculo.worksheet("y_test").row_values(1)
    if variante not in encabezados:
        termina(f"La variante `{variante}` no existe. Revisa que tu clave única esté bien "
                "escrita en el notebook: el id de la carpeta se calcula a partir de ella.")
    return encabezados.index(variante) + 1


def y_test_de(oraculo, columna):
    col = oraculo.worksheet("y_test").col_values(columna)[1:]
    return [float(v) for v in col if v != ""]


def referencias_de(oraculo, variante):
    for fila in oraculo.worksheet("referencias").get_all_records():
        if str(fila["hash8"]) == variante:
            return float(fila["mse_ref"]), float(fila["mse_meta"])
    sys.exit(f"la variante {variante} no está en la hoja de referencias")


def main():
    modo = "validar" if COMENTARIO.strip().startswith("/validar") else "calificar"

    autor_pr, head_sha = datos_del_pr()
    if COMENTARISTA not in (autor_pr, PROFESOR_GH):
        termina(f"@{COMENTARISTA}: solo @{autor_pr} (autor del PR) puede usar `/{modo}`.")

    es_profesor = COMENTARISTA == PROFESOR_GH
    limite_txt = "sin plazo (profesor)" if es_profesor else revisa_ventana()

    variante, ruta = archivo_de_entrega(head_sha)
    valores = parsea(baja_predicciones(ruta, head_sha))

    oraculo, calificaciones = hojas()
    libro = calificaciones.sheet1
    previos = [f for f in libro.get_all_records() if str(f["hash8"]) == variante]
    columna = columna_de(oraculo, variante)   # solo confirma que la variante existe

    # Amarre variante <-> handle: el primer intento la reclama.
    duenos = {str(f["github_user"]) for f in previos} - {PROFESOR_GH}
    if not es_profesor and duenos and autor_pr not in duenos:
        termina(f"La variante `{variante}` ya está registrada a nombre de otra persona. "
                "Entrega la que corresponde a tu clave única.")
    usados = len([f for f in previos if str(f["github_user"]) != PROFESOR_GH])
    restantes = "sin límite (profesor)" if es_profesor else str(max(0, LIMITE_INTENTOS - usados))

    # `/validar` es un ensayo: revisa forma, no toca la hoja y no gasta intento.
    if modo == "validar":
        termina(
            f"### Formato correcto\n\n"
            f"| | |\n|---|---|\n"
            f"| Variante | `{variante}` |\n"
            f"| Archivo | `{ruta}` |\n"
            f"| Predicciones | {len(valores)} ✓ |\n"
            f"| Rango | {min(valores):.2f} a {max(valores):.2f} "
            f"(promedio {sum(valores) / len(valores):.2f}) |\n"
            f"| Intentos disponibles | {restantes} |\n"
            f"| Cierre | {limite_txt} |\n\n"
            "Tu entrega tiene la forma correcta y **esta revisión no consumió ningún "
            "intento**. Cuando quieras la calificación, comenta `/calificar`.\n\n"
            "Revisa que ese rango tenga sentido para lo que estás prediciendo: si se ve "
            "raro, probablemente el orden de tus predicciones no corresponde al de "
            "`test.csv`, y eso el formato no lo puede detectar."
        )

    if not es_profesor and usados >= LIMITE_INTENTOS:
        termina(f"@{autor_pr}: ya usaste tus {LIMITE_INTENTOS} intentos "
                f"para la variante `{variante}`, así que esta entrega no se calificó "
                "ni se registró. Tu calificación es la del último intento registrado.")
    intento = (len(previos) if es_profesor else usados) + 1

    y_test = y_test_de(oraculo, columna)
    if len(y_test) != len(valores):
        sys.exit(f"el oráculo trae {len(y_test)} valores y las predicciones {len(valores)}")
    mse_ref, mse_meta = referencias_de(oraculo, variante)

    mse = sum((p - y) ** 2 for p, y in zip(valores, y_test)) / len(y_test)
    calif = califica(mse, mse_ref, mse_meta)

    libro.append_row([
        datetime.now(UTC).isoformat(timespec="seconds"),
        variante, autor_pr, PR, head_sha[:12],
        round(mse, 4), calif, intento,
    ], value_input_option="USER_ENTERED")

    if calif >= 10:
        veredicto = "Llegaste al error irreducible: encontraste la estructura completa."
    elif calif >= 8:
        veredicto = "Te falta al menos un término. Revisa los residuales contra cada variable."
    elif calif > 5:
        veredicto = "Vas mejor que el modelo lineal, pero falta la mayor parte de la estructura."
    else:
        veredicto = ("No le ganaste a una regresión lineal con las variables crudas. "
                     "Algo del pipeline está mal, o el orden de tus predicciones no coincide "
                     "con el de `test.csv`.")

    comenta(
        f"### Tarea 01 — intento {intento}\n\n"
        f"| | |\n|---|---|\n"
        f"| Variante | `{variante}` |\n"
        f"| Tu MSE | **{mse:.2f}** |\n"
        f"| MSE del baseline lineal (= 5) | {mse_ref:.2f} |\n"
        f"| MSE meta (= 10) | {mse_meta:.2f} |\n"
        f"| **Calificación** | **{calif}** |\n"
        f"| Intentos restantes | {'sin límite (profesor)' if es_profesor else LIMITE_INTENTOS - intento} |\n"
        f"| Cierre | {limite_txt} |\n\n"
        f"{veredicto}"
    )
    print(f"variante={variante} usuario={autor_pr} intento={intento} "
          f"mse={mse:.4f} calif={calif}")


if __name__ == "__main__":
    main()
