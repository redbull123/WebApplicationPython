from flask import Flask
from flask import render_template
from flask import request
from models import User
from app import app
from app import db
import archivosEbm
import rulesApp
import extractFiles


@app.route("/register",methods=["GET","POST"])
def register():
	if request.method == 'POST': 	
		db.create_all()
		if 'secret' == request.form['inputAuthen']:
			if request.form['inputPassword'] == request.form['inputRpassword']:
				user=User(username=request.form['username'],password=request.form['inputPassword'])
				if (User.query.filter_by(username=request.form['username']).first()):
					return render_template('register.html', variable = "Usuario ya Existe")
				else:
					db.session.add(user)
					db.session.commit()	
					return render_template('login.html', variable = "Usuario Registrado")
			else:
				return render_template('register.html', variable = "No coincide Password")
		else:
			return render_template('register.html', variable = "Incorrecto Autenticacion")
	else:
		return render_template('register.html')

@app.route("/",methods=["GET","POST"])
def login():
	db.create_all()
	if request.method == 'POST':
		if (User.query.filter_by(username=request.form['username'], password = request.form['password']).first()):
			return render_template('menu.html')
		else:
			return render_template('login.html', variable = "Usuario o Password Incorrecto")
	else:
		return render_template('login.html')
@app.route("/menu",methods=["GET","POST"])
def menu():
	db.create_all()
	if request.method == 'POST':
		route_html = request.form['select']
		if route_html == "Corporativo":
			return render_template('login.html')
		else:
			return render_template('ebm.html')
	else:
		return render_template('login.html')

@app.route("/ebm", methods=["GET","POST"])
def ebm():
	if request.method == 'POST':

		sgsn = request.form['select']
		fecha = request.form['fecha']
		hora = request.form['hora']
		minuto = request.form['minuto']
		imsi = request.form['imsi']
		cantidad = request.form['cantidad']
		requerimiento = request.form['requerimiento']
		filtro = request.form['filtro']
		extension = fecha+"-"+hora+minuto
		archivos = "A"+fecha+"."+hora+minuto
		
		if sgsn != "option":
			if hora == "Hora":
				outPut = "Empty"
				log = "Seleccione un valor para hora"
			else:
				if minuto =="Minuto":
					log = "Seleccione un valor para minuto"
					outPut = "Empty"
				else:
					log = rulesApp.rulesEbm(requerimiento,cantidad,filtro)
					if log == "valid":
						log = extractFiles.validaFolder(extension,sgsn,archivos)
						if log == "sucess$":
							ruta = "/home/paco/Escritorio/python-app-web/sgsn"+sgsn+"/"+extension+"/" 
							outPut= archivosEbm.ejecutaScript(ruta,imsi,requerimiento,cantidad,filtro)
						elif log != "sucess$":
							outPut = "No hay logs para la fecha indicada en el Servidor"
					elif log != "valid":
						outPut = "No selecciono una combinacion Valida"

		elif sgsn == "option":
			log = "Seleccione un SGSN"
			outPut = "Empty"
		return render_template('ebm.html', variable = outPut, out_log = log)
	else:
		return render_template('login.html')


@app.route("/srx",methods=["GET","POST"])
def home():
	process = ""
	texto =""
	db.create_all()
	if request.method == 'POST':
				var = request.form['select']
				if var == 'option':
					texto = 'Seleccione un Campo'
					process = ''
				if var == 'Fase I':
					ip = request.form['ip']
					command= 'show security ike security-associations '+ ip +' | no-more'
					ssh_client = conexionSSH()
					if (ssh_client == "Ocurrio un error estableciendo la conexion. \n"):
						texto="No se ejecuto el comando {} por problemas de conexion".format(command)
					else:
						process = process + " Executing {}...\n".format(command)
						stdin, stdout, stderr = ssh_client.exec_command(command)
						texto = stdout.readlines()
						ssh_client.close()
						process = process + " Se desactivo la conexion SSH con exito.\n"

				if var == 'Fase II':
					ip = request.form['ip']
					command = 'show security ipsec inactive-tunnels vpn-name tunnel-'+ ip +' | no-more'
					ssh_client = conexionSSH()
					if (ssh_client == "Ocurrio un error estableciendo la conexion. \n"):
						texto="No se ejecuto el comando {} por problemas de conexion".format(command)
					else:
						process = process + " Executing {}...\n".format(command)
						stdin, stdout, stderr = ssh_client.exec_command(command)
						texto = stdout.readlines()
						ssh_client.close()
						process = process + " Se desactivo la conexion SSH con exito.\n"

				if var == 'Corporativo':
					ip = request.form['ip']
					command = 'show configuration | display set | match gateway-'+ ip +' | match address | no-more'
					ssh_client = conexionSSH()
					if (ssh_client == "Ocurrio un error estableciendo la conexion. \n"):
						texto="No se ejecuto el comando {} por problemas de conexion".format(command)
					else:
						process = process + " Executing {}...\n".format(command)
						stdin, stdout, stderr = ssh_client.exec_command(command)		
						texto = stdout.readlines()
						ssh_client.close()
						process = process + " Se desactivo la conexion SSH con exito.\n"
				return render_template('srx.html', status = process, variable = texto)
	else:
		return render_template('login.html')