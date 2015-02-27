#!/bin/bash
fping -g $1 $2 > fping_lista.txt 2>/dev/null
grep "is alive" fping_lista.txt > activos.txt
echo "Lista de Direcciones IP Activas"
echo "-------------------------------"
for host in `cat activos.txt | cut -d " " -f 1`
    do
	   echo $host
    done
arp -an | grep ether > macs.txt
echo ""
echo "Lista de MACs Activas (IP,MAC,Interface)"
echo "---------------------"
cat macs.txt | cut -d " " -f 2,4,7
