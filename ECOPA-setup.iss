[Setup]
AppName=ECOPA
AppVersion=1.0
AppPublisher=ECOPA
DefaultDirName={autopf}\ECOPA
DefaultGroupName=ECOPA
OutputDir=installer
OutputBaseFilename=ECOPA-Setup
Compression=lzma2
SolidCompression=yes
SetupIconFile=assets\icone.ico
UninstallDisplayIcon={app}\ECOPA.exe

[Files]
Source: "dist\ECOPA.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ECOPA"; Filename: "{app}\ECOPA.exe"
Name: "{commondesktop}\ECOPA"; Filename: "{app}\ECOPA.exe"

[Run]
Filename: "{app}\ECOPA.exe"; Description: "Iniciar ECOPA"; Flags: postinstall nowait
