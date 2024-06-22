; -- NSIS script for FastAPI application --

!define APPNAME "MyFastAPIApp"
!define APPVERSION "1.0"
!define INSTALLDIR "$PROGRAMFILES64\${APPNAME}"

; Include Modern UI
!include "MUI2.nsh"
!include "LogicLib.nsh"

; General
Name "${APPNAME}"
OutFile "MyFastAPIAppSetup.exe"
InstallDir "${INSTALLDIR}"
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Custom colors
!define MUI_PAGE_BGCOLOR "FFFFFF"
!define MUI_BGCOLOR "FFFFFF"

; Welcome page
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\win.bmp"
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${APPNAME} ${APPVERSION} Setup"
!define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ${APPNAME} ${APPVERSION}.$\r$\n$\r$\nClick Next to continue."

; Custom variables
Var AgentType
Var Dialog
Var Label
Var RadioStore
Var RadioProcess
Var RadioBoth

; Pages
!insertmacro MUI_PAGE_WELCOME
Page custom AgentTypePage AgentTypeLeave
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Language
!insertmacro MUI_LANGUAGE "English"

; Custom page function
Function AgentTypePage
  !insertmacro MUI_HEADER_TEXT "Agent Type Selection" "Choose your preferred agent type"
  nsDialogs::Create 1018
  Pop $Dialog

  ${NSD_CreateLabel} 0 0 100% 20u "Please select your preferred agent type:"
  Pop $Label
  SendMessage $Label ${WM_SETFONT} $mui.Header.Text.Font 0

  ${NSD_CreateRadioButton} 10 30 80% 15u "Store Agent (S)"
  Pop $RadioStore
  ${NSD_CreateRadioButton} 10 50 80% 15u "Process Agent (P)"
  Pop $RadioProcess
  ${NSD_CreateRadioButton} 10 70 80% 15u "Both (B)"
  Pop $RadioBoth

  nsDialogs::Show
FunctionEnd

Function AgentTypeLeave
  ${NSD_GetState} $RadioStore $0
  ${If} $0 == ${BST_CHECKED}
    StrCpy $AgentType "S"
  ${EndIf}
  ${NSD_GetState} $RadioProcess $0
  ${If} $0 == ${BST_CHECKED}
    StrCpy $AgentType "P"
  ${EndIf}
  ${NSD_GetState} $RadioBoth $0
  ${If} $0 == ${BST_CHECKED}
    StrCpy $AgentType "B"
  ${EndIf}
FunctionEnd

; Function to check if Python 3.12.4 is installed
Function CheckPython
  ExecWait 'cmd /c python --version' $0
  ${If} $0 != 0
    Goto InstallPython
  ${Else}
    ReadRegStr $0 HKLM "SOFTWARE\Python\PythonCore\3.12\InstallPath" ""
    StrCmp $0 "" InstallPython
  ${EndIf}
  Return

  InstallPython:
    ; Install Python 3.12.4
    File /oname=$TEMP\python-3.12.4-amd64.exe "python-3.12.4-amd64.exe"
    ExecWait '$TEMP\python-3.12.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1'
    Delete $TEMP\python-3.12.4-amd64.exe
FunctionEnd

Section "MainSection" SEC01
  ; Check for Python and install if necessary
  Call CheckPython

  SetOutPath "$INSTDIR"
  File "app.py"
  File "requirements.txt"
  File "start.bat"
  File ".env"

  ; Write agent type to a file
  FileOpen $0 "$INSTDIR\agent_type.txt" w
  FileWrite $0 $AgentType
  FileClose $0

  ; Install Python dependencies
  ExecWait 'cmd /c pip install -r "$INSTDIR\requirements.txt"'

  ; Create a shortcut in the Start Menu
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\start.bat"

  ; Create a shortcut on the desktop
  CreateShortcut "$DESKTOP\${APPNAME}.lnk" \quiet "$INSTDIR\start.bat"

  ; Uninstall information
  WriteUninstaller "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${APPVERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "Your Company Name"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\app.py"
  Delete "$INSTDIR\requirements.txt"
  Delete "$INSTDIR\start.bat"
  Delete "$INSTDIR\.env"
  Delete "$INSTDIR\agent_type.txt"
  Delete "$INSTDIR\uninstall.exe"
  Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
  Delete "$DESKTOP\${APPNAME}.lnk"
  RMDir "$SMPROGRAMS\${APPNAME}"
  RMDir "$INSTDIR"

  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd