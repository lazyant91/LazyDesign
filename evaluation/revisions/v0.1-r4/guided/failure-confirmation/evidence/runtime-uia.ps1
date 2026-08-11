$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class R4FailureWin32 {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr hWnd, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr hWnd, ref POINT p);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@

$packet = 'Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r4\guided\failure-confirmation'
$exe = Join-Path $packet 'project\bin\x64\Debug\net9.0-windows10.0.22621.0\win-x64\LazyDesign.EvaluationApp.exe'
$log = Join-Path $packet 'evidence\runtime-uia.txt'
$png = Join-Path $packet 'evidence\runtime.png'
$out = [System.Collections.Generic.List[string]]::new()
function L([string]$s) { $out.Add($s); Write-Output $s }
function FromB64([string]$s) { [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($s)) }
function ById($root,[string]$id) {
  $c=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::AutomationIdProperty,$id)
  return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants,$c)
}
function ByTypeAndName($root,$type,[string]$name) {
  $tc=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty,$type)
  $nc=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty,$name)
  return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.AndCondition]::new($tc,$nc))
}
function AllByType($root,$type) {
  $c=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty,$type)
  return @($root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$c))
}
function TextNames($root) {
  return @(AllByType $root ([System.Windows.Automation.ControlType]::Text) | ForEach-Object {$_.Current.Name} | Where-Object {$_})
}
function IsVisible($e) { return ($e -and -not $e.Current.IsOffscreen) }
function InvokeElement($e) {
  if(-not $e){throw 'cannot invoke null element'}
  $p=$null
  if(-not $e.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern,[ref]$p)){throw "InvokePattern unavailable for '$($e.Current.Name)'"}
  ([System.Windows.Automation.InvokePattern]$p).Invoke()
}
function StartEvalApp {
  $proc=Start-Process -FilePath $exe -PassThru
  $win=$null
  for($i=0;$i -lt 60 -and -not $win;$i++){
    Start-Sleep -Milliseconds 200; $proc.Refresh()
    if($proc.HasExited){throw "app exited before window; exit=$($proc.ExitCode)"}
    if($proc.MainWindowHandle -ne 0){$win=[System.Windows.Automation.AutomationElement]::FromHandle($proc.MainWindowHandle)}
  }
  if(-not $win){throw 'top-level UIA window not found'}
  [R4FailureWin32]::SetForegroundWindow([IntPtr]$proc.MainWindowHandle)|Out-Null
  return @($proc,$win)
}
function StopEvalApp($proc) {
  if($proc -and -not $proc.HasExited){$proc.CloseMainWindow()|Out-Null;Start-Sleep -Milliseconds 350;if(-not $proc.HasExited){Stop-Process -Id $proc.Id -Force}}
}

$requiredMessage=FromB64 '7J6l7LmY6rCAIOydkeuLte2VmOyngCDslYrslZjsirXri4jri6QuIOyepey5mOqwgCDsvJzsoLgg7J6I6rOgIOuPmeydvO2VnCDrhKTtirjsm4ztgazsl5Ag7Jew6rKw65CY7Ja0IOyeiOuKlOyngCDtmZXsnbjtlZwg7ZuEIOuLpOyLnCDsi5zrj4TtlZjshLjsmpQu'
$retryName=FromB64 '7J6l7LmYIOyXsOqysCDri6Tsi5wg7Iuc64+E'
$removeName=FromB64 '7ZqM7J2Y7IukIOuUlOyKpO2UjOugiOydtCDsoIDsnqXrkJwg7J6l7LmYIOygnOqxsA=='
$deviceName=FromB64 '7ZqM7J2Y7IukIOuUlOyKpO2UjOugiOydtA=='

