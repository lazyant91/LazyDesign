$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class EvalWin32DeviceList {
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

$packet = 'Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r2\baseline\device-list'
$exe = Join-Path $packet 'project\bin\x64\Debug\net9.0-windows10.0.22621.0\win-x64\LazyDesign.EvaluationApp.exe'
$log = Join-Path $packet 'evidence\runtime-uia.txt'
$png = Join-Path $packet 'evidence\runtime.png'
$out = [System.Collections.Generic.List[string]]::new()
function L([string]$s) { $out.Add($s); Write-Output $s }
function ById($root, [string]$id) {
  $c = [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::AutomationIdProperty, $id)
  return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $c)
}
function ByTypeAndName($root, $type, [string]$name) {
  $tc = [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty, $type)
  $nc = [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty, $name)
  return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.AndCondition]::new($tc, $nc))
}
function AllByType($root, $type) {
  $c = [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty, $type)
  return $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $c)
}
function ResizeClient([IntPtr]$hwnd, [int]$widthDip, [int]$heightDip) {
  $dpi = [EvalWin32DeviceList]::GetDpiForWindow($hwnd)
  $cw = [int][Math]::Round($widthDip * $dpi / 96.0)
  $ch = [int][Math]::Round($heightDip * $dpi / 96.0)
  $r = [EvalWin32DeviceList+RECT]::new(); $r.Right=$cw; $r.Bottom=$ch
  $style=[uint32][EvalWin32DeviceList]::GetWindowLong($hwnd,-16)
  $ex=[uint32][EvalWin32DeviceList]::GetWindowLong($hwnd,-20)
  [EvalWin32DeviceList]::AdjustWindowRectExForDpi([ref]$r,$style,$false,$ex,$dpi) | Out-Null
  [EvalWin32DeviceList]::SetWindowPos($hwnd,[IntPtr]::Zero,80,80,$r.Right-$r.Left,$r.Bottom-$r.Top,0x0040) | Out-Null
  Start-Sleep -Milliseconds 700
}

L 'METHOD: Launch frozen v0.1-r2 baseline device-list executable; exercise Windows UI Automation at a measured 520-DIP client width, ListView selection, Remove enabled state, keyboard traversal, dynamic CommandBar overflow under a narrower client width, and empty-state transition; capture a screenshot without changing OS settings.'
L 'COMMAND: powershell.exe -File evaluation/.runs/v2/v0.1-r2/baseline/device-list/evidence/runtime-uia.ps1'

