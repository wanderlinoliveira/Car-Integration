import pymssql
import datetime
from config import hyteraHost, hyteraUser, hyteraPassword

def readBaseHytera():
	try:
		connection = pymssql.connect(host=hyteraHost, user=hyteraUser, password=Hyterapassword) #ip servidor Hytera
		cursor = connection.cursor()
	except:
		print("Connct", sys.exc_info()[1])
		return -1
	cursor = connection.cursor()
	sql = ('SELECT DISTINCT DeviceID FROM [RDS].[dbo].[GpsInfo]')
	cursor.execute(sql)
	ids = cursor.fetchall()
	data = []
	for id in ids:
		sql2 = ('SELECT DISTINCT [DeviceID] ,[Lontitude] ,[Latitude] ,[RecvGpsTime] ,[HappenTime] ,[Speed] FROM[RDS].[dbo].[GpsInfo] WHERE RecvGpsTime =(SELECT MAX(RecvGpsTime) FROM [RDS].[dbo].[GpsInfo] WHERE DeviceID=' + str(id[0]) + ');')
		cursor.execute(sql2)
		data.append(cursor.fetchall())
	carsTimr = {}
	veiculos = {}
	for dt in data:
		for each in dt:
			car = {}
			car["id"] = str(each[0])
			car["longitude"] = str(each[1]) 
			car["latitude"] = str(each[2])
			car["vel"] = str(each[5]) 
			time = each[3]
			delta = datetime.datetime.now() - time
			if delta.total_seconds() < 60*10:
				car["status"] = "online" 
			else:
				car["status"] = "offline" 
			if carsTimr.get(str(each[0])): #Tratar carros recebidos mais de uma vez
				if time > carsTimr[str(each[0])]: #Pegar info mais recente
					veiculos[str(each[0])] = car
					carsTimr[str(each[0])] = time
			else:	
				veiculos[str(each[0])] = car
				carsTimr[str(each[0])] = time
	return veiculos