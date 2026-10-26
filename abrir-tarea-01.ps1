$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonTarea = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonTarea)) {
    throw 'Falta el entorno .venv. Instala las dependencias con uv sync --frozen.'
}
& $pythonTarea -m ipykernel install --sys-prefix --name mineria-datos --display-name 'Python 3.13 (mineria-datos)'
if ($LASTEXITCODE -ne 0) { throw 'No se pudo registrar el kernel local.' }
& $pythonTarea -m jupyterlab 'tareas/tarea_01_aproximacion_funcion.ipynb'
