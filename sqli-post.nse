description = [[
Ejemplo para Deteccion SQL Injection via POST
Uso :
nmap -n -v -p 80 --script ./sqli-post.nse --script-args=sqli-get.uri="/acme/login.php",sqli-get.param="username" 192.168.1.137
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

-- URI de la pagina a analiza, en siguiente version puede ser un argumento
-- local uri = "/acme/login.php"
local uri = stdnse.get_script_args("sqli-post.uri")
local param = stdnse.get_script_args("sqli-post.param")

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

-- La data del POST
local postdata = {}
-- postdata[param]="'"
-- postdata["password"]=""
-- postdata["Login"]="Login"

response = http.get(host, port, uri)

if response.body then

      local forms = http.grab_forms(response.body)

      if forms then
	local form = http.parse_form(forms[1])
	-- This works just for one login form in one dynamic web page
	for _, field in ipairs(form['fields']) do
	    postdata[field['name']]= field['value'] or ""
	end
	postdata[param]="'"
      end
	
end

-- Se realiza el POST
local responsepost = http.post(host, port, uri, nil, nil, postdata)

-- Se analiza la respuesta en busqueda del error de sintaxis
-- if response.body and response.status==200 and response.body:match("You have an error in your SQL syntax") then
-- 	return "La pagina en http://" .. host.ip .. "/acme/login.php ===> Es VULNERABLE a Inyeccion de SQL"
-- end

if responsepost.body and ( responsepost.status==200 or responsepost.status==500 ) then
	for line in io.lines ("/home/wcuestas/ehtoolz/open-sec/sqlierrors.lst") do
         if responsepost.body:match(line) then
            return "La pagina en http://" .. hostname .. uri .. " ===> Es VULNERABLE a Inyeccion de SQL en el parametro ---> " .. param
         end
        end

end


end
