#!/usr/bin/env pwsh
# Install go-teaching-skills to Cursor user skills directory

$skillsDir = "$env:USERPROFILE\.cursor\skills"
$targetDir = "$skillsDir\go-teaching-skills"
$repoUrl   = "https://github.com/goss-rs/skills.git"

if (Test-Path $targetDir) {
    Write-Host "go-teaching-skills already installed at $targetDir"
    Write-Host "Pulling latest changes..."
    git -C $targetDir pull
} else {
    New-Item -ItemType Directory -Force $skillsDir | Out-Null
    Write-Host "Cloning $repoUrl -> $targetDir"
    git clone $repoUrl $targetDir
}

Write-Host ""
Write-Host "Done. Skills available in all Cursor projects."
Write-Host "To sync the go-lesson-plan knowledge corpus, run from your Go teaching repo:"
Write-Host "  python .cursor\skills\go-teaching-skills\go-lesson-plan\scripts\sync_skill_knowledge.py"
