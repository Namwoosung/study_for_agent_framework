param([ValidateSet('hermes','pydanticai','bridge')][string]$Service)
$ErrorActionPreference = 'Stop'
$Private = Join-Path $PSScriptRoot '.local'
switch ($Service) {
    'hermes' {
        & (Join-Path $Private 'hermes314/Scripts/python.exe') -u (Join-Path $PSScriptRoot 'hermes/run.py')
    }
    'pydanticai' {
        & (Join-Path $Private 'pa/Scripts/python.exe') -u (Join-Path $PSScriptRoot 'pydanticai/run.py')
    }
    'bridge' {
        $Relay = Join-Path $Private 'openai_bridge.py'
        if (-not (Test-Path -LiteralPath $Relay)) { throw 'Private OpenAI relay is installed separately on the demo PC.' }
        & py -3.14 -u $Relay
    }
    default { throw 'Specify -Service hermes, pydanticai or bridge.' }
}
exit $LASTEXITCODE
