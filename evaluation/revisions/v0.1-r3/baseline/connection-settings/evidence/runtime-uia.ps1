$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class R3StarterWin32 {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left,Top,Right,Bottom; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X,Y; }
  [DllImport("user32.dll")] public static extern uint GetDpiForWindow(IntPtr h);
  [DllImport("user32.dll", SetLastError=true)] public static extern int GetWindowLong(IntPtr h,int n);
  [DllImport("user32.dll", SetLastError=true)] public static extern bool AdjustWindowRectExForDpi(ref RECT r,uint s,bool m,uint e,uint d);
  [DllImport("user32.dll", SetLastError=true)] public static extern bool SetWindowPos(IntPtr h,IntPtr a,int x,int y,int cx,int cy,uint f);
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h,out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h,ref POINT p);
}
'@
$packet='Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r3\baseline\connection-settings'
$exe=Join-Path $packet 'project\bin\x64\Debug\net9.0-windows10.0.22621.0\win-x64\LazyDesign.EvaluationApp.exe'
$log=Join-Path $packet 'evidence\runtime-uia.txt'
$png=Join-Path $packet 'evidence\runtime.png'
$out=[Collections.Generic.List[string]]::new(); function L([string]$s){$out.Add($s);Write-Output $s}
function ByType($r,$t){$c=[Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::ControlTypeProperty,$t);return $r.FindAll([Windows.Automation.TreeScope]::Descendants,$c)}
L 'METHOD: Launch the frozen unchanged starter executable, resize client to 420 DIP, inspect UIA tree for required connection-settings controls/text, and capture the client. No source or OS setting is changed.'
L 'COMMAND: powershell.exe -File evaluation/.runs/v2/v0.1-r3/baseline/connection-settings/evidence/runtime-uia.ps1'
$p=Start-Process $exe -PassThru
try {
  $w=$null
  for($i=0;$i -lt 60 -and -not $w;$i++){Start-Sleep -Milliseconds 200;$p.Refresh();if($p.HasExited){throw "app exited early: $($p.ExitCode)"};if($p.MainWindowHandle -ne 0){$w=[Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)}}
  if(-not $w){throw 'top-level UIA window not found'}
  $h=[IntPtr]$p.MainWindowHandle;$dpi=[R3StarterWin32]::GetDpiForWindow($h);$cw=[int][Math]::Round(420*$dpi/96);$ch=[int][Math]::Round(700*$dpi/96)
  $r=[R3StarterWin32+RECT]::new();$r.Right=$cw;$r.Bottom=$ch;$s=[uint32][R3StarterWin32]::GetWindowLong($h,-16);$e=[uint32][R3StarterWin32]::GetWindowLong($h,-20);[R3StarterWin32]::AdjustWindowRectExForDpi([ref]$r,$s,$false,$e,$dpi)|Out-Null;[R3StarterWin32]::SetWindowPos($h,[IntPtr]::Zero,80,80,$r.Right-$r.Left,$r.Bottom-$r.Top,0x0040)|Out-Null;Start-Sleep -Milliseconds 500
  $ed=ByType $w ([Windows.Automation.ControlType]::Edit);$cb=ByType $w ([Windows.Automation.ControlType]::ComboBox);$btn=ByType $w ([Windows.Automation.ControlType]::Button);$txt=ByType $w ([Windows.Automation.ControlType]::Text)
  $names=@($txt|ForEach-Object{$_.Current.Name}|Where-Object{$_});$buttonNames=@($btn|ForEach-Object{$_.Current.Name}|Where-Object{$_})
  $scenarioControlsAbsent=($ed.Count -eq 0 -and $cb.Count -eq 0 -and $btn.Count -eq 0)
  L "RUNTIME: launched=yes pid=$($p.Id) window='$($w.Current.Name)' dpi=$dpi client_width_dip=$([Math]::Round($cw*96.0/$dpi,2))"
  L "SCENARIO_CONTROLS: textbox_count=$($ed.Count) combobox_count=$($cb.Count) button_count=$($btn.Count) all_required_interactive_controls_absent=$scenarioControlsAbsent"
  L "TEXTS: $($names -join ' | ')"
  $cr=[R3StarterWin32+RECT]::new();[R3StarterWin32]::GetClientRect($h,[ref]$cr)|Out-Null;$pt=[R3StarterWin32+POINT]::new();[R3StarterWin32]::ClientToScreen($h,[ref]$pt)|Out-Null
  $bmp=[Drawing.Bitmap]::new($cr.Right-$cr.Left,$cr.Bottom-$cr.Top);$g=[Drawing.Graphics]::FromImage($bmp);$g.CopyFromScreen($pt.X,$pt.Y,0,0,$bmp.Size);$bmp.Save($png,[Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$bmp.Dispose()
  L "SCREENSHOT: path=evidence/runtime.png size=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top)"
  L 'RESULT: starter runtime launched, but requested connection-settings scenario controls/content are absent.'
}
finally {$out|Set-Content $log -Encoding UTF8;if($p -and -not $p.HasExited){$p.CloseMainWindow()|Out-Null;Start-Sleep -Milliseconds 300;if(-not $p.HasExited){Stop-Process -Id $p.Id -Force}}}
