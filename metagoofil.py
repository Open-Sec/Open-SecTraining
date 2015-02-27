#!/usr/bin/python
#Covered by GPL V2.0
import time
import string
import httplib,sys
from socket import *
import re
import getopt
import urllib
import time
import os

#Cheers to Trompeti, deepbit, Scorpionn, Javier Mendez  and all s21sec crew ;)

print "\n*************************************"
print "*MetaGooFil Ver. 1.4		    *"
print "*Coded by Christian Martorella      *"
print "*Edge-Security Research             *"
print "*cmartorella@edge-security.com      *"
print "*Modified by Open-Sec               *"
print "*Jan-22th-2014                          *"
print "*************************************\n\n"

#Changes made by Open-Sec
#1. Search in Google now includes all the occurrences, not just the most viewed ones, so, "similar pages" count
#   because sometimes they link to different files
#2. Changed regular expression to match href inside tables and inside simple html body
#3. Changed main body (test) to use simple array elements instead of tuplas from edge-security to match with
#   modification number 2.  So, instead of using x[1], it's using now x.
#   With tuplas :
#   [('<', 'http://www.isecom.org/press/hakin9_OSSTMM_DE.pdf'), ('<', 'http://www.isecom.org/osstmm3.HUMSEC.draft.pdf')]
#   Without tuplas :
#   ['http://www.open-sec.com/media/GuiaEttercap.pdf', 'http://www.open-sec.com/media/Open-SecVATools.pdf']
#   Changes from June, 27th, 2010 :
#   - Google results won't include "About " word if the http request includes num=, this parameter corresponds to -l
#   - Inserted portions from 1.4b version for PDFs files that gets better results because newer PDFs versions.
#   - Still works better than the one published by Edge-Security ;)   
#  Changes from March, 28th 2011 :
#  - In howmany, return clean is now at for loop level, don't know why it doesn't work as before and has NO logic.
#  - Because some change in data to parse from Google (links has changed with a lot of garbage at the end), 
#    http://www.google.com/url?sa=t&source=web&cd=17&ved=0CEEQFjAGOAo&url=http%3A%2F%2Fwww.sunarp.gob.pe%2FVIIIJornada.pdf&ei=0D6RTYKEBKaJ0QHF_fzgDg&usg=AFQjCNE1lRhSfCMfnFioRECF7PqdZvcbfA&sig2=crbu-T3S3VWj7xnwLzqe3Q
#    Just changed the run function manipulating according that garbage the url and the file name.
#  Changes from December, 11th, 2011 :
#  - Added an User-Agent as in run function.
#  - Commented an IF len(result) == 1 in howmany function, just don't remember now why I added these lines before because 
#Change from January, 22th 2014 :
# 1. Now, results brings a list of 2 items so we take just the second one :
#--->r1 = re.compile('[1234567890,]* results')
#--->result = r1.findall(data)
#--->print len(result)
#--->print result
#--->print result[0]
#--->print result[1]
#--->Output :
#--->[+] Command extract found, proceeding with leeching
#--->[+] Searching in sunarp.gob.pe for: pdf
#--->2
#--->[' results', '2,460 results']
#--->results
#--->2,460 results
# 2. Changes in logic about quantities when there are n0 files of the required extension, when files are fewer than limit (-l parameter), wen files are more than limit, etc :
#By Open-Sec - Start		
#limit=limiteinicial ---> reoved on Jan 22th 2014
#print limiteinicial
#print total
#print limit
#cant = 0
#if total <= limit:
#	limit=total
#	cant = total
#else:
#	cant = limit
#	print "[+]Limit: ",int(limit)
#	result=[]
#	#print word
#	while cant <= limit:
#		print "[+] Searching results: " + str(limit) +"\r"
#		#By Open-Sec - End
# 3. In run function, the num parameters was changed from static 20 to str(i)
# 	h.putrequest('GET',"/search?num="+str(i)+"&start="+str(i)+"&hl=en&btnG=Search&meta=&q=site%3A"+w+"+filetype%3A"+file+"&safe=off&filter=0")



