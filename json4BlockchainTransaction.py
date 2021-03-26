import flask
from flask import Flask,jsonify,json
from flask import request
#import json
import requests




#lancer le module Flask à l'execution de l'api
app = flask.Flask(__name__)

#pas d'affichage des details des messages d erreur
app.config["DEBUG"] = False

#route de POST depuis le WEB
@app.route('/CO2Json2Blockchain', methods=['POST'])

def jsonning_CO2value():
 bootstrap_servers = ['localhost:9092']

#valeurs recuperees de orchestre
 payload = request.data
# print("valeur de CO2 a integrer", payload)
 payload = payload.decode("utf-8")
 jdata = json.loads(payload)
 CO2 = 55
 print(payload)

 id = jdata["discourse_id"]
 CO2 = jdata["valeur_CO2"]
 date = jdata["modified_at"]
# CO2 = payload.decode("utf-8")
 CO2 = int(CO2)
 CO2 = hex(CO2)
 id = hex(id)
 
 print(CO2, id)
 model = {
 "jsonrpc":"2.0",
 "date":date
 "method":"eth_sendTransaction",
 "params":[{
 "from": "0xedabf979f8337238f4da8091e8181696b8a9561e",
 "to": "0x4bf108c16b569d7296b24154ebad626fa9104a6e",
 "gas": "0x76c0",
 "gasPrice": "0x9184e72a000",
 "value":CO2,
 "data": "0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"
 }],
 "id":id
 }

 model = json.dumps(model)
 print("valeur de CO2 integree ds json : ", model)
 return(model)

if __name__ == '__main__':

 app.run(debug=False, port=5005, host='0.0.0.0')

