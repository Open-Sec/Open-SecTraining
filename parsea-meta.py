#filepath = 'tmp.lst'
#Usage : python parsea-meta.py path_to_directory_with_files > report_name.lst

import os
import sys

#path = '.'
path = sys.argv[1]

for file in os.listdir(path):
    current = os.path.join(path, file)
    filename, file_extension = os.path.splitext(current)
    if os.path.isfile(current) and file_extension == '.pdf':
        #cmd = "pdftk " + current + " dump_data > tmp.lst"
        cmd = "exiftool " + current + "> tmp.lst"
        print('\n')
        print("Procesando : ",current)
        os.system(cmd)
        data = open("tmp.lst")
        line = data.readline()
        while line:
            #print(line)
            if "Creator Tool" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Creado con : ",line.split(":")[-1:])
            if "Producer" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Generado con : ",line.split(":")[-1:])
            if "Author" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Autor : ",line.split(":")[-1:])
            line = data.readline()
    listnew = ['.xlsx', '.docx']
    if os.path.isfile(current) and file_extension.lower() in listnew:
        #cmd = "pdftk " + current + " dump_data > tmp.lst"
        cmd = "exiftool " + current + "> tmp.lst"
        print('\n')
        print("Procesando : ",current)
        os.system(cmd)
        data = open("tmp.lst")
        line = data.readline()
        while line:
            #print(line)
            if "Creator" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Autor : ",line.split(":")[-1:])
            if "Last Modified By" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Modificado por : ",line.split(":")[-1:])
            if "Application" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Creado con : ",line.split(":")[-1:])
            line = data.readline()
    listold = ['.xls', '.doc']
    if os.path.isfile(current) and file_extension.lower() in listold:
        #cmd = "pdftk " + current + " dump_data > tmp.lst"
        cmd = "exiftool " + current + "> tmp.lst"
        print('\n')
        print("Procesando : ",current)
        os.system(cmd)
        data = open("tmp.lst")
        line = data.readline()
        while line:
            #print(line)
            if "Author" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Autor : ",line.split(":")[-1:])
            if "Last Modified By" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Modificado por : ",line.split(":")[-1:])
            if "Comp Obj User Type" in line:
                #line2 = data.readline()
                #print("Entro")
                print("Creado con : ",line.split(":")[-1:])
            line = data.readline()

