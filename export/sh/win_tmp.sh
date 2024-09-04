#!/bin/bash

# PowerShell コマンドを使って %TEMP% の値を取得
readonly WINDOWS_TEMP=$(powershell.exe -Command '[System.IO.Path]::GetTempPath()' | tr -d '\r')

# Windows パスを WSL パスに変換
readonly WSL_TEMP=$(wslpath "$WINDOWS_TEMP")

echo $WSL_TEMP
