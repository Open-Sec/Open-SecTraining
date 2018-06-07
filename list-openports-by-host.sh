#!/bin/bash
# xtract-host-open-ports.sh file.gnmap file.nmap
# takes hosts and open ports from .gnmap and DNS names from .nmap
# .gnmap doesn't store dns names and sometimes there are several IPs for one DNS name and viceversa

grep "Nmap scan report for" $2 > nombreshosts.lst
grep "Ports:" $1 | sort -k 2 | uniq > gnmapuniq.lst

prevIFS=$IFS
IFS=$'\n'
numlinea=1
for linea in `cat gnmapuniq.lst`
	do 
		echo $linea > lineatemp.txt
		hostip=`cat lineatemp.txt | cut -d " " -f 2`
		hostname=`grep $hostip nombreshosts.lst | cut -d " " -f 5,6`
		flagquiebrehost=1
		camposxlinea=`cat lineatemp.txt | wc -w`
		for (( campo = 1; campo <= camposxlinea; campo++ ))
			do
				tipodelim=`grep , lineatemp.txt | wc -l`
				if [ $tipodelim -ge 1 ]
				then
					delim=","
				else
					delim=" "
				fi
				cat lineatemp.txt | cut -d $delim -f $campo > puertotemp.txt
				proto=`cat puertotemp.txt | cut -d "/" -f 5`
				estado=`cat puertotemp.txt | cut -d "/" -f 2`
				if [ "$estado" == "open" ]
				then
					#Definicion default de puerto para cualquier linea
					port=`cat puertotemp.txt | cut -d "/" -f 1`
					#Quiebre por host en reporte y definicion de puerto en caso cumple el primer puerto escaneado
					if [ $flagquiebrehost -eq 1 ]
					then
						echo -e "######### Host : $hostname ---> \n"
						if [ `grep ^Host puertotemp.txt | wc -l` -ge 1 ] 
						then
							port=`cat puertotemp.txt | cut -d " " -f  4 | cut -d "/" -f 1`
						fi
						flagquiebrehost=0
					fi
					service=`cat puertotemp.txt | cut -d "/" -f 7`
					echo -e "$proto / $port / $estado ---> $service \n"
				fi
			done
		#echo -e "\n"
	done
#done
IFS=$prevIFS
