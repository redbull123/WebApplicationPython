from scp import SCPClient
import paramiko
import subprocess
import confiAuth

def extraerFileEBM(archivos,sgsn,extension,ip,user, pwd):
	try: 
	    destinationPathscp = "/home/paco/Escritorio/python-app-web/sgsn"+sgsn+"/"+extension+"/"
        remotePathscp = "/logs/ebs/ready/"+archivos+"*"
        subprocess.check_output('sshpass -p '+pwd+' scp '+user+'@'+ip+':'+remotePathscp+' '+destinationPathscp, shell=True)
		out = "sucess$"
	except Exception as err:
		out = "failed"
	return out

def validaFolder(extension,sgsn,archivos):
	try:
		subprocess.check_output('cd /home/paco/Escritorio/python-app-web/sgsn'+sgsn+'/'+extension+'/', shell=True) 
		result = "sucess$"
	except Exception:
        
	        subprocess.check_output('mkdir /home/paco/Escritorio/python-app-web/sgsn'+sgsn+'/'+extension+'/', shell=True)
        	ip, user, pwd = confiAuth.getAuth(sgsn)	
        	result = extraerFileEBM(archivos,sgsn,extension,ip,user,pwd)
	
    	return result
