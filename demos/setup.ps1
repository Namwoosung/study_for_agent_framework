$ErrorActionPreference = 'Stop'
$DemoRoot = $PSScriptRoot
$Private = Join-Path $DemoRoot '.local'
$Runtime = Join-Path $DemoRoot 'hermes/.runtime'
$Source = Join-Path $Runtime 'source/hermes-agent-0.22.5'
New-Item -ItemType Directory -Force $Private,$Runtime | Out-Null

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program exited with $LASTEXITCODE" }
}

$Zip = Join-Path $Runtime 'hermes.zip'
if (-not (Test-Path -LiteralPath $Zip)) {
    Invoke-Checked curl.exe @('-fLsS','https://codeload.github.com/NousResearch/hermes-agent/zip/refs/tags/v0.22.5','-o',$Zip)
}
Invoke-Checked py @('-3.14','-m','venv',(Join-Path $Private 'hermes314'))
Invoke-Checked py @('-3.11','-m','venv',(Join-Path $Private 'pa'))
$HermesPython = Join-Path $Private 'hermes314/Scripts/python.exe'
$PAPython = Join-Path $Private 'pa/Scripts/python.exe'
$Requirements = Join-Path $Private 'hermes-requirements-demo.txt'
$Extract = @'
import sys, tomllib, zipfile
from pathlib import Path

archive, destination, requirements = map(Path, sys.argv[1:])
root = 'hermes-agent-0.22.5'
with zipfile.ZipFile(archive) as z:
    if not (destination / root / '.demo-extracted').exists():
        z.extractall(destination)
        (destination / root / '.demo-extracted').touch()
    project = tomllib.loads(z.read(f'{root}/pyproject.toml').decode())
deps = project['project']['dependencies']
# Browser tools are excluded from these demos. Their package pins a different Pillow version.
requirements.write_text('\n'.join(dep for dep in deps if not dep.lower().startswith('browser-harness==')),
                        encoding='utf-8')
'@
Invoke-Checked $HermesPython @('-c',$Extract,$Zip,(Join-Path $Runtime 'source'),$Requirements)
Invoke-Checked $HermesPython @('-m','pip','install','-r',$Requirements)
Invoke-Checked $PAPython @('-m','pip','install','pydantic-ai-slim[openai]==2.61.0','pydantic-ai-harness==0.61.0')
