$ErrorActionPreference = 'silentlycontinue'
if ($args.count -eq 0) {
   write-output "Debes ingresar la IP a escanear"
   exit
}

$ip=$args[0]

$ports = 21,22,23,25,80,110,143,389,443,445,636,1433,1521,3128,3306,3389,8080
$elemento = 0
$UTF8 = [System.Text.Encoding]::UTF8

write-output "Puertos abiertos en $ip :"

for ($elemento; $elemento -lt $ports.length; $elemento++)
{
  #Usando la clase TcpClient de .Net
  $tcp = New-Object System.Net.Sockets.TcpClient
  $tcp.SendTimeout = 3000
  $tcp.ReceiveTimeout = 3000 
  $tcp.Connect($ip,$ports[$elemento])
  if ($tcp.Connected)
  {
    write-output "El puerto $($ports[$elemento]) esta abierto"
    #Forzando a obtener el banner si es HTTP y a veces HTTPS
    if ( ($ports[$elemento] -eq 80) -or ($ports[$elemento] -eq 443) )
    {
       $msg = "quit\r\n"
       $data = $UTF8.GetBytes($msg)
       $stream1 = $tcp.GetStream() 
       $Writer = New-Object System.IO.StreamWriter($stream1)
       $msg | %{
        $Writer.WriteLine($_)
        $Writer.Flush()
       }
       $Stream.Close()
    }
    $stream2 = $tcp.GetStream()
    $buffer = new-object System.Byte[] 1024
    $encoding = new-object System.Text.AsciiEncoding
    $banner = $stream2.Read($buffer, 0, 1024)
    write-output "Banner ===> $($encoding.GetString($buffer, 0, $banner))"
    $stream.Close()
    $tcp.Close()
  }
  else
  {
   write-output "El puerto $($ports[$elemento]) esta filtrado o cerrado"
  }
}
