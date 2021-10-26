import paramiko


def conexionSSH():
	global process
	paramiko.util.log_to_file('./message.log') # Change for a file on the server.
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh_client.connect("1.1.1.1","22",username="example",password="example") # Change for the firewall IP address
	except Exception:
		ssh_client.close()
		return "Ocurrio un error estableciendo la conexion. \n"
	return ssh_client