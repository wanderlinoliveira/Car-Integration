
import requests
import json
from mongoconnection import getVeiculos, getFulltrack2Keys, getVeiculosFromRecusos, getDBConnection
from config import fulltrack2Keys, fulltrack2List, fulltrack2url

configured = False
url = fulltrack2url
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
        lista = getVeiculos() 
    else:
        print("Picking keys and list from config file")
        keys = fulltrack2Keys
        headers = {
            'apiKey': keys["apiKey"],
            'secretKey':  keys["secretKey"]
        }
        lista = fulltrack2List

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
                ras_vei_veiculo = carro["ras_vei_veiculo"].strip()
                if any(ras_vei_veiculo in s for s in lista):
                    if(ras_vei_veiculo.isdigit()):
                        cursor["id"] = ras_vei_veiculo
                    else:
                        ras_vei_id = carro["ras_vei_id"].strip()
                        cursor["id"] = ras_vei_id						
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
