import socket   
import sys 
import time
from mongoconnection import mongoConnection, setHost, setDB
from fulltrack2 import readBaseFulltrack2
from hytera import readBaseHytera

HOST = "" #IP do mapa
PORT = 11001
API = ""

HELP = ("\tpython3 file [option] [arguments]\n\nUse:\n" + 
        " -a, --api\t define API\n" +
        " -h, --host\t define host IP\n" +
        " -d, --db\t define mongo-database name\n" +
        " -m, --dbhost\t define mongo host IP\n" +
		"\n\tUse the database or config file to set the parameters:\n" +
		"\t\t Hytera: Only config file\n" +
		"\t\t Fulltrack2: Config file or mongo-database\b")

for i, argv in enumerate(sys.argv):
    try:
        if argv == '--api' or argv == '-a':
            API = sys.argv[i+1].lower()
        if argv == '--host' or argv == '-h':
            HOST = sys.argv[i+1]
        if argv == '--db' or argv == '-d':
            setDB(sys.argv[i+1])
            DB = mongoConnection()
        if argv == '--dbhost' or argv == '-m':
            setHost(sys.argv[i+1])
        if argv == '--help':
            print(HELP)
            sys.exit(0)
    except Exception as error:
        print("Error: " +  str(error))
        print(HELP)
        sys.exit(0)

#carros= [[105,-17.864260, -39.491790,"True"],[5, -17.864357, -39.491860,"True"],[100, -17.864319, -39.491908, "False"],[101, -17.864286, -39.491932,"True"],[102,-17.864302, -39.491845,"False"],[666, -17.864245, -39.491871,"True"]]

def connectSaffira():
	count = 0
	print("Waiting connection...")
	try:
		con, cliente = tcp.accept()		
	except:
		print ("Accept:",sys.exc_info()[1])
		return	
	print ('Conectado com ', cliente)
	while True:
		while True:	
			if	API == 'fulltrack2': 
				carros = readBaseFulltrack2()
			elif API == 'hytera': 
				carros = readBaseHytera()
			else:
				print("There's no support for this")
				break
			if not carros:
				time.sleep(3)
				continue
			else: break
		msg = str(carros)
		print("Enviando:",msg)
		print("*********************************************************************")
		while True:
			try:
				con.send(msg.encode())
				break
			except:
				print ("Send:", sys.exc_info()[1])
				count =count + 1
				if(count == 5): return
				time.sleep(3)
		time.sleep(10)

while True:
	try:
		tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if tcp != -1: break
	except:
		print ("Socket:", sys.exc_info()[1])
		time.sleep(3)

orig = (HOST, PORT)
timer = 0
while True:
	try:
		resBind = tcp.bind(orig)
		timer = 0
		if resBind != -1: break
	except:
		print (timer,"Bind:", sys.exc_info()[1])
		time.sleep(3+timer)
		timer = timer + 1
	
while True:
	try:
		resListen = tcp.listen(1)
		if resListen==None or resListen != -1: break
	except:
		print ("Listen:", sys.exc_info()[1])
		time.sleep(3)
while True:
	connectSaffira()
	time.sleep(3)


