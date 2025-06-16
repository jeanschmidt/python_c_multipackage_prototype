# PowerShell script for cleanup on Windows
# Equivalent to cleanup_linux_mac.sh

# Remove virtualenv and test directory
if (Test-Path ".venv") {
    Remove-Item -Recurse -Force .venv
}

if (Test-Path "test_env") {
    Remove-Item -Recurse -Force test_env
}

# Clean python_load_poc
Push-Location python_load_poc
Get-ChildItem -Filter "*.egg-info" -Directory | Remove-Item -Recurse -Force
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
}

# Clean C extension
Push-Location python_load_poc_c_extension
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
}
Pop-Location
Pop-Location

# Clean python_load_poc_alt
Push-Location python_load_poc_alt
Get-ChildItem -Filter "*.egg-info" -Directory | Remove-Item -Recurse -Force
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
}

# Clean C extension
Push-Location python_load_poc_alt_c_extension
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
}
Pop-Location
Pop-Location

Write-Host "Cleanup completed."