#!/usr/bin/env python3

from http.server import  BaseHTTPRequestHandler, HTTPServer
import os
import subprocess
import re
#import stat
import wernicke
import answer
import spinal_reflex
from markopolo_config import *

# "port" value defined in 'markopolo_config.py' file
# "password" value defined in 'markopolo_config.py' file
 
# el ingreso debe ser asi:
# GET /PSW_venecia_PSWUSR_marcos_USRCOM_frase+a+procesar_COM HTTP/1.1
# donde: PSW_venecia_PSW define el password como -venecia-
#        USR_marcos_USR define el usuario como -marcos-
#        COM_frase+a+procesar_COM define la comunicacion entrante como -frase+a+procesar- 


def first_corrections(ingreso):
#vocales minusculas con tilde
	replacements = (
		("á", "a"),
		("é", "e"),
		("í", "i"),
		("ó", "o"),
		("ú", "u"),
		("ñ", "n"),
	)
	for a, b in replacements:
		ingreso = ingreso.replace(a, b).replace(a.upper(), b.upper())
	return ingreso

	
def getpassword(ingreso):
	#aisla el password de ingreso
	inpassword = re.sub('(^.*)PSW_', '', ingreso)
	inpassword = re.sub('_PSW(.*$)', '', inpassword)
	#ver el password
	#print('password entrante:',inpassword)
	return inpassword


def getuser(ingreso):
	#aisla el password de ingreso
	inuser = re.sub('(^.*)USR_', '', ingreso)
	inuser = re.sub('_USR(.*$)', '', inuser)
	#ver el user
	#print('user entrante:',inuser)
	return inuser


def getcom(ingreso):
	#aisla la comunicacion de ingreso
	incom = re.sub('(^.*)COM_', '', ingreso)
	incom = re.sub('_COM(.*$)', '', incom)
	#ver la comunicacion
	#print('com entrante:',incom)
	return incom


pid = str(os.getpid())
pidfile = "/tmp/markopolo.pid"
print("Main server pid process: %s" % pid)

class http_server:
    def __init__(self):
        print("Markopolo listen in port: %s" % int(port_srv))
        print('')
        server = HTTPServer(('', int(port_srv)), myHandler)
        server.serve_forever()

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        # define input in 'txtinput' variable
        txtinput = self.requestline
        
        #quita inicio y final del input
        txtinput = txtinput.replace('GET /', '')
        txtinput = txtinput.replace(' HTTP/1.1', '')
        
        # aisla password, usuario y comunicacion
        inpasswd = getpassword(txtinput)
        user = getuser(txtinput)
        com = getcom(txtinput)
        
        #testea si el password es correcto para continuar
        if (inpasswd == password):
        		#print('el password es correcto')
        		
        		#reemplaza tildes y otros caracteres no procesables como la 'ñ'
        		txtinput = first_corrections(com)
        		
        		# activa reflejos espinales
        		reflex_response = spinal_reflex.reflex(txtinput)
        		
        		#define provisoriamente el output como la salida de spinal_reflex
        		txtoutput = reflex_response[1]
        		
        		#comprueba que no sea una respuesta (ve la presencia de un archivo temporal)
        		#si es una respuesta ejecuta el archivo temporal
        		file_answer = '/tmp/markopolo-answer'
        		if (os.path.exists(file_answer)):
        			print('Incomming answer DETECTED')
        			txtoutput = answer.answerexec (file_answer,com,user)
        			os.remove(file_answer)
        			
        		else:
        			#si spinal_reflex no generó acción, el ingreso no fue una respuesta se continua con el procesamiento desde wernicke
        			if(reflex_response[0] != 'stop'):
        				print('Wernicke Area ACTIVE')
        				# define output (txtoutput) from 'wernicke' module work
        				txtoutput = wernicke.procesar(txtinput,user) #.encode("utf-8")
        
        else:
        		print('Conexion rechazada. Password incorrecto.')
        		print('')
        		txtoutput = 'Conexion rechazada. Password incorrecto.'
        		txtoutput = txtoutput.encode("utf-8")
        
        
        #Print response (txtoutput) to file.
        response_file = open('response.output','w')
        response_file.write(txtoutput.decode('utf-8'))
        response_file.close()
        #Print response (txtoutput) to client. La codificacion tiene que ser utf8 para que no genere errores
        self.wfile.write(txtoutput)
        
        return

class main:
    def __init__(self):
         self.server = http_server()
 
if __name__ == '__main__':
    m = main()