global word,w,limit,result,extcommand

#Win
##extcommand='c:\extractor\\bin\extract.exe -l libextractor_ole2'
#OSX
#extcommand='/opt/local/bin/extract'
extcommand='/usr/bin/extract'
#Cygwin
#extcommand='/cygdrive/c/extractor/bin/extract.exe'
#extcommand='/usr/bin/extract'

result =[]
global dir
dir = "none"


def usage():
 print "MetaGooFil 1.4\n"
 print "usage: metagoofil options \n"
 print "	-d: domain to search"
 print " 	-f: filetype to download (all,pdf,doc,xls,ppt,odp,ods, etc)"
 print "	-l: limit of results to work with (default 100)"
 print "	-o: output file, html format."
 print "	-t: target directory to download files.\n"
 print "	Example: metagoofil.py -d microsoft.com -l 20 -f all -o micro.html -t micro-files\n"
 sys.exit()


#Mac address extractor#
def get_mac(file,dir):
	 	filename=dir+"/"+file	
		#print filename
		line=open(filename,'r')
		res=""
		for l in line:
			res+=l
		macrex=re.compile('-[0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z]\}')	
		macgetter=macrex.findall(res)
		if macgetter==[]:
			mac=''
		else:
			mac=macgetter[0]
			mac=mac.strip("-")
			mac=mac.strip("}")
			mac=mac[:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
		return mac

#From metagoofil 1.4b
def get_info_pdf(file,dir):
                filename=dir+"/"+file
                line=open(filename,'r')
                res=""
                for l in line:
                        res+=l
                arex=re.compile('xap:Author=.* ')
                getter=arex.findall(res)
                if getter==[]:
                        aut3=''
                else:
                        aut3=getter[0]
                        aut3=aut3.split(" ")[0]
                        aut3=aut3.replace("xap:Author='","")
                        aut3=aut3.replace("'","")
                        pat=""
                        return aut3,pat
                rex=re.compile('xmpmeta')
                getter=rex.findall(res)
                if getter==[]:
                        meta=''
                else:
                        meta=getter[0]
                if meta=='':
                        return meta,meta
                else:
                        pass
                arex=re.compile('Author\(.*\)[<|\/]')
                getter=arex.findall(res)
                if getter==[]:
                        aut=''
                else:
                        aut=getter[0].split("/")[0]
                        #print aut.split("/")[0]
                ###
                arex=re.compile('\<rdf:li\>(.*)\</rdf:li\>\</rdf:Seq\>')
                getter=arex.findall(res)
                if getter==[]:
                        aut2=''
                else:
                        temp=getter[0].replace("<rdf:li>","")
                        aut2=temp.replace("</rdf:li>","")
                        #print aut2
                ##PATH
                rex=re.compile('Title\(.*\)[<|\/]')
		getter=rex.findall(res)
                if getter==[]:
                        pat=''
                else:
                        pat=getter[0]
                        print pat.split("/")[0]
                #SOFTware
                arex=re.compile('Producer=(.*)>')
                getter=arex.findall(res)
                if getter==[]:
                        producer=''
                else:
                        producer=getter[0]
                        producer=producer.replace("></rdf:Description","")

                arex=re.compile(' pdf:Producer=(.*) ')
                getter=arex.findall(res)
                if getter==[]:
                        producer=''
                else:
                        producer=getter[0]
                aut=aut+aut2+aut3
                return aut,pat
#End of fragment from metagoofil 1.4b

def howmany(w):
	 h = httplib.HTTP('www.google.com')
	 #By Open-Sec - Start
	 h.putrequest('GET',"/search?num=100&start=0+hl=en&btnG=Search&meta=&q=site%3A"+w+"+filetype%3A"+file+"&safe=off&filter=0")
	 #By Open-Sec - End
      	 h.putheader('Host', 'www.google.com')
	 h.putheader('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	 #h.putheader('User-agent', 'Internet Explorer 6.0 ')
	 h.endheaders()
	 returncode, returnmsg, headers = h.getreply()
	 #print returncode
	 #print returnmsg
	 #print headers
	 data=h.getfile().read()
	 #print data
	 r1 = re.compile('[1234567890,]* results')
	 #print r1
	 result = r1.findall(data)
	 #print len(result)
	 #print result
	 #print result[0]
	 #print result[1]
	 if len(result) == 1:
	    clean = 0
	    return clean
	 if result == []:
	     r1 = re.compile('[0123456789,]* results')
	     result = r1.findall(data)
	 #contador=0
	 #print result[1]
	 #for x in result[1]:
		  #contador+=1
		  #print contador
		  #print x
		  #print clean
	 #clean = re.sub(' <b>','',x)
	 #clean = re.sub('</b> ','',clean)
	 #clean = re.sub('About','',clean)
	 clean = 0
	 clean = re.sub('results','',result[1])
	 clean = re.sub(',','',clean)
		  #clean = re.sub('of','',clean)
		  #clean returned at for loop level, no logic, but, it works
	 #print clean
	 return clean
	 #print clean
	 if len(result) == 0:
		clean = 0
	 return clean



def run(w,i):
	res = []
	h = httplib.HTTP('www.google.com')
	#By Open-Sec - Start
	h.putrequest('GET',"/search?num="+str(i)+"&start="+str(i)+"&hl=en&btnG=Search&meta=&q=site%3A"+w+"+filetype%3A"+file+"&safe=off&filter=0")
	#h.putrequest('GET',"/search?num=20&start="+str(i)+"&hl=en&btnG=Search&meta=&q=site%3A"+w+"+filetype%3A"+file+"&safe=off&filter=0")
	#By Open-Sec - End
	h.putheader('Host', 'www.google.com')
	h.putheader('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')
	#h.putheader('User-agent', 'Internet Explorer 6.0 ')
	h.endheaders()
	returncode, returnmsg, headers = h.getreply()
	#print returncode
	#print returnmsg
	#print headers
	data=h.getfile().read()
	#print data
	#r1 = re.compile('\[[A-Z]*\]</b>(<) <h2 class=[^>]+><a href="([^"]+)"')
	#print r1
	#By Open-Sec - Start
	#Before Sep/14th/2008 it had h2, something changed in content retrieved from Google becuase wph (web personal history)
	r1 = re.compile('<h3 class=[^>]+><a href="([^"]+)"')
	#By Open-Sec - End
	res = r1.findall(data)
	#print res
	return res



def test(argv):
	global limit
	global file
	limit=20
	down ='a'
	if len(sys.argv) < 11:
		usage()
	try :
		opts, args = getopt.getopt(argv,"l:d:f:o:t:")
	except getopt.GetoptError:
		usage()
	for opt,arg in opts:
		if opt == '-l':
			limit = int(arg)
        	elif opt == '-d':
            		word = str(arg)
        	elif opt == '-f':
            		file = str(arg)
        	elif opt == '-o':
            		ofile = str(arg)
		elif opt =='-t':
			dir = str(arg)
	if dir == 'none':
		dir = word
	if file != 'all':
		all=[file]
	else:
		all=['pdf','doc','xls','ppt','sdw','mdb','sdc','odp','ods']
	try:
		fil = open(ofile+'.html','w')
	except:
		print "Failed"
	test=extcommand.split(" ")[0]
	if os.path.isfile(test):
		print "[+] Command extract found, proceeding with leeching"
	else:
		print "Command extract not found, please check and change the location"
		sys.exit()
	date= time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
	fil.write("<style type=\"text\/css\"><!--BODY{font-family:sans-serif;}--></style>")
	fil.write("<center><b>Meta<font color=\"#0000cc\">G</font><font color=\"#ff0000\">o</font><font color=\"#ffff00\">o</font>fil</b> results page for:</center>")
	fil.write("<center><b>"+word+"</b></center>")
	fil.write("<center>"+date+"</center>")
	fil.write("<center><a href=\"http://www.edge-security.com\">By Edge-Security</a></center>")
	fil.write("<hr>")
	fil.write('<a href="#users">Results: Go directly to resuls.</a>')
	authors=[]
	pathos=[]
	limiteinicial=limit
	for fi in all:
		file = fi
		print "[+] Searching in " + word + " for: " + file
		total = int(howmany(word))
		print "[+]Total results in google: "+ str(total)
		if total == 0:
			#pass
			print "There are NO results with extension name " + file
		else:
			fil.write("<hr>")
			fil.write("<strong><u>Searching in " + word + " for: " + file+" files.</u></strong><br><br>")
			#By Open-Sec - Start		
			#limit=limiteinicial ---> removed on Jan 22th 2014
			#print limiteinicial
			#print total
			#print limit
			if total <= limit:
				limit = total
				cant = total
			else:
				cant = limit
			print "[+]Limit: ",int(limit)
			result=[]
			#print word
			while cant <= limit:
				print "[+] Searching results: " + str(limit) +"\r"
				#By Open-Sec - End
				res = run(word,cant)
				#print "desde test"
				#print res
				#print len(res)
				for x in res:
					#print result.count(x)
					#By Open-Sec - Start 
					if result.count(x) == 0:
						#print x
						#print x[1]
						#print x.count('http')
						if x.count('http')!=0:
							result.append(x)
							#print x[1]
						else:
							pass
					#By Open-Sec - End
				cant+=20
			fil.write("<strong>Total available files: "+str(total)+" </strong><br>")
			t=0
			if os.path.exists(dir):
				print "[+] Directory "+	dir + " already exist, reusing it"
			else:
				os.mkdir(dir)
			cantidad_todo=len(result)
			contador=0
			for x in result:		
				contador+=1
				#Previous location of file URL printing
				#fil.write(x+"<br>")
				try:
					if down == "a"	:
						np = 0
						#print "res before ******************************************************"
						#print res
						# First, split based on & and then remove http:/
						# First rest just gets the first element and second one gets the second element and then print the location of file URL
						res=x.split('&')[0]
						res=res.split('://')[1]
						fil.write("http://"+res+"<br>")
						#print res
						#res=res.split("/")[1]
						# Split again to obtain just the file name
						archivo=x.split("://")[1]
						archivo=archivo.split('&')[0]
						archivo=archivo.split('/')
						#print "filename **********"
						#print archivo
						#print "res after ******************************************************"
						#print res
						leng=len(archivo)
						filename=archivo[leng-1]
						#print leng
						#print filename
						#url=x.split('&')
						#print url
						# Restore http:// for downloading and printing
						res="http://"+res
						try:
							print "\t[ "+str(contador)+"/"+str(cantidad_todo)+" ] "+ res
							if os.path.exists(dir+'/'+filename):
								pass
							else:
								#print "res**************************************************"
								#print res
								#print "dir************************************************"
								#print str(dir)
								#print "filename******************************************"
								#print str(filename)
								urllib.urlretrieve(res,str(dir)+"/"+str(filename))
						except IOError:
							print "Can't download"
							np = 1
						if np == 0:
							fil.write("<br>Local copy " + "<a href=\""+dir+"/"+filename+'\">Open</a>')
							fil.write("<br><br>Important metadata:")
							command = extcommand +' '+ dir +'/'+'"'+filename+'"'
							try:
								stdin,stderr = os.popen4(command)
							except:
								print "Error executing extract, maybe the binary path is wrong."
								fil.write('<br>')
							mac=get_mac(filename,dir)
							#From metagoofil 1.4b
							author,path=get_info_pdf(filename,dir)
							if author!="":
                                                                if authors.count(author) == 0:
                                                                        authors.append(author)
                                                                if pathos.count(path) == 0:
                                                                        pathos.append(path)
                                                        else:
                                                                pass
							#End of segmente from metagoofil 1.4b

							if file == 'pdf':
								fil.write('<pre style=\"background:#C11B17;border:1px solid;\" >')
							elif file == 'doc':
								fil.write('<pre style=\"background:#6698FF;border:1px solid;\">')
							elif file == 'xls':
								fil.write('<pre style=\"background:#437C2C;border:1px solid;\">')
							elif file == 'ppt':
								fil.write('<pre style=\"background:#E56717;border:1px solid;\">')
							else:
								fil.write('<pre style=\"background:#827839;border:1px solid;\">')
							if mac !='':
								fil.write('Mac address:' + mac +'\n' )
							else:
								pass
							for line in stderr.readlines():
								fil.write(line)
								au = re.compile('Author -.*')
								aut= au.findall(line)
								if aut != []:
									author=aut[0].split('- ')[1]
									if authors.count(author) == 0:
										authors.append(author)
								
								au = re.compile('creator -.*')
								aut= au.findall(line)
								if aut != []:
									author=aut[0].split('- ')[1]
									if authors.count(author) == 0:
										authors.append(author)

								au = re.compile('author -.*')
                                                                aut= au.findall(line)
                                                                if aut != []:
                                                                        author=aut[0].split('- ')[1]
                                                                        if authors.count(author) == 0:
                                                                                authors.append(author)

								last = re.compile('last saved by -.*')
								aut= last.findall(line)
								if aut != []:
									author=aut[0].split('- ')[1]
									if authors.count(author) == 0:
										authors.append(author)
						    		
								rev = re.compile(': Author \'.*\'')
								aut=rev.findall(line)
								if aut != []:
									author=aut[0].split('\'')[1]
									author=string.replace(author,'\'','')
									if authors.count(author) == 0:
										authors.append(author)

								pa= re.compile('worked on .*')
								pat=pa.findall(line)
								if pat !=[]:
									if pathos.count(pat) == 0:
										temp=pat[0].split('\'')[1]
										pathos.append(temp)
								pat=[]	
								pa= re.compile('template -.*')
								pat=pa.findall(line)
								if pat !=[]:
									if pathos.count(pat) == 0:
										temp=pat[0].split('-')[1]
										pathos.append(temp)
							fil.write('</pre>')
							fil.write('<hr>')
						else:
							print "Can't Download "+ x 
							fil.write("<br>Local copy, failed download :(\n")
							fil.write('<hr>')
					else:
						print "====================="
				except KeyboardInterrupt:
						print "Process Interrupted by user\n"
						sys.exit()
				t+=1
			fil.write("<strong>Total results for "+fi+": "+ str(t)+ "</strong><br>")
	fil.write('<hr>')	
	fil.write('<a name="users">')
	fil.write('<br>')
	fil.write('<b><h2>Total authors found (potential users):</h2></b>')
	fil.write('<pre style=\"background:#737ca1;border:1px solid;\">')
	print "\n"
	print "Usernames found:"
	print "================"		
	if authors != []:
		for x in authors:
				fil.write( str(x)+'<br>')
				print str(x)
	else:
		fil.write("0 users found.<br>")
	fil.write('</pre>')
	print "\n"
	print "Paths found:"
	print "============"	
	fil.write('<b><h2>Path Disclosure:</h2></b>')
	fil.write('<pre style=\"background:#c8bbbe;border:1px solid;\">')
	paty=[]
	if pathos != []:
		for x in pathos:
				temp=""
				a=x.split('\\')
				for x in a:
					if x.count('.'):
						pass
					else:
						temp=temp+x+"\\"
				if paty.count(temp):
					pass
				else:
					fil.write(str(temp)+'<br>')
					paty.append(temp)
					print temp
	else:
			 fil.write('0 path found.<br>')
	fil.write('</pre>')
	print "[+] Process finished"

if __name__ == "__main__":
        try: test(sys.argv[1:])
	except KeyboardInterrupt:
		print "Process interrupted by user.."
	except:
		sys.exit()
