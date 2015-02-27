#!/bin/bash
port=1
echo "Puertos abiertos en $1" > $2
echo "===============================" >> $2
while [ $port -le 1024 ]
do 
     (echo > /dev/tcp/$1/$port) 2>/dev/null 
     if [ $? = 0 ]
     then
             echo "El puerto $port esta abierto" >> $2
     fi
     port=`expr $port + 1`
done
