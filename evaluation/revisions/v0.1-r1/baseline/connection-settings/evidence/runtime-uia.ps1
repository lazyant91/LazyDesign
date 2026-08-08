$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class EvalWin32 {
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

$packet = 'Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r1\baseline\connection-settings'
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
  $and = [System.Windows.Automation.AndCondition]::new($tc, $nc)
  return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $and)
}
function FirstByType($root, $type) {
  $tc = [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty, $type)
  return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $tc)
}
function FirstTogglePattern($root) {
  $all = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
  foreach ($e in $all) {
    try {
      $pattern = $null
      if ($e.TryGetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern, [ref]$pattern)) { return $e }
    } catch {}
  }
  return $null
}

L 'METHOD: Launch frozen v0.1-r1 baseline WinUI 3 executable; use Windows UI Automation for control discovery, keyboard traversal, TextBox validation, ComboBox expansion/selection, ToggleSwitch state change, Save Button invoke; resize only the app window to a measured 420-DIP client width; capture the client screenshot without changing OS settings.'
L 'COMMAND: powershell.exe -File evaluation/.runs/v2/v0.1-r1/baseline/connection-settings/evidence/runtime-uia.ps1'

$p = Start-Process -FilePath $exe -PassThru
try {
  $w = $null
  for ($i = 0; $i -lt 60 -and -not $w; $i++) {
    Start-Sleep -Milliseconds 200
    $p.Refresh()
    if ($p.HasExited) { throw "app exited before top-level window appeared; exit=$($p.ExitCode)" }
    if ($p.MainWindowHandle -ne 0) { $w = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle) }
  }
  if (-not $w) { throw 'Top-level UIA window not found from Process.MainWindowHandle' }

  $pc = [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ProcessIdProperty, $p.Id)
  $hwnd = [IntPtr]$p.MainWindowHandle
  [EvalWin32]::SetForegroundWindow($hwnd) | Out-Null
  $dpi = [EvalWin32]::GetDpiForWindow($hwnd)
  $cw = [int][Math]::Round(420 * $dpi / 96.0)
  $ch = [int][Math]::Round(700 * $dpi / 96.0)
  $r = [EvalWin32+RECT]::new(); $r.Right = $cw; $r.Bottom = $ch
  $style = [uint32][EvalWin32]::GetWindowLong($hwnd, -16)
  $ex = [uint32][EvalWin32]::GetWindowLong($hwnd, -20)
  [EvalWin32]::AdjustWindowRectExForDpi([ref]$r, $style, $false, $ex, $dpi) | Out-Null
  [EvalWin32]::SetWindowPos($hwnd, [IntPtr]::Zero, 80, 80, $r.Right-$r.Left, $r.Bottom-$r.Top, 0x0040) | Out-Null
  Start-Sleep -Milliseconds 700

  $cr = [EvalWin32+RECT]::new(); [EvalWin32]::GetClientRect($hwnd, [ref]$cr) | Out-Null
  $pt = [EvalWin32+POINT]::new(); [EvalWin32]::ClientToScreen($hwnd, [ref]$pt) | Out-Null
  $actualDip = [Math]::Round(($cr.Right-$cr.Left) * 96.0 / $dpi, 2)
  L "RUNTIME: launched=yes pid=$($p.Id) window='$($w.Current.Name)' dpi=$dpi client_px=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top) client_width_dip=$actualDip"

  $tb = ById $w 'ConnectionNameTextBox'
  $validation = ById $w 'NameValidationMessage'
  $combo = FirstByType $w ([System.Windows.Automation.ControlType]::ComboBox)
  $toggle = FirstTogglePattern $w
  $save = ByTypeAndName $w ([System.Windows.Automation.ControlType]::Button) '연결 설정 저장'
  if (-not $tb) { throw 'ConnectionNameTextBox not found' }
  if (-not $combo) { throw 'ComboBox not found' }
  if (-not $toggle) { throw 'ToggleSwitch/TogglePattern element not found' }
  if (-not $save) { throw 'Save Button not found by name' }
  L "CONTROLS: textbox=True textbox_name='$($tb.Current.Name)' combo=True combo_name='$($combo.Current.Name)' toggle=True toggle_name='$($toggle.Current.Name)' save=True save_name='$($save.Current.Name)' validation_initial=$([bool]$validation)"

  $textType = [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Text)
  $texts = $w.FindAll([System.Windows.Automation.TreeScope]::Descendants, $textType)
  $textNames = @($texts | ForEach-Object { $_.Current.Name } | Where-Object { $_ })
  L "TEXTS: $($textNames -join ' | ')"

  $clientL = $pt.X; $clientR = $pt.X + ($cr.Right-$cr.Left)
  $allInside = $true
  foreach ($e in @($tb, $combo, $toggle, $save)) {
    $b = $e.Current.BoundingRectangle
    $inside = ($b.Left -ge $clientL -and $b.Right -le $clientR)
    if (-not $inside) { $allInside = $false }
    L "BOUNDS: id='$($e.Current.AutomationId)' name='$($e.Current.Name)' type='$($e.Current.ControlType.ProgrammaticName)' left=$([Math]::Round($b.Left,1)) right=$([Math]::Round($b.Right,1)) client_left=$clientL client_right=$clientR within_horizontal=$inside"
  }
  foreach ($e in $texts) {
    if ($e.Current.Name) {
      $b = $e.Current.BoundingRectangle
      if ($b.Width -gt 0) {
        $inside = ($b.Left -ge $clientL -and $b.Right -le $clientR)
        if (-not $inside) { $allInside = $false }
        L "TEXT_BOUND: name='$($e.Current.Name)' left=$([Math]::Round($b.Left,1)) right=$([Math]::Round($b.Right,1)) within_horizontal=$inside"
      }
    }
  }
  L "CONTENT_WIDTH_RESULT: client_width_dip=$actualDip all_observed_horizontal_bounds_inside=$allInside"

  $vp = [System.Windows.Automation.ValuePattern]$tb.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
  $vp.SetValue('Office Device'); Start-Sleep -Milliseconds 250
  $validationNonEmpty = ById $w 'NameValidationMessage'
  $nonEmptyVisible = $false
  if ($validationNonEmpty) { $nonEmptyVisible = -not $validationNonEmpty.Current.IsOffscreen }
  L "TEXTBOX_VALIDATION: nonempty_present=$([bool]$validationNonEmpty) nonempty_visible=$nonEmptyVisible"
  $vp.SetValue(''); Start-Sleep -Milliseconds 250
  $validationEmpty = ById $w 'NameValidationMessage'
  $emptyVisible = $false
  if ($validationEmpty) { $emptyVisible = -not $validationEmpty.Current.IsOffscreen }
  L "TEXTBOX_VALIDATION: empty_present=$([bool]$validationEmpty) empty_visible=$emptyVisible"

  $ep = [System.Windows.Automation.ExpandCollapsePattern]$combo.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
  $ep.Expand(); Start-Sleep -Milliseconds 350
  $state = $ep.Current.ExpandCollapseState
  $li = [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::ListItem)
  $and = [System.Windows.Automation.AndCondition]::new($pc, $li)
  $items = [System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Descendants, $and)
  $names = @($items | ForEach-Object { $_.Current.Name } | Where-Object { $_ })
  $target = $null
  foreach ($item in $items) { if ($item.Current.Name -eq 'Bluetooth') { $target = $item; break } }
  $selected = $false
  if ($target) {
    $sip = [System.Windows.Automation.SelectionItemPattern]$target.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
    $sip.Select(); Start-Sleep -Milliseconds 200
    $selected = $sip.Current.IsSelected
  }
  L "COMBOBOX: expanded_state=$state item_count=$($items.Count) items=$($names -join '|') bluetooth_selected=$selected"

  $tp = [System.Windows.Automation.TogglePattern]$toggle.GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern)
  $before = $tp.Current.ToggleState; $tp.Toggle(); Start-Sleep -Milliseconds 200; $after = $tp.Current.ToggleState
  L "TOGGLE: before=$before after=$after"

  [EvalWin32]::SetForegroundWindow($hwnd) | Out-Null
  $tb.SetFocus(); Start-Sleep -Milliseconds 150
  $seq = @()
  1..3 | ForEach-Object {
    [System.Windows.Forms.SendKeys]::SendWait('{TAB}'); Start-Sleep -Milliseconds 200
    $f = [System.Windows.Automation.AutomationElement]::FocusedElement
    $seq += "$($f.Current.ControlType.ProgrammaticName):$($f.Current.AutomationId):$($f.Current.Name)"
  }
  L "KEYBOARD_TAB_SEQUENCE: $($seq -join ' -> ')"

  $vp.SetValue('')
  $save.SetFocus(); Start-Sleep -Milliseconds 100
  $inv = [System.Windows.Automation.InvokePattern]$save.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
  $inv.Invoke(); Start-Sleep -Milliseconds 250
  $focused = [System.Windows.Automation.AutomationElement]::FocusedElement
  $validationSave = ById $w 'NameValidationMessage'
  $saveVisible = $false
  if ($validationSave) { $saveVisible = -not $validationSave.Current.IsOffscreen }
  L "SAVE_INVOKE: invoked=yes focused_after='$($focused.Current.Name)' focused_id='$($focused.Current.AutomationId)' validation_visible=$saveVisible"

  $bmp = [System.Drawing.Bitmap]::new($cr.Right-$cr.Left, $cr.Bottom-$cr.Top)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($pt.X, $pt.Y, 0, 0, $bmp.Size)
  $bmp.Save($png, [System.Drawing.Imaging.ImageFormat]::Png)
  $colorCounts = @{}; $sum = 0; $count = 0
  for ($y=10; $y -lt $bmp.Height; $y+=20) {
    for ($x=10; $x -lt $bmp.Width; $x+=20) {
      $c=$bmp.GetPixel($x,$y); $key="$($c.R),$($c.G),$($c.B)"; if(-not $colorCounts.ContainsKey($key)){$colorCounts[$key]=0}; $colorCounts[$key]++; $sum += $c.R+$c.G+$c.B; $count += 3
    }
  }
  $avg = if($count){[Math]::Round($sum/$count,1)}else{0}
  $top = $colorCounts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 6
  $dominant = @($top | ForEach-Object { "$($_.Key):$($_.Value)" }) -join ';'
  $g.Dispose(); $bmp.Dispose()
  L "SCREENSHOT: path=evidence/runtime.png size=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top) sampled_unique_colors=$($colorCounts.Count) avg_rgb_component=$avg dominant=$dominant"
  L 'RESULT: runtime UI Automation sequence completed without script exception.'
}
catch {
  L "ERROR: $($_.Exception.Message)"
  throw
}
finally {
  $out | Set-Content -Path $log -Encoding UTF8
  if ($p -and -not $p.HasExited) {
    $p.CloseMainWindow() | Out-Null
    Start-Sleep -Milliseconds 400
    if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force }
  }
}
