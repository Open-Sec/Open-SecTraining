$ErrorActionPreference = "silentlycontinue"
if ($args.count -eq 0) {
   write-output "Debes ingresar la subnet a descubrir"
   exit
}
$subnet=$args[0]+"."
$ip=1
for ($ip; $ip -lt 255; $ip++)
{
  $ipaddr=$subnet+$ip
  write-output "Direccion IP : $ipaddr"
  $ping=New-Object System.Net.NetworkInformation.Ping
  $pong=$ping.Send($ipaddr)
  write-output $pong
}
