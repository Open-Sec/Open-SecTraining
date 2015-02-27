#!/bin/bash

echo $1 > ip1.txt
echo $2 > ip2.txt
octeto1=`cat ip1.txt | cut -d "." -f 1`
octeto2=`cat ip1.txt | cut -d "." -f 2`
octeto3=`cat ip1.txt | cut -d "." -f 3`
nodo1=`cat ip1.txt | cut -d "." -f 4`
nodo2=`cat ip2.txt | cut -d "." -f 4`
nodoactual=$nodo1

while [ $nodoactual -le $nodo2 ]
do
	ipactual=$octeto1.$octeto2.$octeto3.$nodoactual
	host $ipactual
	pong=`ping -w 1 -n -c 3 $ipactual | grep "bytes from" | wc -l`
	if [ $pong -ge 1 ] 
	then
		echo "$ipactual is alive"
        fi
	nodoactual=`expr $nodoactual + 1`
done
