description = [[
Ejemplo para Deteccion SQL Injection via GET
Uso :
nmap -n -v -p 80 --script ./sqli-get.nse --script-args=sqli-get.uri="/acme/demosqli.php",sqli-get.param="id" 192.168.1.137
]]

-- Categorias dentro de las que se ubica el script
categories = {"auth","vuln"}

-- Se requiere la libreria http para hacer las peticiones a la pagina web, shortport para validar que los puertos web esten abiertos y stdnse de forma general
local http = require "http"
local shortport = require "shortport"
local stdnse = require "stdnse"

-- Se valida que exista al menos un puerto web abierto
portrule = shortport.http

-- Una vez hecha la validacion anterior, se ejecuta el script
action = function(host, port)

-- URI de la pagina a analizar, en siguiente version puede ser un argumento
-- local uri = "/acme/demosqli.php?id='"
-- Ejemplos :
-- uri : /demosqli.php
-- param : id
local uri = stdnse.get_script_args("sqli-get.uri") 
local param = stdnse.get_script_args("sqli-get.param")

-- stdnse.print_debug(1, "%s: Valor de host %s", SCRIPT_NAME, host.ip)
-- stdnse.print_debug(1, "%s: Valor de uri %s", SCRIPT_NAME, uri)

local _, status_404, resp_404 = http.identify_404(host,port)

if status_404 == 200 then
	stdnse.print_debug(1, "%s: El Web devuelve respuestas ambiguas, se pueden dar falsos positivos porque no devuelve errores 404 estandares. Saliendo.", SCRIPT_NAME)
	return
end

stdnse.print_debug(1, "%s: HTTP HEAD %s", SCRIPT_NAME,uri)

local hostname = ""
if host.targetname == nil then
	hostname = host.ip
else
	hostname = host.targetname
end

-- La data del GET
-- local getdata = "

-- postdata["username"]="'"
-- postdata["password"]=""
-- postdata["Login"]="Login"

-- Se realiza el GET
local response = http.get(host, port, uri .. "?" .. param .. "='", nil)

-- Se analiza la respuesta en busqueda del error de sintaxis
-- stdnse.print_debug(1, "%s: Valor de response-status %s", SCRIPT_NAME, response.status)
-- if response.body and ( response.status==200 or response.status==500 ) and response.body:match("You have an error in your SQL syntax") then
-- if response.body and ( response.status==200 or response.status==500 ) and response.body:match("80040e14") then
if response.body and ( response.status==200 or response.status==500 ) then
	for line in io.lines ("/home/wcuestas/ehtoolz/open-sec/sqlierrors.lst") do
         if response.body:match(line) then
            return "La pagina en http://" .. hostname .. uri .. " ===> Es VULNERABLE a Inyeccion de SQL en el parametro ---> " .. param
         end
        end
--	return "La pagina en http://" .. hostname .. uri .. " ===> Es VULNERABLE a Inyeccion de SQL"
end

end
