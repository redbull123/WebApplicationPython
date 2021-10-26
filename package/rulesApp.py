def rulesEbm(requerimiento,cantidad,filtro):
	if requerimiento == "sImsi":
		if filtro == "0" and cantidad == "0":
			log = "valid"
		else :
			log ="reject"
	elif requerimiento != "sImsi":
		if filtro == "0":
			if cantidad == "0":
				log = "valid"
			elif cantidad == "1":
				log = "valid"
			elif cantidad == "6":
				log = "valid"
			else:
				log ="reject"
		elif filtro == "1":
			if cantidad == "0":
				log = "valid"
			elif cantidad == "2":
				log = "valid"
			elif cantidad == "3":
				log = "valid"
			elif cantidad == "4":
				log = "valid"
			elif cantidad == "6":
				log = "valid"
			else:
				log ="reject"

		elif filtro == "2":
			if cantidad == "0":
				log = "valid"
			elif cantidad == "2":
				log = "valid"
			elif cantidad == "3":
				log = "valid"
			elif cantidad == "4":
				log = "valid"
			else:
				log ="reject"
		elif filtro == "3":
			if cantidad == "5":
				log = "valid"
			else:
				log ="reject"
	return log