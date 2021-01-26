import requests
import json
from config import multiPortal
from datetime import datetime
token = None
expiration = 0

def handShake():
    global token
    global expiration
    url = "http://apiv1.1gps.com.br/seguranca/logon"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "username": multiPortal["username"],
        "password": multiPortal["password"],
        "appid": multiPortal["appid"],
        "token": None,
        "expiration": None
    }
    try:
        r = requests.post(url, headers=headers, data=json.dumps(body))
        response = json.loads(r.text)['object']
        token= response['token']
        expiration= response['expiration']
        print("Hands shaked")
        print(expiration)
        return True
    except Exception as error:
        print("Hand Shake Error:", error)
        return -1

def listarVeiculos():
    global token
    url = "http://apiv1.1gps.com.br/veiculos"
    headers = {
        "Content-Type": "application/json",
        "token": token
    }
    try:
        r = requests.post(url, headers=headers)
        response = json.loads(r.text)['object']
        for carros in response:
            print("********************************")
            print("id", carros["id"])
            print("frota", carros["frota"])
            print("placa", carros["placa"])
    except Exception as error:
        print("Listar Veiculos Error: ", error)
        return -1

def ultimaPosicao():
    global token
    url = "http://apiv1.1gps.com.br/posicoes/ultimaPosicao"
    headers = {
        "Content-Type": "application/json",
        "token": token
    }
    try:
        r = requests.post(url, headers=headers)
        response = json.loads(r.text)['object']
        data = []
        now = datetime.now()
        for vehicle in response:
            carro = {}
            carro["id"]= vehicle["id"]
            carro["latitude"]= 0
            carro["longitude"]= 0
            #carro["placa"]= vehicle["frota"] #placa?
            #carro["frota"]= vehicle["frota"] 
            #carro["placa"]=  vehicle["placa"]
            dispositivos = vehicle["dispositivos"]
            for dips in dispositivos:
                if(not dips["posicoes"]):
                    continue
                for info in dips["posicoes"]:
                    if info["componentes"][0]['nome']:
                        carro["latitude"]=  info["latitude"]
                        carro["longitude"]= info["longitude"]
                        carro["vel"]= info["velocidade"]
                        date_time = datetime.fromtimestamp(int(info["dataProcessamento"]/1000))
                        carro["dataProcessamento"] = date_time.strftime("%d/%m/%Y, %H:%M:%S")
                        if int(now.timestamp() - int(info["dataProcessamento"]/1000)) > 300:
                            carro["status"]= "offline"
                        else:
                            componentes = info["componentes"]
                            for comp in componentes:
                                if(comp["nome"] == "Ignicao"):
                                    if(int(comp["valor"]) != 0):
                                        carro["status"]= "online"
                                    else:
                                        carro["status"]= "red"
            data.append(carro)
        return data
    except Exception as error:
        print("Get última posição Error: ", error)
        handShake()
        return -1

def readBaseMultiPortal():
    if token or handShake() is not -1:
        data = ultimaPosicao()
        return data
    else:
        return -1