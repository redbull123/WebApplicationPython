import subprocess
from analyzeFile import enumPair, enumPairSC, enumCC, contarCC

def verificaFolder(ruta):
	try:
		subprocess.check_output('cd '+ruta, shell=True)
		result = "true"
	except Exception:
		result = "false"
	return result

def ejecutaProcess(command):
	try:
		result = subprocess.check_output(command, shell=True)
	except Exception:
		result = "Comando no ejecutado"
	return result

def ejecutaCommand(filtro,requerimiento,ruta,imsi):
	
	if filtro == "0":
		result = ejecutaProcess("/home/paco/Escritorio/python-app-web/parse_ebm_log.pl -e "+requerimiento+" -d "+ ruta ) 
		result_form = "@".join(result.split("\n"))
	elif filtro == "1":
		result = ejecutaProcess("/home/paco/Escritorio/python-app-web/parse_ebm_log.pl -e "+requerimiento+" -c "+imsi+" -d "+ ruta)  
		result_form = "@".join(result.split("\n"))
	elif filtro == "2":
		flag = 0
		cc =""
		ssc=""
		for word in imsi.split("@"):
			if flag == 0 :
				cc = word
			elif flag == 1 :
				ssc = word
			flag = flag + 1
		result = ejecutaProcess("/home/paco/Escritorio/python-app-web/parse_ebm_log.pl -e "+requerimiento+" -c "+cc+" -z "+ssc+" -d "+ ruta)
		result_form = "@".join(result.split("\n"))
	elif filtro == "3":
		flag = 0
		cause =""
		for word in imsi.split("@"):
			if flag == 0 :
				cause = word
			elif flag == 1 :
				tac = word
			flag = flag + 1
		result = ejecutaProcess("/home/paco/Escritorio/python-app-web/parse_ebm_log.pl -e "+requerimiento+" -c "+cause+" -d "+ ruta) 
		result_form = "@".join(result.split("\n"))
	return result_form

def methodsToRead(result_form,keyWord,imsi,ruta,requerimiento):
	numberCC = enumCC(result_form,keyWord)
	cantCC = contarCC(numberCC,keyWord)
	outPut = "Ruta del directorio : "+ruta + "@"+ "Parametro a Buscar o Contar: "+imsi +"@"+ "Parametro de Filtro: "+requerimiento + "@"+cantCC
	return outPut

def ejecutaScript(ruta,imsi,requerimiento,cantidad,filtro):
	try:
		var = verificaFolder(ruta)
		if var == "true":
			if requerimiento == "sImsi":
				result = subprocess.check_output('/home/paco/Escritorio/python-app-web/parse_ebm_log.pl -i '+imsi+' -d '+ ruta , shell=True)
				outPut = "@".join(result.split("\n"))

			elif requerimiento !=  "sImsi" and requerimiento != "causeCode" :
				result_form = ejecutaCommand(filtro,requerimiento,ruta,imsi)
				if cantidad == "1":
					keyWord = "cause_code"
					outPut = methodsToRead(result_form,keyWord,imsi,ruta,requerimiento)
				elif cantidad == "2":
					keyWord = "tac"
					outPut = methodsToRead(result_form,keyWord,imsi,ruta,requerimiento)
				elif cantidad == "3":
					keyWord = "rac"
					outPut = methodsToRead(result_form,keyWord,imsi,ruta,requerimiento)
				elif cantidad == "4":
					keyWord = "lac"
					outPut = methodsToRead(result_form,keyWord,imsi,ruta,requerimiento)
				elif cantidad == "5":
					keyWord = "tac"
					keyWord2 = "eci"
					flag = 0
					tac = ""
					for word in imsi.split("@"):
						if flag == 0 :
							cause = word
						elif flag == 1 :
							tac = word
						flag = flag + 1

					numberCC = enumPair(result_form,keyWord,keyWord2,tac)
					cantCC = contarCC(numberCC,keyWord2)
					outPut = "Ruta del directorio : "+ruta + "@"+ "Parametro a Buscar o Contar: "+imsi +"@"+ "Parametro de Filtro: "+requerimiento + "@"+cantCC
				elif cantidad == "6":
					keyWord = "event_result"
					keyWord2 = "cs_fallback_service_type"
					flag = 0
					event = ""
					cs = ""
					for word in imsi.split("@"):
						if flag == 0 :
							event = word
						elif flag == 1 :
							cs = word
						flag = flag + 1
					numberCC = enumPairSC(result_form,keyWord,keyWord2,event,cs)
					cantCC = contarCC(numberCC,keyWord)
					outPut = "Ruta del directorio : "+ruta + "@"+ "Parametro a Buscar o Contar: "+imsi +"@"+ "Parametro de Filtro: "+requerimiento + "@"+cantCC

				elif cantidad == "0":  
					outPut = result_form
		else :
			outPut = "El directorio no existe"
	except Exception as err:
		outPut = "No se ejecuto el script"
	return outPut

