import flask
from flask import Flask,jsonify,json
from kafka import KafkaProducer
from flask import request
import json
import base64
import requests


#lancer le module Flask à l'execution de l'api
app = flask.Flask(__name__)

#pas d'affichage des details des messages d erreur
app.config["DEBUG"] = True

#decrire l'acces a partir de root/messahesKafka limité a la fonction POST depuis le WEB
@app.route('/messageBroker',  methods=['POST'])

#declarer fonction(s)
def post_messageBroker():

 bootstrap_servers = ['localhost:9092']


#variables recuperees
 data = request.data
 topicName = request.headers.get('topicName')
# topicNameR = request.headers.get('topicNameR')
 contentType = request.headers.get('contentType')

#Si 'value' de Header est de type Json alors envoyer le contenu vers Kafka
 if contentType == 'application/json':
     producer = KafkaProducer(bootstrap_servers = 'localhost:9092', request_timeout_ms=1)
#     producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), bootstrap_servers='localhost:9092')
     attente = producer.send(topicName, data)
     result = attente.get(timeout=0.5)
     producer.flush()
     print ("L ENVOI VERS KAFKA OK POUR JSON", contentType)
     return("json processed"),200

#Si 'value' de Header est de type Text, alors envoyer le contenu vers Kafka
 elif contentType == 'text/plain':
     producer = KafkaProducer(bootstrap_servers='localhost:9092')
     attente = producer.send(topicName, data)
     result = attente.get(timeout=0.5)
     producer.flush()
     print ("text ok ")
     return("text processed"),200

#Si le contenu de Header est de type Image, alors transformer le contenu en bytes-like object puis envoye a Kafka
 elif 'image/jpeg' in contentType:
     data = data.encode("utf-8")
     jpg_as_text = base64.b64encode(data)
     producer = KafkaProducer(bootstrap_servers='localhost:9092')
     producer.send(topicName, (jpg_as_text))
     attente = producer.send(topicName, jpg_as_text)
     result = attente.get(timeout=0.5)
     producer.flush()
     return('image processed')

 else:
     contentType = "text/plain"
     print("data au mauvais format recuperes pour text", data)
     producer = KafkaProducer(bootstrap_servers='localhost:9092')
     attente = producer.send(topicNameR, data)
     result = attente.get(timeout=0.5)
     producer.flush()
     print("payload format not supported yet darling")
     return("mauvais format"), 406


app.run(debug=False, port=5001, host='0.0.0.0')

