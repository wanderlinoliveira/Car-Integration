
import requests
import json
from mongoconnection import getFulltrack2Veiculos, getFulltrack2Keys, getFulltrack2VeiculosFromDevices, getDBConnection, isListOriginDevices
from config import fulltrack2

configured = False
url = fulltrack2["url"]
headers = {}
lista = []

def setConfiguration():
    DBConnection = getDBConnection()
    global headers
    global lista
    if DBConnection:
        print("Picking keys and list from database")
        keys = getFulltrack2Keys()        
        headers = {
            'apiKey': keys["apiKey"],
            'secretKey':  keys["secretKey"]
        }
        if(not isListOriginDevices()):
            lista = getFulltrack2Veiculos()
        else:
            lista = getFulltrack2VeiculosFromDevices()
    else:
        print("Picking keys and list from config file")
        keys = fulltrack2["keys"]
        headers = {
            'apiKey': keys["apiKey"],
            'secretKey':  keys["secretKey"]
        }
        lista = fulltrack2["tracklist"]

def readBaseFulltrack2():
    global configured
    if not configured:
        setConfiguration()
        configured = True              
    try:
        global headers
        r = requests.get(url,headers=headers)
        r_json = r.json()
    except Exception as error:
            print("readBaseFulltrack2 Error: ", error)
            return -1
    data = []
    for carro in r_json["data"]:
            cursor = {}
            try:
                if(not isListOriginDevices()):
                    identifier = carro["ras_vei_id"].strip()
                else:
                    identifier = carro["ras_vei_veiculo"].strip()
                if identifier in lista:
                    cursor["id"] = carro["ras_vei_id"].strip()						
                    cursor["latitude"] = carro["ras_eve_latitude"]
                    cursor["longitude"] = carro["ras_eve_longitude"]
                    if carro["ras_eve_gps_status"] == "0":
                        cursor["status"] = "offline"                #Veiculo offline (Veiculo offline default cinza)
                    elif carro['ras_eve_ignicao'] == "0":        
                        cursor["status"] = "red"                    #Veiculo desligado/parado
                    elif carro['ras_eve_velocidade'] != "0":
                        cursor["status"] = "blue"                   #Veiculo em movimento
                    else:
                        cursor["status"] = "online"                 #Veiculo parado e ligado (Veiculo online default verde)
                    cursor["vel"] = carro['ras_eve_velocidade']
                    data.append(cursor)
            except:
                continue
    return data

def testFulltrack2(saveInFile=False):
    setConfiguration()
    try:
        global headers
        r = requests.get(url,headers=headers)
        r_json = r.json()
        for carro in r_json["data"]:
            print(carro["ras_vei_id"],carro["ras_vei_placa"])
    except Exception as error:
            print("readBaseFulltrack2 Error: ", error)
            return -1
    if saveInFile:
        f = open("jsontest.py", "w")
        f.write(str(r_json["data"]))
    #print(r_json["data"])

def getIdByVeiculo(saveInFile=False):
    setConfiguration()
    try:
        global headers
        r = requests.get(url,headers=headers)
        r_json = r.json()
    except Exception as error:
            print("readBaseFulltrack2 Error: ", error)
            return -1
    data = {}
    for carro in r_json["data"]:
        ras_vei_veiculo = carro["ras_vei_veiculo"].strip()
        if ras_vei_veiculo in fulltrack2["ras_vei_veiculoList"]:
            data[ ras_vei_veiculo ] = carro["ras_vei_id"].strip()
    if saveInFile:
        f = open("jsontest.py", "w")
        f.write(str(data))
    print(data)
