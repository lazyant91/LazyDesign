$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class EvalWin32Failure {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr hWnd, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr hWnd, ref POINT p);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@
$packet = 'Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r2\guided\failure-confirmation'
$exe = Join-Path $packet 'project\bin\x64\Debug\net9.0-windows10.0.22621.0\win-x64\LazyDesign.EvaluationApp.exe'
$log = Join-Path $packet 'evidence\runtime-uia.txt'
$png = Join-Path $packet 'evidence\runtime.png'
$out = [System.Collections.Generic.List[string]]::new()
function L([string]$s) { $out.Add($s); Write-Output $s }
function ById($root,[string]$id) {
  $c=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::AutomationIdProperty,$id)
  return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants,$c)
}
function ByTypeAndName($root,$type,[string]$name) {
  $a=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty,$type)
  $b=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty,$name)
  return $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.AndCondition]::new($a,$b))
}
function AllButtons($root) {
  $c=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
  return @($root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$c))
}
function TextNames($root) {
  $c=[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty,[System.Windows.Automation.ControlType]::Text)
  return @($root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$c) | ForEach-Object {$_.Current.Name} | Where-Object {$_})
}
function StartEvalApp {
  $p=Start-Process -FilePath $exe -PassThru
  $w=$null
  for($i=0;$i -lt 60 -and -not $w;$i++) {
    Start-Sleep -Milliseconds 200; $p.Refresh()
    if($p.HasExited){throw "app exited before window; exit=$($p.ExitCode)"}
    if($p.MainWindowHandle -ne 0){$w=[System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)}
  }
  if(-not $w){throw 'top-level UIA window not found'}
  [EvalWin32Failure]::SetForegroundWindow([IntPtr]$p.MainWindowHandle) | Out-Null
  return @($p,$w)
}
function StopEvalApp($p) {
  if($p -and -not $p.HasExited){$p.CloseMainWindow() | Out-Null; Start-Sleep -Milliseconds 350; if(-not $p.HasExited){Stop-Process -Id $p.Id -Force}}
}
function IsVisible($e) { return ($e -and -not $e.Current.IsOffscreen) }
function InvokeElement($e) {
  $ip=[System.Windows.Automation.InvokePattern]$e.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
  $ip.Invoke()
}
L 'METHOD: Launch frozen v0.1-r2 guided failure-confirmation executable; exercise InfoBar Retry and dismissal plus ContentDialog keyboard/default/close and focus-return behavior with Windows UI Automation; capture a runtime screenshot without changing OS settings.'
L 'COMMAND: powershell.exe -File evaluation/.runs/v2/v0.1-r2/guided/failure-confirmation/evidence/runtime-uia.ps1'
$p1=$null; $p2=$null
try {
  $pair=StartEvalApp; $p1=$pair[0]; $w1=$pair[1]
  $info=ById $w1 'ConnectionErrorInfoBar'; $retry=ById $w1 'RetryButton'; $remove=ById $w1 'RemoveDeviceButton'
  if(-not $info -or -not $retry -or -not $remove){throw 'required initial controls not found'}
  $texts=TextNames $w1
  $required=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('7J6l7LmY6rCAIOydkeuLte2VmOyngCDslYrslZjsirXri4jri6QuIOyepey5mOqwgCDsvJzsoLgg7J6I6rOgIOuPmeydvO2VnCDrhKTtirjsm4ztgazsl5Ag7Jew6rKw65CY7Ja0IOyeiOuKlOyngCDtmZXsnbjtlZwg7ZuEIOuLpOyLnCDsi5zrj4TtlZjshLjsmpQu'))
  L "RUNTIME1: launched=yes pid=$($p1.Id) window='$($w1.Current.Name)' info_visible=$(IsVisible $info) retry_enabled=$($retry.Current.IsEnabled) remove_visible=$(IsVisible $remove) required_message_present=$($texts -contains $required)"
  L "TEXTS_INITIAL: $($texts -join ' | ')"
  L "BUTTONS_INITIAL: $(@(AllButtons $w1 | ForEach-Object {"$($_.Current.AutomationId):$($_.Current.Name):enabled=$($_.Current.IsEnabled)"}) -join '|')"
  $retry.SetFocus(); Start-Sleep -Milliseconds 100
  $seq=@(); 1..2 | ForEach-Object {[System.Windows.Forms.SendKeys]::SendWait('{TAB}');Start-Sleep -Milliseconds 160;$f=[System.Windows.Automation.AutomationElement]::FocusedElement;$seq += "$($f.Current.ControlType.ProgrammaticName):$($f.Current.AutomationId):$($f.Current.Name)"}
  L "KEYBOARD_TAB_SEQUENCE: $($seq -join ' -> ')"
  InvokeElement $retry; Start-Sleep -Milliseconds 350
  $textsAfter=TextNames $w1; $retry=ById $w1 'RetryButton'
  $retryTitle=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('6rGw7IukIOuUlOyKpO2UjOugiOydtOyXkCDri6Tsi5wg7Jew6rKw7ZWY64qUIOykkeyeheuLiOuLpC4=')); $retryMessage=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('7Jew6rKw7J2EIOuLpOyLnCDsi5zrj4TtlZjqs6Ag7J6I7Iq164uI64ukLg=='))
  L "INFOBAR_RETRY: title_changed=$($textsAfter -contains $retryTitle) message_changed=$($textsAfter -contains $retryMessage) retry_enabled_after=$($retry.Current.IsEnabled)"
  L "TEXTS_AFTER_RETRY: $($textsAfter -join ' | ')"
  $hwnd=[IntPtr]$p1.MainWindowHandle; $cr=[EvalWin32Failure+RECT]::new(); [EvalWin32Failure]::GetClientRect($hwnd,[ref]$cr)|Out-Null; $pt=[EvalWin32Failure+POINT]::new(); [EvalWin32Failure]::ClientToScreen($hwnd,[ref]$pt)|Out-Null
  $bmp=[System.Drawing.Bitmap]::new($cr.Right-$cr.Left,$cr.Bottom-$cr.Top); $g=[System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($pt.X,$pt.Y,0,0,$bmp.Size); $bmp.Save($png,[System.Drawing.Imaging.ImageFormat]::Png)
  $colors=@{};$sum=0;$count=0;for($y=10;$y -lt $bmp.Height;$y+=20){for($x=10;$x -lt $bmp.Width;$x+=20){$c=$bmp.GetPixel($x,$y);$k="$($c.R),$($c.G),$($c.B)";if(-not $colors.ContainsKey($k)){$colors[$k]=0};$colors[$k]++;$sum+=$c.R+$c.G+$c.B;$count+=3}}
  $avg=if($count){[Math]::Round($sum/$count,1)}else{0};$g.Dispose();$bmp.Dispose();L "SCREENSHOT: path=evidence/runtime.png size=$($cr.Right-$cr.Left)x$($cr.Bottom-$cr.Top) sampled_unique_colors=$($colors.Count) avg_rgb_component=$avg"
  StopEvalApp $p1; $p1=$null

  $pair=StartEvalApp; $p2=$pair[0]; $w2=$pair[1]
  $info=ById $w2 'ConnectionErrorInfoBar'; $retry=ById $w2 'RetryButton'; $remove=ById $w2 'RemoveDeviceButton'
  $buttons=AllButtons $w2
  $closeCandidate=ById $w2 'CloseButton'
  L "INFOBAR_CLOSE_DISCOVERY: candidate_present=$([bool]$closeCandidate) candidate_id='$($closeCandidate.Current.AutomationId)' candidate_name='$($closeCandidate.Current.Name)'"
  if($closeCandidate){InvokeElement $closeCandidate;Start-Sleep -Milliseconds 300;$info=ById $w2 'ConnectionErrorInfoBar';L "INFOBAR_DISMISSAL: invoked=yes info_visible_after=$(IsVisible $info)"} else {L 'INFOBAR_DISMISSAL: invoked=no info_visible_after=True'}

  InvokeElement $remove; Start-Sleep -Milliseconds 500
  $dialog=ById $w2 'RemoveDeviceDialog'; $primary=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Remove'; $cancel=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Cancel'
  $dialogTexts=TextNames $w2
  $dialogMessage=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('7KCA7J6l65CcIOyepey5mCAn6rGw7IukIOuUlOyKpO2UjOugiOydtCfqsIAg7J20IFBD7JeQ7IScIOygnOqxsOuQqeuLiOuLpC4g64uk7IucIOyCrOyaqe2VmOugpOuptCDsnqXsuZjrpbwg64uk7IucIOy2lOqwgO2VtOyVvCDtlanri4jri6Qu'))
  L "DIALOG_TEXTS: $($dialogTexts -join ' | ')"
  L "DIALOG_OPEN: primary_present=$([bool]$primary) cancel_present=$([bool]$cancel) device_named=$($dialogTexts -contains $dialogMessage)"
  [EvalWin32Failure]::SetForegroundWindow([IntPtr]$p2.MainWindowHandle)|Out-Null
  [System.Windows.Forms.SendKeys]::SendWait('{ENTER}'); Start-Sleep -Milliseconds 450
  $dialogAfterEnter=ById $w2 'RemoveDeviceDialog'; $focused=[System.Windows.Automation.AutomationElement]::FocusedElement
  L "DIALOG_DEFAULT_ACTION: enter_sent=yes dialog_visible_after=$(IsVisible $dialogAfterEnter) focused_after_id='$($focused.Current.AutomationId)' focused_after_name='$($focused.Current.Name)'"

  $remove=ById $w2 'RemoveDeviceButton'; InvokeElement $remove; Start-Sleep -Milliseconds 450
  $cancel=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Cancel'
  if(-not $cancel){throw 'Cancel button not found on reopened ContentDialog'}
  InvokeElement $cancel; Start-Sleep -Milliseconds 450
  $dialogAfterCancel=ById $w2 'RemoveDeviceDialog'; $focused2=[System.Windows.Automation.AutomationElement]::FocusedElement
  L "DIALOG_CLOSE_ACTION: cancel_invoked=yes dialog_visible_after=$(IsVisible $dialogAfterCancel) focused_after_id='$($focused2.Current.AutomationId)' focused_after_name='$($focused2.Current.Name)'"
  $remove=ById $w2 'RemoveDeviceButton'; InvokeElement $remove; Start-Sleep -Milliseconds 450
  $primary=ByTypeAndName $w2 ([System.Windows.Automation.ControlType]::Button) 'Remove'
  if(-not $primary){throw 'Remove primary button not found on reopened ContentDialog'}
  InvokeElement $primary; Start-Sleep -Milliseconds 450
  $dialogAfterPrimary=ById $w2 'RemoveDeviceDialog'; $focused3=[System.Windows.Automation.AutomationElement]::FocusedElement
  L "DIALOG_PRIMARY_ACTION: remove_invoked=yes dialog_visible_after=$(IsVisible $dialogAfterPrimary) focused_after_id='$($focused3.Current.AutomationId)' focused_after_name='$($focused3.Current.Name)'"
  L 'RESULT: runtime UI Automation sequence completed without script exception.'
}
catch {L "ERROR: $($_.Exception.Message)"; throw}
finally {
  $out | Set-Content -Path $log -Encoding UTF8
  if($p1){StopEvalApp $p1}; if($p2){StopEvalApp $p2}
}
