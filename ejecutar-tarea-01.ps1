$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonTarea = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonTarea)) {
    throw 'Falta el entorno .venv. Ejecuta uv sync --frozen desde la raiz del repositorio.'
}
# Registra el kernel dentro de .venv, con la ruta de Python de este checkout.
& $pythonTarea -m ipykernel install --sys-prefix --name mineria-datos --display-name 'Python 3.13 (mineria-datos)'
if ($LASTEXITCODE -ne 0) { throw 'No se pudo registrar el kernel local.' }
# Ejecuta el notebook y regenera los resultados.
& $pythonTarea -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 'tareas/tarea_01_aproximacion_funcion.ipynb'
if ($LASTEXITCODE -ne 0) { throw 'Fallo la ejecucion local del notebook.' }
& $pythonTarea 'tareas/verificar_tarea_01.py'
if ($LASTEXITCODE -ne 0) { throw 'Fallo la verificacion local de los resultados.' }