$p = Start-Process -FilePath $exe -PassThru
try {
  $w=$null
  for($i=0;$i -lt 60 -and -not $w;$i++){
    Start-Sleep -Milliseconds 200
    $p.Refresh()
    if($p.HasExited){ throw "app exited before top-level window appeared; exit=$($p.ExitCode)" }
    if($p.MainWindowHandle -ne 0){ $w=[System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle) }
  }
  if(-not $w){ throw 'Top-level UIA window not found' }
  $hwnd=[IntPtr]$p.MainWindowHandle
  [EvalWin32DeviceList]::SetForegroundWindow($hwnd) | Out-Null
  ResizeClient $hwnd 520 720
  $dpi=[EvalWin32DeviceList]::GetDpiForWindow($hwnd)
  $cr=[EvalWin32DeviceList+RECT]::new(); [EvalWin32DeviceList]::GetClientRect($hwnd,[ref]$cr) | Out-Null
  $pt=[EvalWin32DeviceList+POINT]::new(); [EvalWin32DeviceList]::ClientToScreen($hwnd,[ref]$pt) | Out-Null
  $actualDip=[Math]::Round(($cr.Right-$cr.Left)*96.0/$dpi,2)
  L "RUNTIME: launched=yes pid=$($p.Id) window='$($w.Current.Name)' dpi=$dpi client_px=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top) client_width_dip=$actualDip"

  $refresh=ByTypeAndName $w ([System.Windows.Automation.ControlType]::Button) 'Refresh'
  $add=ByTypeAndName $w ([System.Windows.Automation.ControlType]::Button) 'Add device'
  $remove=ByTypeAndName $w ([System.Windows.Automation.ControlType]::Button) 'Remove'
  $list=ById $w 'DeviceList'
  if(-not $refresh){ throw 'Refresh command not found' }
  if(-not $add){ throw 'Add device command not found' }
  if(-not $remove){ throw 'Remove command not found' }
  if(-not $list){ throw 'DeviceList not found' }
  L "CONTROLS: refresh=True add=True remove=True remove_initial_enabled=$($remove.Current.IsEnabled) list=True"

  $texts=AllByType $w ([System.Windows.Automation.ControlType]::Text)
  $textNames=@($texts | ForEach-Object {$_.Current.Name} | Where-Object {$_})
  L "TEXTS: $($textNames -join ' | ')"
  $english=$texts | Where-Object {$_.Current.Name -eq 'Portable conference-room presentation receiver'} | Select-Object -First 1
  $nonAscii=@($texts | Where-Object {$_.Current.Name -match '[^\x00-\x7F]' -and $_.Current.Name.Length -ge 10})
  $korean=$nonAscii | Sort-Object {$_.Current.Name.Length} -Descending | Select-Object -First 1
  L "LONG_CONTENT_DISCOVERY: english_present=$([bool]$english) non_ascii_long_count=$($nonAscii.Count) longest_non_ascii='$($korean.Current.Name)'"

  $clientL=$pt.X; $clientR=$pt.X+($cr.Right-$cr.Left); $allInside=$true
  foreach($e in @($refresh,$add,$remove,$list,$english,$korean)){
    if($e){
      $b=$e.Current.BoundingRectangle
      if($b.Width -gt 0){
        $inside=($b.Left -ge $clientL -and $b.Right -le $clientR)
        if(-not $inside){$allInside=$false}
        L "BOUNDS: id='$($e.Current.AutomationId)' name='$($e.Current.Name)' type='$($e.Current.ControlType.ProgrammaticName)' left=$([Math]::Round($b.Left,1)) right=$([Math]::Round($b.Right,1)) within_horizontal=$inside"
      }
    }
  }
  L "CONTENT_WIDTH_RESULT: client_width_dip=$actualDip all_observed_horizontal_bounds_inside=$allInside"

  $items=AllByType $list ([System.Windows.Automation.ControlType]::ListItem)
  L "LIST_INITIAL: item_count=$($items.Count) names=$(@($items | ForEach-Object {$_.Current.Name}) -join '|') remove_enabled=$($remove.Current.IsEnabled)"
  if($items.Count -lt 1){ throw 'No ListView items found' }
  $first=$items[0]
  $sel=[System.Windows.Automation.SelectionItemPattern]$first.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
  $sel.Select(); Start-Sleep -Milliseconds 300
  $remove=ByTypeAndName $w ([System.Windows.Automation.ControlType]::Button) 'Remove'
  L "LIST_SELECTION: selected=$($sel.Current.IsSelected) selected_name='$($first.Current.Name)' remove_enabled_after_selection=$($remove.Current.IsEnabled)"

  [EvalWin32DeviceList]::SetForegroundWindow($hwnd) | Out-Null
  $refresh.SetFocus(); Start-Sleep -Milliseconds 100
  $seq=@()
  1..4 | ForEach-Object {
    [System.Windows.Forms.SendKeys]::SendWait('{TAB}'); Start-Sleep -Milliseconds 180
    $f=[System.Windows.Automation.AutomationElement]::FocusedElement
    $seq += "$($f.Current.ControlType.ProgrammaticName):$($f.Current.AutomationId):$($f.Current.Name)"
  }
  L "KEYBOARD_TAB_SEQUENCE: $($seq -join ' -> ')"

  $bmp=[System.Drawing.Bitmap]::new($cr.Right-$cr.Left,$cr.Bottom-$cr.Top)
  $g=[System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($pt.X,$pt.Y,0,0,$bmp.Size)
  $bmp.Save($png,[System.Drawing.Imaging.ImageFormat]::Png)
  $sum=0; $count=0; $colors=@{}
  for($y=10;$y -lt $bmp.Height;$y+=20){ for($x=10;$x -lt $bmp.Width;$x+=20){ $c=$bmp.GetPixel($x,$y); $key="$($c.R),$($c.G),$($c.B)"; if(-not $colors.ContainsKey($key)){$colors[$key]=0}; $colors[$key]++; $sum += $c.R+$c.G+$c.B; $count+=3 } }
  $avg=if($count){[Math]::Round($sum/$count,1)}else{0}
  $g.Dispose(); $bmp.Dispose()
  L "SCREENSHOT: path=evidence/runtime.png size=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top) sampled_unique_colors=$($colors.Count) avg_rgb_component=$avg"

  ResizeClient $hwnd 300 720
  $buttons=AllByType $w ([System.Windows.Automation.ControlType]::Button)
  $buttonSummary=@($buttons | ForEach-Object {"$($_.Current.AutomationId):$($_.Current.Name):enabled=$($_.Current.IsEnabled)"})
  $more=$buttons | Where-Object {$_.Current.AutomationId -match 'More|Overflow' -or $_.Current.Name -match '^More$|overflow'} | Select-Object -First 1
  $overflowOpened=$false; $overflowItems=@()
  if($more){
    try {
      $inv=[System.Windows.Automation.InvokePattern]$more.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern); $inv.Invoke(); Start-Sleep -Milliseconds 350
      $overflowOpened=$true
      $root=[System.Windows.Automation.AutomationElement]::RootElement
      $procCond=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ProcessIdProperty,$p.Id)
      $allProc=$root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$procCond)
      $overflowItems=@($allProc | Where-Object {$_.Current.ControlType -eq [System.Windows.Automation.ControlType]::MenuItem -or $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button} | ForEach-Object {$_.Current.Name} | Where-Object {$_})
    } catch {}
  }
  L "COMMANDBAR_NARROW: width_dip=300 buttons=$($buttonSummary -join '|') more_present=$([bool]$more) overflow_opened=$overflowOpened overflow_items=$($overflowItems -join '|')"

  ResizeClient $hwnd 520 720
  for($iteration=0;$iteration -lt 6;$iteration++){
    $list=ById $w 'DeviceList'
    if(-not $list){ break }
    $items=AllByType $list ([System.Windows.Automation.ControlType]::ListItem)
    if($items.Count -eq 0){ break }
    $first=$items[0]
    $sp=[System.Windows.Automation.SelectionItemPattern]$first.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
    $sp.Select(); Start-Sleep -Milliseconds 150
    $remove=ByTypeAndName $w ([System.Windows.Automation.ControlType]::Button) 'Remove'
    if(-not $remove -or -not $remove.Current.IsEnabled){ throw 'Remove was not enabled after selecting an item' }
    $ip=[System.Windows.Automation.InvokePattern]$remove.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
    $ip.Invoke(); Start-Sleep -Milliseconds 250
  }
  $empty=ByTypeAndName $w ([System.Windows.Automation.ControlType]::Text) 'No devices'
  $listAfter=ById $w 'DeviceList'
  $remaining=0
  if($listAfter){ $remaining=(AllByType $listAfter ([System.Windows.Automation.ControlType]::ListItem)).Count }
  $emptyVisible=$false; if($empty){$emptyVisible=-not $empty.Current.IsOffscreen}
  L "EMPTY_STATE: remaining_items=$remaining no_devices_present=$([bool]$empty) no_devices_visible=$emptyVisible"
  L 'RESULT: runtime UI Automation sequence completed without script exception.'
}
catch {
  L "ERROR: $($_.Exception.Message)"
  throw
}
finally {
  $out | Set-Content -Path $log -Encoding UTF8
  if($p -and -not $p.HasExited){
    $p.CloseMainWindow() | Out-Null; Start-Sleep -Milliseconds 400
    if(-not $p.HasExited){ Stop-Process -Id $p.Id -Force }
  }
}
