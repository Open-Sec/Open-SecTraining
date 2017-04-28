description = [[
http-google-email queries the Google web search engine and Google Groups for e-mails pertaining to a specific domain.
]]

---
-- @usage
-- nmap -p80 --script http-google-email <host>
--
-- @output
-- PORT   STATE SERVICE
-- 80/tcp open  http
-- | http-google-email: 
-- | nmap-dev () insecure org
-- | nmap-svn () insecure org
-- |_fyodor () insecure org
--
-- @args http-google-email.domain Domain to search for. 
-- @args http-google-email.pages The number of results pages to be requested from Google Web search and Google Group search respectively. Default is 5.
---

author = "Shinnok"
license = "Same as Nmap--See http://nmap.org/book/man-legal.html"
categories = {"discovery", "safe", "external"}

local http = require "http"
local shortport = require "shortport"
local stdnse = require "stdnse"

portrule = shortport.http

--Builds Google Web Search query
-- () param domain 
-- () param page
-- () return Url 
local function google_search_query(domain, page)
  --return string.format("http://www.google.com/search?q=%%40%s&hl=en&lr=&ie=UTF-8&start=%s&sa=N", domain, page)
  --return string.format("http://www.google.com/search?hl=en&meta=&client=safari&rls=en&q=@%s&start=%s", domain, page)
  --OPEN-SEC : El siguiente URL fue tomado de lo elaborado para theHarvester :
  return string.format("http://www.google.com/search?num=100&start=%s&hl=en&meta=&client=safari&q=%%40%%22%s%%22", page, domain)
end
--Builds Google Groups Search query
-- () param domain 
-- () param page
-- () return Url 
local function google_groups_query(domain, page)
  return string.format("http://groups.google.com/groups?q=%s&hl=en&lr=&ie=UTF-8&start=%s&sa=N", domain, page)
end


---
--MAIN
---
action = function(host, port)
  --OPEN-SEC: Se incremento el default de paginas a tomar en cuenta de los resultados en Google
  local pages = 50
  local target
  local emails = {}

  if(stdnse.get_script_args("http-google-email.pages")) then
      pages = stdnse.get_script_args("http-google-email.pages")*10
  end

  -- Check if we have the domain argument passed
  if(stdnse.get_script_args("http-google-email.domain")) then
    target = stdnse.get_script_args("http-google-email.domain")
  else
    -- Verify that we have a hostname available
    if not(host.targetname) then
      return string.format("[ERROR] Host can not be resolved to a domain name.")
    else
      target = host.targetname
    end
  end

  stdnse.print_debug(1, "%s: Checking domain %s", SCRIPT_NAME, target) 

  -- Google Web search

  for page=0, pages, 10 do
    local qry = google_search_query(target, page)
    -- stdnse.print_debug(1, "%s: Valor de qry %s", SCRIPT_NAME, qry)
    local req = http.get_url(qry)
    stdnse.print_debug(2, "%s", qry)
    stdnse.print_debug(2, "%s", req.body)
    -- stdnse.print_debug(1, "%s: Body %s", SCRIPT_NAME, req.body)    

    body = req.body:gsub('<em>', '')
    body = body:gsub('</em>', '')
    -- stdnse.print_debug(1, "%s: Body %s", SCRIPT_NAME, body)

    if body then
      local found = false
      --OPEN-SEC:Las direcciones de correo vienen precedidad de "bold".  Siempre hay cambios en la rpta de Google.
      for email in body:gmatch('[A-Za-z0-9%.%%%+%-]+@<b>' .. target) do
	--stdnse.print_debug(1,"Email ANTES PAIRS ---> %s ",email)
	----OPEN-SEC:Si emails es nil ({}), la primera vez que pasa no entra al for ...pairs, se puede definir emails = {""} para depuracion.
	--OPEN-SEC: Renovar valor de found para que inserte en array todos los emails encontrados y unicos.
	found = false
        for i, value in pairs(emails) do
          --stdnse.print_debug(1,"ENTRO")
          --stdnse.print_debug(1,"Email %s - Value --->%s, Indice %s",email,value,i)
          if value == email then
            found = true
	  end
        end
        if not found then 
	  --stdnse.print_debug(1,"Email insertado es: %s",email)
          emails[#emails+1] = email
        end
      end
    end
    stdnse.sleep(2.0)
  end

 --for i, v in pairs(emails) do
      --print(i,v)
  --end
  
  -- Google Groups search

  --for page=0, pages, 10 do
    --local qry = google_groups_query(target, page)
    --local req = http.get_url(qry)
    --stdnse.print_debug(2, "%s", qry)
    --stdnse.print_debug(2, "%s", req.body)

    --body = req.body:gsub('<b>', '')
    --body = body:gsub('</b>', '')
    --if body then
      --local found = false
      --for email in body:gmatch('[A-Za-z0-9%.%%%+%-]+@' .. target) do
        --for _, value in pairs(emails) do
          --if value == email then
            --found = true
          --end
        --end
        --if not found then 
          --emails[#emails+1] = email
        --end
      --end
    --end
  --end

  if #emails > 0 then
    return "\n" .. stdnse.strjoin("\n", emails)
  end
end
