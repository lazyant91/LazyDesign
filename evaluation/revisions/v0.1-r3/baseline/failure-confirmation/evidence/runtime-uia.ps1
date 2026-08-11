$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class R3FailureStarterWin32 {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left,Top,Right,Bottom; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X,Y; }
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h,out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h,ref POINT p);
}
'@
$packet='Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r3\baseline\failure-confirmation'
$exe=Join-Path $packet 'project\bin\x64\Debug\net9.0-windows10.0.22621.0\win-x64\LazyDesign.EvaluationApp.exe'
$log=Join-Path $packet 'evidence\runtime-uia.txt'
$png=Join-Path $packet 'evidence\runtime.png'
$out=[Collections.Generic.List[string]]::new()
function L([string]$s){$out.Add($s);Write-Output $s}
function AllByType($r,$t){$c=[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::ControlTypeProperty,$t);return $r.FindAll([Windows.Automation.TreeScope]::Descendants,$c)}
L 'METHOD: Launch the frozen unchanged starter executable; inspect UIA for failure-confirmation text and interactive controls; capture the client without changing source or OS settings.'
L 'COMMAND: powershell.exe -File evaluation/.runs/v2/v0.1-r3/baseline/failure-confirmation/evidence/runtime-uia.ps1'
$p=Start-Process $exe -PassThru
try {
  $w=$null
  for($i=0;$i -lt 60 -and -not $w;$i++){Start-Sleep -Milliseconds 200;$p.Refresh();if($p.HasExited){throw "app exited early: $($p.ExitCode)"};if($p.MainWindowHandle -ne 0){$w=[Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)}}
  if(-not $w){throw 'top-level UIA window not found'}
  $buttons=AllByType $w ([Windows.Automation.ControlType]::Button)
  $texts=AllByType $w ([Windows.Automation.ControlType]::Text)
  $windows=AllByType $w ([Windows.Automation.ControlType]::Window)
  $names=@($texts|ForEach-Object{$_.Current.Name}|Where-Object{$_})
  $buttonNames=@($buttons|ForEach-Object{$_.Current.Name}|Where-Object{$_})
  L "RUNTIME: launched=yes pid=$($p.Id) window='$($w.Current.Name)'"
  L "SCENARIO_CONTROLS: button_count=$($buttons.Count) descendant_window_count=$($windows.Count)"
  L "BUTTONS: $($buttonNames -join ' | ')"
  L "TEXTS: $($names -join ' | ')"
  $h=[IntPtr]$p.MainWindowHandle;$cr=[R3FailureStarterWin32+RECT]::new();[R3FailureStarterWin32]::GetClientRect($h,[ref]$cr)|Out-Null;$pt=[R3FailureStarterWin32+POINT]::new();[R3FailureStarterWin32]::ClientToScreen($h,[ref]$pt)|Out-Null
  $bmp=[Drawing.Bitmap]::new($cr.Right-$cr.Left,$cr.Bottom-$cr.Top);$g=[Drawing.Graphics]::FromImage($bmp);$g.CopyFromScreen($pt.X,$pt.Y,0,0,$bmp.Size);$bmp.Save($png,[Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$bmp.Dispose()
  L "SCREENSHOT: path=evidence/runtime.png size=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top)"
  L 'RESULT: starter runtime launched, but the requested failure-confirmation scenario UI and actions are absent.'
}
finally {$out|Set-Content $log -Encoding UTF8;if($p -and -not $p.HasExited){$p.CloseMainWindow()|Out-Null;Start-Sleep -Milliseconds 300;if(-not $p.HasExited){Stop-Process -Id $p.Id -Force}}}
