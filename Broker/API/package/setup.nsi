; -- NSIS script for FastAPI application --

!define APPNAME "MyFastAPIApp"
!define APPVERSION "1.0"
!define INSTALLDIR "$PROGRAMFILES${APPNAME}"

OutFile "MyFastAPIAppSetup.exe"
InstallDir "${INSTALLDIR}"

Page directory
Page instfiles

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  File "app.py"
  File "requirements.txt"
  File "start.bat"
  File ".env"

  ; Install Python dependencies
  ExecWait 'cmd /c pip install -r "$INSTDIR\requirements.txt"'

  ; Create a shortcut in the Startup folder
  CreateShortCut "$SMSTARTUP\MyFastAPIApp.lnk" "$INSTDIR\start.bat"

  ; Uninstall information
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\app.py"
  Delete "$INSTDIR\requirements.txt"
  Delete "$INSTDIR\start.bat"
  Delete "$INSTDIR\.env"
  Delete "$SMSTARTUP\MyFastAPIApp.lnk"
  Delete "$INSTDIR\uninstall.exe"
  RMDir "$INSTDIR"
SectionEnd