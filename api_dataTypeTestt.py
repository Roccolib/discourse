import flask
from flask import Flask,jsonify,json
from kafka import KafkaProducer
from flask import request
import json
import base64


#lancer le module Flask à l'execution de l'apli 
app = flask.Flask(__name__)

#pas d'affichage des details des messages d erreur
app.config["DEBUG"] = True

#decrire l'acces a partir de root/messahesKafka limité a la fonction POST depuis le WEB
@app.route('/dataType',  methods=['POST'])

#declarer fonction(s)
def post_messagesKafka():
 topicName = request.headers.get('topicName')
 bootstrap_servers = ['localhost:9092']

#recherche d'entete 'Content-Type' annoncant le type de contenu du body
 if 'Content-Type' in request.headers:
     print('bonjour serveur')

#recherche du contenu de l'entete 'Content_Type'
     headval = request.headers.get('Content-Type')
     print("pour information, mon entete s'appelle :",(headval))     


#Si 'value' de Header est de type Json alors envoyer le contenu vers Kafka
     if 'application/json' in headval: 
         json_data = request.json
         producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),bootstrap_servers=bootstrap_servers)
         attente = producer.send(topicName, json_data)
         result = attente.get(timeout=0.1)
         return("json intégré"),200 

#Si 'value' de Header est de type Text, alors envoyer le contenu vers Kafka
     elif 'text/plain' in headval:
          data = request.get_data()
 #          print(data)
          producer = KafkaProducer(bootstrap_servers='localhost:9092')
          producer.send(topicName, (data))
          attente = producer.send(topicName, data)
          result = attente.get(timeout=0.1)
          return("txt intégré"),200

#Si le contenu de Header est de type Image, alors transformer le contenu en bytes-like object puis envoye a Kafka
     elif 'image/jpeg' in headval:
          data = request.get_data()
          jpg_as_text = base64.b64encode(data)
         # print(jpg_as_text)
          producer = KafkaProducer(bootstrap_servers='localhost:9092')
          producer.send(topicName, (jpg_as_text))
          attente = producer.send(topicName, jpg_as_text)
          result = attente.get(timeout=0.5)
          return('image integree')
#         print('C une image')
#Si le contenu de Header est different des 3 valeurs precedentes, alors annoncer qu'il n'est pas pris en compte
     return("payload format not supported yet darling")
 else:
#Si Header 'Content-Type' n'est pas present, alors rien ne peut etre importe
     return('Content-Type is missing !payload cannot be processed')


# tire la chasse en cas de blocage plus haut
# producer.flush()


app.run(debug=False, host='0.0.0.0')

