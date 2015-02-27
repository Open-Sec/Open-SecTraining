@echo off
for /L %%p in (20,1,82) do echo Chequeando Puerto %%p: >> puertos.txt & echo open 192.168.1.171 %%p > comftp.txt & echo quit >> comftp.txt & echo quit >> comftp.txt & echo quit >> comftp.txt & ftp -s:comftp.txt 2>> puertos.txt
