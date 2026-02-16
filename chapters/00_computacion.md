# Requerimientos computacionales

## Introducción

Aunque en su práctica profesional probablemente no ejecutarán procesos de minería de datos personalmente, es fundamental que comprendan cómo funcionan estas herramientas y puedan seguir el flujo completo de un proyecto de ciencia de datos. Para ello, necesitarán familiarizarse con el ecosistema de herramientas que utilizan los científicos de datos.

Este curso ofrece dos caminos para configurar su entorno de trabajo:

1. **GitHub Codespaces (Recomendado)**: Un entorno completamente configurado en la nube. Solo necesitan una cuenta de GitHub y un navegador. Ideal para comenzar rápidamente sin instalaciones locales.

2. **Desarrollo Local**: Si prefieren trabajar en su propia computadora, pueden instalar las herramientas necesarias localmente. Esto les da más control y no depende de límites de uso de servicios en la nube.

Ambas opciones proporcionan exactamente el mismo entorno de desarrollo con Python 3.13 y todas las bibliotecas necesarias para el curso.

---

## Opción 1: GitHub Codespaces (Recomendado)

Esta es la forma más rápida de comenzar. GitHub Codespaces proporciona un entorno de desarrollo completo en la nube, accesible desde su navegador.

### 1.1 Crear cuenta en GitHub

Si aún no tienen una cuenta en GitHub:

