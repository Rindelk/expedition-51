@echo off
title Stop Expedition 51 Server
echo [*] Terminating any running cloudflared tunnels and local servers...
taskkill /F /IM cloudflared.exe >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
echo [OK] Expedition 51 server and tunnel stopped cleanly.
timeout /t 2 >nul
