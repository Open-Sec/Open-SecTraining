#!/bin/bash
#Execute : bash specialps.sh file-targets-ports.lst
#File format:
#ip_address1 port1,port2,port3,...
#ip_address2 port4,port5,port6....

for line in `cat targets.lst`
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
			( nmap -n -v -Pn -sT --open --disable-arp-ping -p `echo $ports` `echo $target`)
			target=""
			ports=""
		fi
	done