1. Visiten [github.com](https://github.com)
2. Hagan clic en "Sign up" (Registrarse)
3. Proporcionen:
   - Dirección de email (preferentemente su email institucional)
   - Contraseña segura
   - Nombre de usuario (puede ser su nombre o un alias profesional)
4. Verifiquen su dirección de email siguiendo el enlace que recibirán por correo
5. Completen el proceso de configuración inicial

**Nota**: La cuenta gratuita de GitHub es suficiente para este curso. Incluye 60 horas mensuales de Codespaces sin costo.

### 1.2 Fork del repositorio

Un "fork" es una copia del repositorio del curso en su propia cuenta de GitHub. Esto les permite trabajar con los materiales sin afectar el repositorio original.

**Pasos para hacer fork:**

1. Inicien sesión en su cuenta de GitHub
2. Visiten el repositorio del curso: [https://github.com/nasaul/mineria_datos](https://github.com/nasaul/mineria_datos)
3. En la esquina superior derecha, hagan clic en el botón **"Fork"**
4. GitHub creará una copia del repositorio en su cuenta (se verá como `su-usuario/mineria_datos`)
5. Serán redirigidos automáticamente a su fork

### 1.3 Iniciar GitHub Codespaces

Desde su fork del repositorio:

1. Hagan clic en el botón verde **"Code"**
2. Seleccionen la pestaña **"Codespaces"**
3. Hagan clic en **"Create codespace on main"**

**Qué esperar:**

- La primera vez, la inicialización puede tomar 2-3 minutos
- Verán una pantalla de carga indicando que se está configurando el entorno
- Al finalizar, se abrirá VS Code en su navegador con todo configurado automáticamente:
  - Python 3.13
  - Todas las bibliotecas de ciencia de datos (numpy, pandas, scikit-learn, etc.)
  - Jupyter Lab
  - Extensiones de VS Code recomendadas

**Importante**: Los Codespaces se suspenden automáticamente después de 30 minutos de inactividad y se eliminan después de 30 días sin uso. Sus archivos guardados permanecerán en su repositorio.

### 1.4 Primeros pasos en Codespaces

Una vez que Codespaces esté listo:

**Abrir la terminal:**

- Presionen `` Ctrl+` `` (backtick) o vayan a menú "Terminal" > "New Terminal"

**Verificar instalación:**
```bash
python --version
# Debe mostrar: Python 3.13.x
```

**Comandos disponibles:**

El proyecto usa `just` como ejecutor de tareas. Para ver todos los comandos disponibles:
```bash
just
```

**Iniciar Jupyter Lab:**
```bash
just lab
```

Esto abrirá Jupyter Lab en una nueva pestaña de su navegador, donde podrán crear y ejecutar notebooks.

**Otros comandos útiles:**

- `just preview` - Iniciar servidor de previsualización de Quarto (para ver las notas del curso)
- `just render` - Generar la versión final del libro
- `just format` - Formatear el código Python automáticamente

---

## Opción 2: Desarrollo Local

Si prefieren trabajar en su propia computadora, sigan estos pasos. Esta opción requiere más configuración inicial pero les da control completo sobre su entorno.

### 2.1 Instalar uv

`uv` es un gestor de paquetes y entornos virtuales de Python extremadamente rápido. Lo usaremos para manejar las dependencias del proyecto.

#### En macOS

**Opción 1: Usando el instalador automático (recomendado)**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Opción 2: Usando Homebrew**
```bash
brew install uv
```

**Agregar al PATH:**
El instalador debería configurar esto automáticamente. Si no, agreguen esta línea a su `~/.zshrc` o `~/.bash_profile`:
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

**Verificar instalación:**
```bash
uv --version
```

#### En Windows

**Opción 1: Usando PowerShell (recomendado)**

Abran PowerShell como administrador y ejecuten:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Nota sobre Execution Policy**: Si reciben un error sobre la política de ejecución, ejecuten primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Opción 2: Usando winget**
```powershell
winget install --id=astral-sh.uv -e
```

**Reiniciar terminal:**
Después de instalar, cierren y vuelvan a abrir su terminal.

**Verificar instalación:**
```powershell
uv --version
```

### 2.2 Instalar Visual Studio Code

VS Code es el editor de código recomendado para este curso. Es gratuito, potente y tiene excelente soporte para Python y Jupyter.

**Instalación:**

1. Descarguen VS Code desde [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Ejecuten el instalador:
   - **Windows**: Ejecuten el archivo `.exe` descargado. Durante la instalación, marquen la opción "Add to PATH"
   - **macOS**: Arrastren la aplicación a la carpeta "Applications"

**Agregar comando `code` al PATH (macOS):**

Si en macOS no pueden ejecutar `code` desde la terminal:

1. Abran VS Code
2. Presionen `Cmd+Shift+P` para abrir la paleta de comandos
3. Escriban "shell command" y seleccionen "Shell Command: Install 'code' command in PATH"

**Verificar:**
```bash
code --version
```

### 2.3 Extensiones recomendadas de VS Code

Las siguientes extensiones mejorarán significativamente su experiencia de desarrollo:

- **Python** (`ms-python.python`) - Soporte completo para Python
- **Pylance** (`ms-python.vscode-pylance`) - IntelliSense avanzado para Python
- **Jupyter** (`ms-toolsai.jupyter`) - Soporte para notebooks
- **Ruff** (`charliermarsh.ruff`) - Linter y formateador rápido

**Instalación automática:**

Al abrir el proyecto, VS Code detectará el archivo de configuración y les sugerirá instalar las extensiones recomendadas. Simplemente hagan clic en "Install All" cuando aparezca la notificación.

**Instalación manual:**

Si no aparece la notificación, pueden instalarlas manualmente:

1. Abran la vista de extensiones con `Cmd+Shift+X` (macOS) o `Ctrl+Shift+X` (Windows)
2. Busquen cada extensión por su nombre
3. Hagan clic en "Install"

### 2.4 Clonar y configurar el proyecto

**Clonar el repositorio:**

Desde su terminal, naveguen a la carpeta donde deseen guardar el proyecto y ejecuten:

```bash
# Si hicieron fork, usen la URL de su fork:
git clone https://github.com/su-usuario/mineria_datos.git

# O clonen directamente el repositorio original:
git clone https://github.com/nasaul/mineria_datos.git

# Entren al directorio del proyecto:
cd mineria_datos
```

**Sincronizar dependencias:**

`uv` leerá el archivo `pyproject.toml` e instalará todas las dependencias necesarias:

```bash
uv sync
```

Este comando:
- Creará un entorno virtual en `.venv/`
- Instalará Python 3.13 si no está disponible
- Instalará todas las bibliotecas listadas en `pyproject.toml`

**Abrir en VS Code:**

```bash
code .
```

Esto abrirá el proyecto en VS Code. Al hacerlo por primera vez, VS Code:
- Detectará el entorno virtual en `.venv/`
- Sugerirá instalar las extensiones recomendadas
- Configurará el intérprete de Python automáticamente

### 2.5 Uso básico de uv

Una vez instalado, estos son los comandos esenciales de `uv` que usarán:

**Sincronizar dependencias (instalar paquetes del `pyproject.toml`):**
```bash
uv sync
```

**Activar el entorno virtual manualmente** (generalmente no es necesario con VS Code):

- macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```
- Windows (PowerShell):
  ```powershell
  .venv\Scripts\activate
  ```
- Windows (CMD):
  ```cmd
  .venv\Scripts\activate.bat
  ```

**Ejecutar comandos sin activar el entorno:**

`uv run` ejecuta comandos usando el entorno del proyecto automáticamente:

```bash
# Iniciar Jupyter Lab
uv run jupyter lab

# Ejecutar un script de Python
uv run python mi_script.py

# Usar comandos definidos con just
uv run just lab
```

**Instalar un paquete adicional:**
```bash
uv add nombre-paquete
# Ejemplo:
uv add requests
```

**Eliminar un paquete:**
```bash
uv remove nombre-paquete
```

**Ver paquetes instalados:**
```bash
uv pip list
```

---

## Verificación de la instalación

Independientemente de la opción que hayan elegido, verifiquen que todo funcione correctamente:

### Verificar Python y paquetes

Abran una terminal (en Codespaces o localmente) y ejecuten:

```python
python -c "import numpy, pandas, sklearn; print('¡Todo funciona correctamente!')"
```

Si no ven errores y aparece el mensaje de éxito, están listos.

### Probar Jupyter Lab

1. Inicien Jupyter Lab:
   ```bash
   just lab
   ```
   O directamente:
   ```bash
   uv run jupyter lab  # Desarrollo local
   jupyter lab          # Codespaces
   ```

2. En Jupyter Lab, creen un nuevo notebook (Python 3)

3. En la primera celda, ejecuten:
   ```python
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt

   print(f"NumPy version: {np.__version__}")
   print(f"Pandas version: {pd.__version__}")
   print("¡Entorno configurado correctamente!")
   ```

4. Ejecuten la celda con `Shift+Enter`

Si todo funciona sin errores, su entorno está completamente configurado.

---

## Introducción a Git y GitHub

### ¿Qué es Git?

**Git** es un sistema de control de versiones distribuido. En términos simples, es una herramienta que registra los cambios en sus archivos a lo largo del tiempo, permitiéndoles:

- Mantener un historial completo de modificaciones
- Regresar a versiones anteriores si algo sale mal
- Colaborar con otros sin sobrescribir el trabajo ajeno
- Experimentar con nuevas ideas en "ramas" separadas sin afectar el código principal

Piensen en Git como un "sistema de guardado avanzado" que no solo guarda su trabajo, sino que mantiene un registro detallado de cada cambio, quién lo hizo y cuándo.

### ¿Qué es GitHub?

**GitHub** es una plataforma en la nube que aloja repositorios de Git. Mientras que Git funciona localmente en su computadora, GitHub proporciona:

- Un lugar centralizado para almacenar su código
- Herramientas de colaboración (pull requests, code reviews)
- Respaldo automático de su trabajo
- Una forma de compartir su código públicamente

**Analogía**: Si Git es como Word con "Control de cambios" activado, GitHub es como Google Drive donde almacenan y comparten esos documentos.

### Conceptos fundamentales

Antes de usar Git, es importante entender estos conceptos:

- **Repositorio (repo)**: Una carpeta que Git está rastreando. Contiene todos sus archivos y el historial completo de cambios.
- **Commit**: Una "instantánea" de sus archivos en un momento específico. Como guardar una versión con un nombre descriptivo.
- **Branch (rama)**: Una línea independiente de desarrollo. La rama principal suele llamarse `main` o `master`.
- **Remote**: Una versión del repositorio almacenada en un servidor (como GitHub).
- **Clone**: Descargar una copia completa de un repositorio remoto a su computadora.
- **Fork**: Crear una copia de un repositorio ajeno en su cuenta de GitHub.
- **Pull**: Descargar cambios del repositorio remoto a su copia local.
- **Push**: Enviar sus commits locales al repositorio remoto.

### Flujo de trabajo básico con Git

El flujo típico de trabajo con Git sigue estos pasos:

1. **Modifican archivos** en su proyecto
2. **Agregan cambios al área de preparación** (`git add`) - seleccionan qué cambios quieren guardar
3. **Crean un commit** (`git commit`) - guardan esos cambios con un mensaje descriptivo
4. **Suben los commits** (`git push`) - envían los cambios a GitHub

Este ciclo se repite continuamente mientras trabajan en su proyecto.

### Configuración inicial de Git

Si están trabajando localmente (no en Codespaces), deben configurar Git con su información:

```bash
# Configurar su nombre (aparecerá en los commits)
git config --global user.name "Tu Nombre"

# Configurar su email (debe coincidir con el de GitHub)
git config --global user.email "tu-email@ejemplo.com"

# Verificar la configuración
git config --list
```

**Nota**: En GitHub Codespaces, esto ya está configurado automáticamente.

### Comandos principales de Git

#### Ver el estado actual

El comando más usado. Muestra qué archivos han cambiado y cuáles están listos para commit:

```bash
git status
```

**Ejemplo de salida:**
```
On branch main
Changes not staged for commit:
  modified:   chapters/0_computacion.md

Untracked files:
  nuevo_archivo.py
```

#### Agregar cambios al área de preparación

Antes de hacer commit, deben "preparar" los archivos que quieren incluir:

```bash
# Agregar un archivo específico
git add nombre_archivo.py

# Agregar todos los archivos modificados en una carpeta
git add chapters/

# Agregar todos los cambios en el proyecto
git add .

# Agregar solo archivos Python modificados
git add *.py
```

**Consejo**: Usen `git status` después de `git add` para verificar qué archivos están preparados.

#### Crear un commit

Un commit guarda los cambios preparados con un mensaje descriptivo:

```bash
# Commit con mensaje corto
git commit -m "Agrega función para calcular la media"

# Commit con mensaje detallado
git commit -m "Implementa análisis exploratorio de datos

- Agrega funciones para estadísticas descriptivas
- Incluye visualizaciones con matplotlib
- Actualiza documentación con ejemplos"
```

**Buenas prácticas para mensajes de commit:**
- Usen verbos en presente: "Agrega" en lugar de "Agregué" o "Agregado"
- Sean específicos pero concisos
- Primera línea máximo 50 caracteres
- Si necesitan más detalle, dejen una línea en blanco y agreguen más explicación

#### Ver el historial de commits

Para ver qué cambios se han hecho:

```bash
# Ver historial completo
git log

# Ver historial resumido (una línea por commit)
git log --oneline

# Ver últimos 5 commits
git log -5

# Ver historial con gráfico de ramas
git log --oneline --graph --all
```

#### Ver diferencias

Para ver exactamente qué cambió en los archivos:

```bash
# Ver cambios no preparados (working directory vs último commit)
git diff

# Ver cambios preparados (staging area vs último commit)
git diff --staged

# Ver cambios en un archivo específico
git diff nombre_archivo.py

# Comparar dos commits
git diff commit1 commit2
```

#### Deshacer cambios

Si cometieron un error, pueden revertirlo:

```bash
# Descartar cambios en un archivo (¡cuidado! se pierden los cambios)
git checkout -- nombre_archivo.py

# Quitar un archivo del área de preparación (sin perder cambios)
git reset nombre_archivo.py

# Quitar todos los archivos del área de preparación
git reset

# Deshacer el último commit (manteniendo los cambios)
git reset --soft HEAD~1

# Ver un archivo como estaba en un commit anterior
git show commit_hash:ruta/archivo.py
```

### Trabajando con repositorios remotos (GitHub)

#### Clonar un repositorio

Para descargar un repositorio desde GitHub:

```bash
# Clonar usando HTTPS
git clone https://github.com/usuario/repositorio.git

# Clonar su fork del curso
git clone https://github.com/su-usuario/mineria_datos.git

# Clonar en una carpeta específica
git clone https://github.com/usuario/repo.git mi_carpeta
```

#### Ver repositorios remotos

```bash
# Ver qué remotos están configurados
git remote -v

# Agregar un remote adicional
git remote add nombre-remote https://github.com/usuario/repo.git

# Cambiar URL de un remote
git remote set-url origin nueva-url
```

#### Descargar cambios (Pull)

Para obtener cambios del repositorio remoto:

```bash
# Descargar y fusionar cambios de la rama actual
git pull

# Descargar cambios de una rama específica
git pull origin main

# Solo descargar cambios sin fusionar
git fetch
```

**Cuándo usar pull:**

- Antes de empezar a trabajar cada día
- Cuando otros colaboradores hayan subido cambios
- Antes de hacer push de sus propios cambios

#### Subir cambios (Push)

Para enviar sus commits a GitHub:

```bash
# Subir cambios de la rama actual
git push

# Subir una rama específica
git push origin nombre-rama

# Primera vez que suben una rama nueva
git push -u origin nombre-rama

# Forzar push (¡cuidado! puede sobrescribir trabajo ajeno)
git push --force  # Eviten esto a menos que sepan lo que hacen
```

### Trabajando con ramas (Branches)

Las ramas permiten trabajar en nuevas características sin afectar el código principal:

```bash
# Ver todas las ramas
git branch

# Crear una rama nueva
git branch nombre-rama

# Cambiar a una rama
git checkout nombre-rama

# Crear y cambiar a una rama (en un solo comando)
git checkout -b nombre-rama

# Eliminar una rama local
git branch -d nombre-rama

# Ver ramas remotas
git branch -r

# Ver todas las ramas (locales y remotas)
git branch -a
```

#### Fusionar ramas (Merge)

Para incorporar cambios de una rama a otra:

```bash
# Primero, cambiarse a la rama destino
git checkout main

# Luego, fusionar la otra rama
git merge nombre-rama

# Si hay conflictos, Git les indicará qué archivos revisar
# Después de resolver conflictos:
git add archivo-con-conflicto
git commit -m "Resuelve conflictos de merge"
```

### Flujo de trabajo recomendado para el curso

Para trabajar en sus tareas y proyectos:

**1. Al comenzar el trabajo:**
```bash
# Asegurarse de estar en main
git checkout main

# Descargar últimos cambios
git pull

# Crear una rama para su trabajo
git checkout -b tarea-1
```

**2. Mientras trabajan:**
```bash
# Hacer cambios en sus archivos...

# Ver qué cambió
git status
git diff

# Agregar cambios
git add .

# Hacer commit
git commit -m "Completa ejercicio de análisis exploratorio"

# Repetir este ciclo cuantas veces necesiten
```

**3. Al terminar:**
```bash
# Subir la rama a GitHub
git push -u origin tarea-1

# Luego pueden crear un Pull Request en GitHub para revisión
# O fusionar localmente:
git checkout main
git merge tarea-1
git push
```

### Ignorar archivos con .gitignore

No todos los archivos deben subirse a Git. El archivo `.gitignore` especifica qué ignorar:

```bash
# Ejemplo de .gitignore para proyectos de datos
__pycache__/
*.pyc
.ipynb_checkpoints/
.venv/
.env
datos_privados/
*.csv
*.xlsx
```

**Qué ignorar:**
- Archivos generados automáticamente (`__pycache__`, `.pyc`)
- Entornos virtuales (`.venv/`)
- Datos sensibles o privados
- Archivos de configuración local
- Datasets grandes (usar Git LFS o almacenamiento externo)

### Comandos útiles adicionales

```bash
# Ver quién modificó cada línea de un archivo
git blame nombre_archivo.py

# Buscar en el historial
git log --grep="palabra clave"

# Ver archivos rastreados
git ls-files

# Renombrar/mover archivos
git mv archivo_viejo.py archivo_nuevo.py

# Eliminar archivos
git rm archivo.py

# Guardar cambios temporalmente sin hacer commit
git stash
git stash list
git stash pop

# Ver información de un commit específico
git show commit_hash

# Crear un tag (útil para versiones)
git tag v1.0.0
git push --tags
```

### Recursos para aprender más

- **Documentación oficial de Git**: [https://git-scm.com/doc](https://git-scm.com/doc)
- **Git en español**: [https://git-scm.com/book/es/v2](https://git-scm.com/book/es/v2)
- **GitHub Guides**: [https://guides.github.com/](https://guides.github.com/)
- **Visualizar Git**: [https://git-school.github.io/visualizing-git/](https://git-school.github.io/visualizing-git/)
- **Práctica interactiva**: [https://learngitbranching.js.org/?locale=es_ES](https://learngitbranching.js.org/?locale=es_ES)

### Consejos finales

1. **Hagan commits frecuentes**: Es mejor tener muchos commits pequeños que pocos commits gigantes
2. **Mensajes descriptivos**: Un buen mensaje de commit explica el "por qué", no solo el "qué"
3. **Pull antes de push**: Siempre descarguen cambios antes de subir los suyos para evitar conflictos
4. **Una tarea, una rama**: Trabajen en ramas separadas para diferentes características o tareas
5. **No suban archivos grandes**: Git no está diseñado para datasets de muchos GB
6. **Revisen antes de commit**: Usen `git diff` para verificar qué están guardando
7. **No teman experimentar**: Si algo sale mal, casi siempre hay forma de revertirlo

---

## Soporte y ayuda

Si encuentran problemas durante la configuración:

1. **Revisen los errores cuidadosamente**: Los mensajes de error suelen indicar qué salió mal
2. **Consulten la documentación oficial**:
   - [GitHub Codespaces](https://docs.github.com/es/codespaces)
   - [uv documentation](https://docs.astral.sh/uv/)
   - [VS Code documentation](https://code.visualstudio.com/docs)
3. **Pregunten en clase**: Probablemente otros compañeros tengan dudas similares
4. **Usen el foro del curso**: Compartan su problema y es probable que alguien pueda ayudar

**Problemas comunes:**

- **Codespaces no inicia**: Verifiquen que no hayan excedido las 60 horas mensuales gratuitas
- **`uv` no se encuentra**: Asegúrense de haber reiniciado la terminal después de instalar
- **Errores de permisos en Windows**: Ejecuten PowerShell como administrador
- **Python no se encuentra**: Verifiquen que el PATH esté configurado correctamente
