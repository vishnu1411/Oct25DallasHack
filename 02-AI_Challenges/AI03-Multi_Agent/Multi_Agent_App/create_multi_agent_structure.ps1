# Multi-Agent Structure Creation Script
param(
    [string]$BaseDir = "."
)

Write-Host "Creating Multi-Agent Application Structure..." -ForegroundColor Green

# Function to create directories
function Create-Directory {
    param([string]$Path)
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "Created directory: $Path" -ForegroundColor Yellow
    }
}

# Function to create files
function Create-File {
    param([string]$Path, [string]$Content)
    $dir = Split-Path $Path -Parent
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    Set-Content -Path $Path -Value $Content -Encoding UTF8
    Write-Host "Created file: $Path" -ForegroundColor Cyan
}

# Create directory structure
$dirs = @(
    "config",
    "models", 
    "services",
    "agents",
    "utils",
    "tests"
)

foreach ($dir in $dirs) {
    Create-Directory -Path (Join-Path $BaseDir $dir)
}

# 1. requirements.txt
$requirements = @"
azure-search-documents==11.4.0
azure-identity==1.15.0
openai==1.3.0
python-dotenv==1.0.0
rich==13.7.0
aiohttp==3.9.1
asyncio-mqtt==0.13.0
pydantic==2.5.0
pytest==7.4.3
pytest-asyncio==0.21.1
"@
Create-File -Path (Join-Path $BaseDir "requirements.txt") -Content $requirements

# 2. .env
$env_content = @"
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=your_openai_endpoint_here
AZURE_OPENAI_KEY=your_openai_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2023-12-01-preview

# Azure Search Configuration  
AZURE_SEARCH_ENDPOINT=your_search_endpoint_here
AZURE_SEARCH_KEY=your_search_api_key_here
AZURE_SEARCH_INDEX=retail-index

# Application Settings
LOG_LEVEL=INFO
MAX_RETRIES=3
TIMEOUT_SECONDS=30
"@
Create-File -Path (Join-Path $BaseDir ".env") -Content $env_content

# 3. config/__init__.py
Create-File -Path (Join-Path $BaseDir "config\__init__.py") -Content "# Configuration package"

# 4. config/settings.py
$settings_content = @"
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

class Settings:
    # Azure OpenAI Settings
    AZURE_OPENAI_ENDPOINT: str = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    AZURE_OPENAI_KEY: str = os.getenv('AZURE_OPENAI_KEY', '')
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4')
    AZURE_OPENAI_API_VERSION: str = os.getenv('AZURE_OPENAI_API_VERSION', '2023-12-01-preview')
    
    # Azure Search Settings
    AZURE_SEARCH_ENDPOINT: str = os.getenv('AZURE_SEARCH_ENDPOINT', '')
    AZURE_SEARCH_KEY: str = os.getenv('AZURE_SEARCH_KEY', '')
    AZURE_SEARCH_INDEX: str = os.getenv('AZURE_SEARCH_INDEX', 'retail-index')
    
    # Application Settings
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    TIMEOUT_SECONDS: int = int(os.getenv('TIMEOUT_SECONDS', '30'))

settings = Settings()
"@
Create-File -Path (Join-Path $BaseDir "config\settings.py") -Content $settings_content

Write-Host "Basic structure created successfully!" -ForegroundColor Green
Write-Host "Run this script with additional parts to create all files:" -ForegroundColor Yellow
Write-Host "powershell -ExecutionPolicy Bypass -File create_multi_agent_structure.ps1" -ForegroundColor Cyan