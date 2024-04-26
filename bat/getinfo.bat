@echo off
bcdedit /enum | findstr /i "path" | findstr ".efi" >nul && (set "__BIOS=UEFI") || (set "__BIOS=BIOS")
reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecureBoot\State -v UefiSecureBootEnabled | findstr "0x1" >nul && (set "__SECURE=ON") || (set "__SECURE=OFF")
reg query "HKLM\Hardware\Description\System\CentralProcessor\0" | findstr /i "x86" > NUL && set __CPU=x86 || set __CPU=x64
for /f %%i in ('wmic ComputerSystem get TotalPhysicalMemory ^| findstr /iv "TotalPhysicalMemory" ^| findstr /r /v "^$"') do (set _RAMKB=%%i)
FOR /F "usebackq" %%n IN (`powershell -NoP -NoL -C [math]::Round^(%_RAMKB%/^[Math]::Pow(1024^,3^)^)`) DO (SET "__RAM=%%nG")

rem end: print all
echo BIOS: %__BIOS% ^| SECURE: %__SECURE% ^| ARCH: %__CPU% ^| RAM: %__RAM%