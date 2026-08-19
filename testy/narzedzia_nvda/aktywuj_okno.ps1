$ErrorActionPreference = "Stop"
Add-Type @"
using System; using System.Runtime.InteropServices; using System.Text;
public class M {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L,T,R,B; }
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern bool GetCursorPos(out System.Drawing.Point p);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern IntPtr GetFocus();
  [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int c);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
}
"@ -ReferencedAssemblies System.Drawing

$p = Get-Process EdSharpNG
$h = $p.MainWindowHandle
[void][M]::ShowWindow($h, 9)
Start-Sleep -Milliseconds 400

$r = New-Object M+RECT
[void][M]::GetWindowRect($h, [ref]$r)
Write-Output ("okno EdSharp: " + $r.L + "," + $r.T + " - " + $r.R + "," + $r.B)

# zapamietaj pozycje kursora, zeby ja przywrocic
$old = New-Object System.Drawing.Point
[void][M]::GetCursorPos([ref]$old)

# klikamy w SRODEK obszaru tekstu (nie w pasek tytulu, nie w menu)
$cx = [int](($r.L + $r.R) / 2)
$cy = [int]($r.T + (($r.B - $r.T) * 0.6))
[void][M]::SetCursorPos($cx, $cy)
Start-Sleep -Milliseconds 250
[M]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)   # LEFTDOWN
[M]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)   # LEFTUP
Start-Sleep -Milliseconds 900

# przywroc kursor tam, gdzie byl
[void][M]::SetCursorPos($old.X, $old.Y)

$fg = [M]::GetForegroundWindow()
$sb = New-Object System.Text.StringBuilder 512
[void][M]::GetWindowText($fg, $sb, 512)
$pidNow = 0
[void][M]::GetWindowThreadProcessId($fg, [ref]$pidNow)
Write-Output ("foreground: " + $sb.ToString() + " pid=" + $pidNow)
Write-Output ("EDSHARP_AKTYWNY=" + ($pidNow -eq $p.Id))
