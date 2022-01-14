#!/usr/bin/zsh
port=1
echo "Puertos abiertos en $1" > $2
echo "===============================" >> $2
zmodload zsh/net/tcp
while [ $port -le 1024 ]
do 
     ztcp $1 $port 2>/dev/null 
     if [ $? = 0 ]
     then
             echo "El puerto $port esta abierto" >> $2
     fi
     port=`expr $port + 1`
done
