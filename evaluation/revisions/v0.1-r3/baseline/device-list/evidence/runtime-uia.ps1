$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class R3DeviceListWin32 {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
  [DllImport("user32.dll")] public static extern uint GetDpiForWindow(IntPtr hWnd);
  [DllImport("user32.dll", SetLastError=true)] public static extern int GetWindowLong(IntPtr hWnd, int nIndex);
  [DllImport("user32.dll", SetLastError=true)] public static extern bool AdjustWindowRectExForDpi(ref RECT r, uint style, bool menu, uint exStyle, uint dpi);
  [DllImport("user32.dll", SetLastError=true)] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr after, int x, int y, int cx, int cy, uint flags);
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr hWnd, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr hWnd, ref POINT p);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@
$packet = 'Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r3\baseline\device-list'
$exe = Join-Path $packet 'project\bin\x64\Debug\net9.0-windows10.0.22621.0\win-x64\LazyDesign.EvaluationApp.exe'
$log = Join-Path $packet 'evidence\runtime-uia.txt'
$png = Join-Path $packet 'evidence\runtime.png'
$out = [System.Collections.Generic.List[string]]::new()
function L([string]$s) { $out.Add($s); Write-Output $s }
function ById($root,[string]$id) {
  $c=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::AutomationIdProperty,$id)
  $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants,$c)
}
function AllByType($root,$type) {
  $c=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty,$type)
  $root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$c)
}
function ByTypeName($root,$type,[string]$name) {
  $tc=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty,$type)
  $nc=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty,$name)
  $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.AndCondition]::new($tc,$nc))
}
function ResizeClient([IntPtr]$hwnd,[int]$wDip,[int]$hDip) {
  $dpi=[R3DeviceListWin32]::GetDpiForWindow($hwnd)
  $cw=[int][Math]::Round($wDip*$dpi/96.0);$ch=[int][Math]::Round($hDip*$dpi/96.0)
  $r=[R3DeviceListWin32+RECT]::new();$r.Right=$cw;$r.Bottom=$ch
  $s=[uint32][R3DeviceListWin32]::GetWindowLong($hwnd,-16);$e=[uint32][R3DeviceListWin32]::GetWindowLong($hwnd,-20)
  [R3DeviceListWin32]::AdjustWindowRectExForDpi([ref]$r,$s,$false,$e,$dpi)|Out-Null
  [R3DeviceListWin32]::SetWindowPos($hwnd,[IntPtr]::Zero,80,80,$r.Right-$r.Left,$r.Bottom-$r.Top,0x0040)|Out-Null
  Start-Sleep -Milliseconds 650
}
function InvokeElement($e) {
  $p=[System.Windows.Automation.InvokePattern]$e.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
  $p.Invoke()
}
function HasHangul([string]$s) {
  foreach($ch in $s.ToCharArray()) { $n=[int][char]$ch; if($n -ge 0xAC00 -and $n -le 0xD7A3){ return $true } }
  return $false
}
L 'METHOD: Launch frozen r3 baseline device-list executable; verify 520-DIP layout, long fixtures, single selection and Remove state, keyboard traversal, CommandBar overflow at 300 DIP, empty-state transition, and capture a screenshot.'
L 'COMMAND: powershell.exe -File evaluation/.runs/v2/v0.1-r3/baseline/device-list/evidence/runtime-uia.ps1'
$p=Start-Process -FilePath $exe -PassThru
try {
  $w=$null
  for($i=0;$i -lt 60 -and -not $w;$i++){
    Start-Sleep -Milliseconds 200;$p.Refresh()
    if($p.HasExited){throw "app exited early: $($p.ExitCode)"}
    if($p.MainWindowHandle -ne 0){$w=[System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)}
  }
  if(-not $w){throw 'top-level window not found'}
  $hwnd=[IntPtr]$p.MainWindowHandle;[R3DeviceListWin32]::SetForegroundWindow($hwnd)|Out-Null
  ResizeClient $hwnd 520 720
  $dpi=[R3DeviceListWin32]::GetDpiForWindow($hwnd)
  $cr=[R3DeviceListWin32+RECT]::new();[R3DeviceListWin32]::GetClientRect($hwnd,[ref]$cr)|Out-Null
  $pt=[R3DeviceListWin32+POINT]::new();[R3DeviceListWin32]::ClientToScreen($hwnd,[ref]$pt)|Out-Null
  $dip=[Math]::Round(($cr.Right-$cr.Left)*96.0/$dpi,2)
  L "RUNTIME: launched=yes pid=$($p.Id) window='$($w.Current.Name)' dpi=$dpi client_px=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top) client_width_dip=$dip"
  $refresh=ById $w 'RefreshButton';$add=ById $w 'AddButton';$remove=ById $w 'RemoveButton';$list=ById $w 'DeviceListView'
  if(-not $refresh -or -not $add -or -not $remove -or -not $list){throw 'required controls not found'}
  L "CONTROLS: refresh=True add=True remove=True remove_initial_enabled=$($remove.Current.IsEnabled) list=True"
  $texts=AllByType $w ([System.Windows.Automation.ControlType]::Text)
  $names=@($texts|ForEach-Object{$_.Current.Name}|Where-Object{$_})
  $english=$texts|Where-Object{$_.Current.Name -eq 'Portable conference-room presentation receiver'}|Select-Object -First 1
  $hangul=@($texts|Where-Object{(HasHangul $_.Current.Name) -and $_.Current.Name.Length -ge 10})
  $korean=$hangul|Sort-Object {$_.Current.Name.Length} -Descending|Select-Object -First 1
  L "TEXTS: $($names -join ' | ')"
  L "LONG_CONTENT: english_present=$([bool]$english) hangul_long_count=$($hangul.Count) longest_hangul='$($korean.Current.Name)'"
  $left=$pt.X;$right=$pt.X+($cr.Right-$cr.Left);$inside=$true
  foreach($e in @($refresh,$add,$remove,$list,$english,$korean)){
    if($e){$b=$e.Current.BoundingRectangle;if($b.Width -gt 0){$ok=($b.Left -ge $left -and $b.Right -le $right);if(-not $ok){$inside=$false};L "BOUNDS: id='$($e.Current.AutomationId)' name='$($e.Current.Name)' left=$([Math]::Round($b.Left,1)) right=$([Math]::Round($b.Right,1)) within_horizontal=$ok"}}
  }
  L "CONTENT_WIDTH_RESULT: client_width_dip=$dip all_observed_horizontal_bounds_inside=$inside"
  $items=AllByType $list ([System.Windows.Automation.ControlType]::ListItem)
  L "LIST_INITIAL: item_count=$($items.Count) remove_enabled=$($remove.Current.IsEnabled) names=$(@($items|ForEach-Object{$_.Current.Name}) -join '|')"
  if($items.Count -lt 1){throw 'no list items found'}
  $first=$items[0];$sp=[System.Windows.Automation.SelectionItemPattern]$first.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern);$sp.Select();Start-Sleep -Milliseconds 300
  $remove=ById $w 'RemoveButton';L "LIST_SELECTION: selected=$($sp.Current.IsSelected) remove_enabled_after_selection=$($remove.Current.IsEnabled)"
  [R3DeviceListWin32]::SetForegroundWindow($hwnd)|Out-Null;$refresh.SetFocus();Start-Sleep -Milliseconds 100
  $seq=@();1..4|ForEach-Object{[System.Windows.Forms.SendKeys]::SendWait('{TAB}');Start-Sleep -Milliseconds 170;$f=[System.Windows.Automation.AutomationElement]::FocusedElement;$seq += "$($f.Current.ControlType.ProgrammaticName):$($f.Current.AutomationId):$($f.Current.Name)"}
  L "KEYBOARD_TAB_SEQUENCE: $($seq -join ' -> ')"
  $bmp=[System.Drawing.Bitmap]::new($cr.Right-$cr.Left,$cr.Bottom-$cr.Top);$g=[System.Drawing.Graphics]::FromImage($bmp);$g.CopyFromScreen($pt.X,$pt.Y,0,0,$bmp.Size);$bmp.Save($png,[System.Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$bmp.Dispose();L "SCREENSHOT: path=evidence/runtime.png size=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top)"
  ResizeClient $hwnd 300 720
  $buttons=AllByType $w ([System.Windows.Automation.ControlType]::Button)
  $summary=@($buttons|ForEach-Object{"$($_.Current.AutomationId):$($_.Current.Name):enabled=$($_.Current.IsEnabled)"})
  $more=$buttons|Where-Object{$_.Current.AutomationId -match 'More|Overflow' -or $_.Current.Name -eq 'More'}|Select-Object -First 1
  $opened=$false;$overflow=@()
  if($more){try{InvokeElement $more;Start-Sleep -Milliseconds 350;$opened=$true;$root=[System.Windows.Automation.AutomationElement]::RootElement;$pc=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ProcessIdProperty,$p.Id);$proc=$root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$pc);$overflow=@($proc|Where-Object{$_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -or $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::MenuItem}|ForEach-Object{$_.Current.Name}|Where-Object{$_})}catch{}}
  L "COMMANDBAR_NARROW: width_dip=300 buttons=$($summary -join '|') more_present=$([bool]$more) overflow_opened=$opened overflow_items=$($overflow -join '|')"
  ResizeClient $hwnd 520 720
  for($i=0;$i -lt 6;$i++){
    $list=ById $w 'DeviceListView';if(-not $list){break};$items=AllByType $list ([System.Windows.Automation.ControlType]::ListItem);if($items.Count -eq 0){break};$item=$items[0];$sel=[System.Windows.Automation.SelectionItemPattern]$item.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern);$sel.Select();Start-Sleep -Milliseconds 120;$remove=ById $w 'RemoveButton';if(-not $remove.Current.IsEnabled){throw 'Remove not enabled after selection'};InvokeElement $remove;Start-Sleep -Milliseconds 220
  }
  $empty=ByTypeName $w ([System.Windows.Automation.ControlType]::Text) 'No devices';$list2=ById $w 'DeviceListView';$remaining=0;if($list2){$remaining=(AllByType $list2 ([System.Windows.Automation.ControlType]::ListItem)).Count};$visible=$false;if($empty){$visible=-not $empty.Current.IsOffscreen}
  L "EMPTY_STATE: remaining_items=$remaining no_devices_present=$([bool]$empty) no_devices_visible=$visible"
  L 'RESULT: runtime UI Automation sequence completed without script exception.'
}
catch{L "ERROR: $($_.Exception.Message)";throw}
finally{$out|Set-Content -Path $log -Encoding UTF8;if($p -and -not $p.HasExited){$p.CloseMainWindow()|Out-Null;Start-Sleep -Milliseconds 350;if(-not $p.HasExited){Stop-Process -Id $p.Id -Force}}}
