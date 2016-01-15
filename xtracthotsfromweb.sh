#!/bin/bash
#Uso : xtracthosts.sh dominio wget|directorio archivo_urls
#Parametros en orden secuencial :
#dominio como acme.com (sin nombre de host ni cname)
#la palabra wget o el nombre del directorio de una descarga previa
#archivo de texto con urls como http://www.acme.com y https://www.acme.com
#este ultimo es opcional si se usa una descarga previa
#Ejemplos :
#xtracthosts.sh dominio wget urls.txt----> para descargar web y buscar
#xtracthosts.sh dominio pucp.edu.pe urls.txt----> para solamente buscar en base a descarga previa
if [ $2 = "wget" -a $# != 3 ]; then
        echo "bash xtracthosts.sh dominio wget|directorio archivo_urls"
        exit
fi
if [ $2 = "wget" ]; then
        wget -r --no-check-certificate -i $3
fi
if [ $2 != "wget" ]; then
        cd $2
else
        cd www.$1
fi
#url="[http-https]\:\/\/[A-Za-z]*\.$1"
url="http|https"
#Dado que no hay una estructura uniforme, se trata de capturar la mayor cantidad posible de URLs, en las pruebas se observo que la primera seleccion mas frecuente corresponde al campo 4
grep --exclude=temporal.txt -R -E "$url" * | cut -d "/" -f 4 | cut -d '"' -f 1 | grep $1 | cut -d "'" -f 1 | sort -u > ./temporal.txt
#Pero, tambien se requiere extraer el campo 3.  Aun asi, es probable que queden URLs sin ser detectados
grep --exclude=temporal.txt -R -E "$url" * | cut -d "/" -f 3 | cut -d '"' -f 1 | grep $1 | cut -d "'" -f 1 | sort -u >> ./temporal.txt
cat ./temporal.txt | sort -u > ../hosts-$1.txt
echo "Nombres de hosts encontrados"
echo "============================"
cat ../hosts-$1.txt
echo "Reporte en archivo -----> hosts-$1"
cd ..
