# PowerShell script for testing on Windows
# Equivalent to test_linux_mac.sh

# Exit on first error
$ErrorActionPreference = "Stop"

$TEST_FOLDER = "test_env"

# Function to initialize Visual Studio environment
function Initialize-VisualStudioEnvironment {
    Write-Host "Initializing Visual Studio environment..."
    
    # Try to find Visual Studio installation using vswhere if available
    $vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path $vswhere) {
        $vsPath = & $vswhere -latest -property installationPath
        if ($vsPath) {
            $vcvarsPath = Join-Path $vsPath "VC\Auxiliary\Build\vcvars64.bat"
            if (Test-Path $vcvarsPath) {
                Write-Host "Found Visual Studio at: $vsPath"
                
                # Create a temporary batch file to capture environment variables
                $tempBatchFile = [System.IO.Path]::GetTempFileName() + ".bat"
                $tempEnvFile = [System.IO.Path]::GetTempFileName()
                
                # Create batch file to call vcvars64 and dump environment
                @"
@echo off
call "$vcvarsPath"
set > "$tempEnvFile"
"@ | Out-File -FilePath $tempBatchFile -Encoding ASCII
                
                # Run the batch file to dump environment variables
                cmd /c $tempBatchFile
                
                # Read environment variables and set them in current PowerShell session
                Get-Content $tempEnvFile | ForEach-Object {
                    if ($_ -match '(.+?)=(.*)') {
                        $name = $matches[1]
                        $value = $matches[2]
                        # Skip some special environment variables
                        if ($name -notmatch '^(PROMPT|_|=|COMPLUS_|VSCMD_)') {
                            Set-Item -Path "env:$name" -Value $value
                        }
                    }
                }
                
                # Clean up temporary files
                Remove-Item $tempBatchFile, $tempEnvFile
                
                Write-Host "Visual Studio environment initialized successfully."
                return $true
            }
        }
    }
    
    # Try common paths for vcvarsall.bat if vswhere is not available
    $vsVersions = @("2022", "2019", "2017")
    $vsEditions = @("Enterprise", "Professional", "Community", "BuildTools")
    
    foreach ($version in $vsVersions) {
        foreach ($edition in $vsEditions) {
            $vsPath = "${env:ProgramFiles}\Microsoft Visual Studio\$version\$edition"
            if (-not (Test-Path $vsPath)) {
                $vsPath = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\$version\$edition"
            }
            
            if (Test-Path $vsPath) {
                $vcvarsPath = Join-Path $vsPath "VC\Auxiliary\Build\vcvars64.bat"
                if (Test-Path $vcvarsPath) {
                    Write-Host "Found Visual Studio $version $edition at: $vsPath"
                    
                    # Create a temporary batch file to capture environment variables
                    $tempBatchFile = [System.IO.Path]::GetTempFileName() + ".bat"
                    $tempEnvFile = [System.IO.Path]::GetTempFileName()
                    
                    # Create batch file to call vcvars64 and dump environment
                    @"
@echo off
call "$vcvarsPath"
set > "$tempEnvFile"
"@ | Out-File -FilePath $tempBatchFile -Encoding ASCII
                    
                    # Run the batch file to dump environment variables
                    cmd /c $tempBatchFile
                    
                    # Read environment variables and set them in current PowerShell session
                    Get-Content $tempEnvFile | ForEach-Object {
                        if ($_ -match '(.+?)=(.*)') {
                            $name = $matches[1]
                            $value = $matches[2]
                            # Skip some special environment variables
                            if ($name -notmatch '^(PROMPT|_|=|COMPLUS_|VSCMD_)') {
                                Set-Item -Path "env:$name" -Value $value
                            }
                        }
                    }
                    
                    # Clean up temporary files
                    Remove-Item $tempBatchFile, $tempEnvFile
                    
                    Write-Host "Visual Studio environment initialized successfully."
                    return $true
                }
            }
        }
    }
    
    Write-Host "Warning: Could not find Visual Studio installation. MSVC builds may fail."
    return $false
}

# Initialize Visual Studio environment
Initialize-VisualStudioEnvironment

# Setup the environment
Write-Host "Creating Python virtual environment..."
python -m venv .venv
if (-not $?) { exit 1 }

# Activate the virtual environment
Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1
if (-not $?) { exit 1 }

# Build and install the python_load_poc package
Write-Host "Building and installing python_load_poc..."
Push-Location python_load_poc
pip install -r requirements.txt
if (-not $?) { exit 1 }

python setup.py build
if (-not $?) { exit 1 }

python setup.py install
if (-not $?) { exit 1 }
Pop-Location

# Do the testing (from another directory so it won't load the local python_load_poc)
Write-Host "Testing python_load_poc..."
if (-not (Test-Path $TEST_FOLDER)) {
    New-Item -ItemType Directory -Path $TEST_FOLDER | Out-Null
}
Push-Location $TEST_FOLDER
Write-Host ""
Write-Host "########################################################################################"
python -c "import python_load_poc; python_load_poc.print_message()"
if (-not $?) { 
    Write-Host "Test failed for python_load_poc"
    Pop-Location
    deactivate
    exit 1 
}
Write-Host "########################################################################################"
Write-Host ""
Pop-Location

# Create Makefile.win for alternative package if it doesn't exist
if (-not (Test-Path "python_load_poc_alt\python_load_poc_alt_c_extension\Makefile.win")) {
    Write-Host "Creating Makefile.win for alternative package..."
    Copy-Item "python_load_poc\python_load_poc_c_extension\Makefile.win" `
              "python_load_poc_alt\python_load_poc_alt_c_extension\Makefile.win"
    
    # Replace package names in the copied Makefile
    (Get-Content "python_load_poc_alt\python_load_poc_alt_c_extension\Makefile.win") | 
    ForEach-Object {$_ -replace "message\.dll", "message-internal.dll"} | 
    ForEach-Object {$_ -replace "message-internal-internal\.dll", "message-internal.dll"} | 
    Set-Content "python_load_poc_alt\python_load_poc_alt_c_extension\Makefile.win"
}

# Install the alternative package
Write-Host "Building and installing python_load_poc_alt..."
Push-Location python_load_poc_alt
pip install -r requirements.txt
if (-not $?) { exit 1 }

python setup.py build
if (-not $?) { exit 1 }

python setup.py install
if (-not $?) { exit 1 }
Pop-Location

# Do the testing for the alternative package
Write-Host "Testing python_load_poc after installing alternative..."
Push-Location $TEST_FOLDER
Write-Host ""
Write-Host "########################################################################################"
python -c "import python_load_poc; python_load_poc.print_message()"
if (-not $?) { 
    Write-Host "Test failed for python_load_poc after installing alternative"
    Pop-Location
    deactivate
    exit 1 
}
Write-Host "########################################################################################"
Write-Host ""
Pop-Location

# Cleanup
Write-Host "Tests completed successfully!"
deactivate
& .\cleanup_windows.ps1