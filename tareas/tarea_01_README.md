# Tarea 01 — Cómo entregar

La tarea está en [`tarea_01_aproximacion_funcion.ipynb`](tarea_01_aproximacion_funcion.ipynb).
Este documento es solo la mecánica de la entrega.

| | |
|---|---|
| **Cierre** | domingo 20 de septiembre, 11:59 pm (hora de CDMX) |
| **Intentos de calificación** | 3 |
| **Revisiones de formato** | ilimitadas (`/validar`) |

Si nunca han usado git, esta parte les va a tomar más tiempo que la regresión. Es a
propósito: abrir un Pull Request es la forma en que se colabora en software, y van a
hacerlo el resto de su carrera.

---

## Regla de oro para esta parte

**Pídanle a su IA que les explique cada comando antes de correrlo. Si no pueden decir qué
hace, no lo corran.**

Copiar comandos de git sin entenderlos es la manera más rápida de perder trabajo. La IA
es excelente explicando git; úsenla para eso y no para que teclee por ustedes.

Prueben preguntas como: *"¿qué diferencia hay entre un fork y un clone?"*, *"¿qué le pasa
a mis cambios cuando hago `git checkout -b`?"*, *"¿por qué mi push dice que no tengo
permisos?"*.

---

## 1. Hagan un fork

Un **fork** es su copia personal del repositorio, en su propia cuenta de GitHub. No
tienen permiso para escribir en el repo del curso, y no lo necesitan: trabajan en su
copia y al final proponen sus cambios.

En <https://github.com/nasaul/mineria_datos>, botón **Fork** (arriba a la derecha) →
**Create fork**.

## 2. Clonen su fork a su computadora

```bash
git clone https://github.com/SU-USUARIO/mineria_datos.git
cd mineria_datos
```

Cambien `SU-USUARIO` por su usuario de GitHub. Si clonan el del curso en lugar del suyo,
el `git push` del paso 6 va a fallar con un error de permisos — es la equivocación más
común.

## 3. Instalen las dependencias

```bash
uv sync
```

Si no tienen `uv`: <https://docs.astral.sh/uv/getting-started/installation/>.

Para abrir el notebook:

```bash
uv run jupyter lab
```

## 4. Creen una rama

```bash
git checkout -b tarea-01
```

Una **rama** es una línea de trabajo separada. Trabajar en una rama en lugar de en `main`
mantiene su trabajo aislado y es lo que hace posible el Pull Request del paso 7.

## 5. Hagan la tarea

Abran `tareas/tarea_01_aproximacion_funcion.ipynb` y trabajen ahí. La primera celda pide
su **clave única del ITAM**: de ahí sale el nombre de su carpeta de datos, así que si la
escriben mal el notebook no va a encontrar nada.

La última celda escribe su archivo de predicciones en
`entregas/tarea-01/<su-id-de-variante>/predicciones.csv`. Ese es el archivo que se
califica, y la carpeta la crea el notebook solo.

## 6. Commit y push

```bash
git add tareas/tarea_01_aproximacion_funcion.ipynb entregas/
git commit -m "Tarea 01"
git push -u origin tarea-01
```

`git add` selecciona qué cambios entran, `git commit` los guarda con un mensaje en su
computadora, y `git push` los sube a su fork en GitHub. Son tres pasos distintos y vale
la pena entender por qué.

Pueden hacer commit y push tantas veces como quieran: **subir cambios no gasta intentos**.

## 7. Abran el Pull Request

Después del push, GitHub imprime una liga en la terminal. Ábranla, o vayan a su fork y
usen el botón **Compare & pull request**.

Verifiquen que diga:

```
base: nasaul/mineria_datos  main   <-   compare: SU-USUARIO/mineria_datos  tarea-01
```

Un **Pull Request** es una propuesta de cambios más una conversación alrededor. Aquí es
además el canal de entrega: no se mergea, solo se califica y se cierra.

## 8. Validen el formato

Comenten esto en su PR:

```
/validar
```

Un bot revisa que su `predicciones.csv` tenga la forma correcta y les responde con su
**MSE objetivo**: cuál es el error del baseline lineal (la calificación 5) y cuál el del
modelo bien especificado (el 10).

`/validar` **no consume intentos** y lo pueden usar cuantas veces quieran. Úsenlo siempre
antes de calificar. Si marca un error, corrijan, hagan push otra vez y vuelvan a comentar.

## 9. Califiquen

Cuando estén conformes:

```
/calificar
```

Esto sí gasta uno de sus **3 intentos**. El bot mide su MSE contra el conjunto de prueba,
les responde con la calificación y la registra. Su calificación final es la del **último
intento que hayan usado**, no la mejor — así que no gasten el tercero a menos que crean
que van a mejorar.

---

## Errores comunes

| Síntoma | Causa |
|---|---|
| `git push` dice que no tienen permisos | Clonaron el repo del curso en lugar de su fork |
| "No existe la carpeta vXXXXXXXX" | Su clave única está mal escrita en el notebook |
| "No encontré tu entrega" | No hicieron commit de `entregas/`, o no hicieron push |
| "trae 399 predicciones y deben ser 400" | Filtraron o perdieron renglones de `test.csv` |
| El bot no responde | El comentario debe **empezar** con `/validar` o `/calificar` |
| "La Tarea 01 no está abierta" / "el plazo cerró" | Fuera de la ventana de entregas |

Ninguno de estos consume intento. Solo `/calificar` con un archivo válido lo hace.

---

## Sobre la IA

**Sí pueden usarla, y quiero que la usen.** Pero como tutor, no como chofer.

La IA no puede ver sus datos, y cada quien tiene datos distintos: las 12 variables juegan
papeles diferentes según la persona. Puede proponerles transformaciones y explicarles
conceptos, pero no puede saber cuál de sus gráficas de residuales tiene forma. Eso solo
lo revela correr el código.

Péguenle esto al inicio de cada conversación:

> Eres mi tutor de regresión, no mi resolvedor. Reglas: (1) no escribes código que yo
> pueda copiar; si te pido código, me devuelves el nombre de la función y su docstring.
> (2) No me das la respuesta: me preguntas qué espero ver y por qué. (3) Cuando me
> equivoque, no me corriges: me sugieres qué gráfica revelaría mi error. (4) Máximo tres
> oraciones por respuesta.

La **Parte 5** del notebook les pide documentar cada hipótesis que probaron, incluidas las
que fallaron, y un momento concreto en el que la IA se equivocó. Esa parte vale tanto como
el MSE: un notebook con buen error y bitácora vacía significa que no entendieron por qué
funcionó.

Comparar **métodos** entre ustedes es buena idea y se lo recomiendo. Comparar
**resultados** no sirve de nada: sus datos son distintos.