L 'METHOD: Launch frozen v0.1-r4 guided failure-confirmation executable; exercise InfoBar Retry and dismissal plus ContentDialog default/Cancel/Remove actions, keyboard traversal, and focus return with Windows UI Automation; capture a runtime screenshot without changing OS settings.'
L 'COMMAND: powershell.exe -File evaluation/.runs/v2/v0.1-r4/guided/failure-confirmation/evidence/runtime-uia.ps1'
$p1=$null; $p2=$null
try {
  $pair=StartEvalApp; $p1=$pair[0]; $w1=$pair[1]
  $info=ById $w1 'ConnectionErrorInfoBar'
  $retry=ByTypeAndName $w1 ([System.Windows.Automation.ControlType]::Button) $retryName
  $remove=ByTypeAndName $w1 ([System.Windows.Automation.ControlType]::Button) $removeName
  if(-not $info -or -not $retry -or -not $remove){throw 'required initial controls not found'}
  $texts=TextNames $w1
  $buttons=AllByType $w1 ([System.Windows.Automation.ControlType]::Button)
  L "RUNTIME1: launched=yes pid=$($p1.Id) window='$($w1.Current.Name)' info_visible=$(IsVisible $info) retry_present=$([bool]$retry) remove_present=$([bool]$remove) required_message_present=$($texts -contains $requiredMessage)"
  L "BUTTONS_INITIAL: $(@($buttons|ForEach-Object{"$($_.Current.AutomationId):$($_.Current.Name):enabled=$($_.Current.IsEnabled)"}) -join '|')"
  $retry.SetFocus(); Start-Sleep -Milliseconds 100
  $seq=@(); 1..2|ForEach-Object{[System.Windows.Forms.SendKeys]::SendWait('{TAB}');Start-Sleep -Milliseconds 180;$f=[System.Windows.Automation.AutomationElement]::FocusedElement;$seq += "$($f.Current.ControlType.ProgrammaticName):$($f.Current.AutomationId):$($f.Current.Name)"}
  L "KEYBOARD_TAB_SEQUENCE: $($seq -join ' -> ')"
  InvokeElement $retry; Start-Sleep -Milliseconds 300
  $infoAfterRetry=ById $w1 'ConnectionErrorInfoBar'
  L "INFOBAR_RETRY: invoked=yes info_visible_after=$(IsVisible $infoAfterRetry)"

  $hwnd=[IntPtr]$p1.MainWindowHandle; $cr=[R4FailureWin32+RECT]::new();[R4FailureWin32]::GetClientRect($hwnd,[ref]$cr)|Out-Null;$pt=[R4FailureWin32+POINT]::new();[R4FailureWin32]::ClientToScreen($hwnd,[ref]$pt)|Out-Null
  $bmp=[System.Drawing.Bitmap]::new($cr.Right-$cr.Left,$cr.Bottom-$cr.Top);$g=[System.Drawing.Graphics]::FromImage($bmp);$g.CopyFromScreen($pt.X,$pt.Y,0,0,$bmp.Size);$bmp.Save($png,[System.Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$bmp.Dispose();L "SCREENSHOT: path=evidence/runtime.png size=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top)"

  $closeCandidate=ById $w1 'CloseButton'
  if(-not $closeCandidate){$closeCandidate=@(AllByType $w1 ([System.Windows.Automation.ControlType]::Button)|Where-Object{$_.Current.AutomationId -match 'Close'})|Select-Object -First 1}
  L "INFOBAR_CLOSE_DISCOVERY: candidate_present=$([bool]$closeCandidate) candidate_id='$(if($closeCandidate){$closeCandidate.Current.AutomationId}else{''})' candidate_name='$(if($closeCandidate){$closeCandidate.Current.Name}else{''})'"
  if($closeCandidate){InvokeElement $closeCandidate;Start-Sleep -Milliseconds 300;$infoAfterClose=ById $w1 'ConnectionErrorInfoBar';L "INFOBAR_DISMISSAL: invoked=yes info_visible_after=$(IsVisible $infoAfterClose)"} else {L 'INFOBAR_DISMISSAL: invoked=no info_visible_after=True'}
  StopEvalApp $p1; $p1=$null

  $pair=StartEvalApp; $p2=$pair[0]; $w2=$pair[1]
  $remove=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) $removeName
  if(-not $remove){throw 'Remove saved device button not found'}
  $remove.SetFocus(); Start-Sleep -Milliseconds 100
  InvokeElement $remove; Start-Sleep -Milliseconds 500
  $primary=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Remove'
  $cancel=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Cancel'
  $dialogTexts=TextNames $w2
  $focusedBeforeEnter=[System.Windows.Automation.AutomationElement]::FocusedElement
  L "DIALOG_OPEN: primary_present=$([bool]$primary) cancel_present=$([bool]$cancel) device_named=$([bool](@($dialogTexts|Where-Object{$_ -like "*$deviceName*"}).Count)) focused_id='$($focusedBeforeEnter.Current.AutomationId)' focused_name='$($focusedBeforeEnter.Current.Name)'"
  if(-not $primary -or -not $cancel){throw 'ContentDialog action buttons not found'}
  [R4FailureWin32]::SetForegroundWindow([IntPtr]$p2.MainWindowHandle)|Out-Null
  [System.Windows.Forms.SendKeys]::SendWait('{ENTER}');Start-Sleep -Milliseconds 450
  $cancelAfterEnter=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Cancel'
  $focusedAfterEnter=[System.Windows.Automation.AutomationElement]::FocusedElement
  L "DIALOG_DEFAULT_ACTION: enter_sent=yes dialog_actions_present_after=$([bool]$cancelAfterEnter) focused_after_id='$($focusedAfterEnter.Current.AutomationId)' focused_after_name='$($focusedAfterEnter.Current.Name)' focus_returned_to_remove=$($focusedAfterEnter.Current.Name -eq $removeName)"

  $remove=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) $removeName
  InvokeElement $remove;Start-Sleep -Milliseconds 450
  $cancel=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Cancel'
  InvokeElement $cancel;Start-Sleep -Milliseconds 450
  $focusedAfterCancel=[System.Windows.Automation.AutomationElement]::FocusedElement
  $cancelStill=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Cancel'
  L "DIALOG_CLOSE_ACTION: cancel_invoked=yes dialog_actions_present_after=$([bool]$cancelStill) focused_after_name='$($focusedAfterCancel.Current.Name)' focus_returned_to_remove=$($focusedAfterCancel.Current.Name -eq $removeName)"

  $remove=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) $removeName
  InvokeElement $remove;Start-Sleep -Milliseconds 450
  $primary=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Remove'
  InvokeElement $primary;Start-Sleep -Milliseconds 450
  $focusedAfterPrimary=[System.Windows.Automation.AutomationElement]::FocusedElement
  $primaryStill=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Remove'
  L "DIALOG_PRIMARY_ACTION: remove_invoked=yes dialog_actions_present_after=$([bool]$primaryStill) focused_after_name='$($focusedAfterPrimary.Current.Name)' focus_returned_to_remove=$($focusedAfterPrimary.Current.Name -eq $removeName)"
  L 'RESULT: runtime UI Automation sequence completed without script exception.'
}
catch {L "ERROR: $($_.Exception.Message)"; throw}
finally {
  $out|Set-Content -Path $log -Encoding UTF8
  if($p1){StopEvalApp $p1};if($p2){StopEvalApp $p2}
}
