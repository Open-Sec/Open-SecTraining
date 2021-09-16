#!/bin/bash
#Execute : bash specialps.sh file-targets-ports.lst nmap-reports-name
#File format:
#ip_address1 port1,port2,port3,...
#ip_address2 port4,port5,port6....

for line in `cat $1`
	do 
		possibletarget=`echo $line | grep -o "\." | wc -l`
		if [ $possibletarget -eq 3 ]
		then
			target=$line
		else
			ports=$line
		fi
		if [ ! -z "$target" ] && [ ! -z "$ports" ]
		then
			( nmap -n -v -Pn -sT --open --disable-arp-ping -sV -p `echo $ports` `echo $target` -oA `echo $2 --append-output`)
			target=""
			ports=""
		fi
	done
