import flask
from flask import Flask,jsonify,json
from kafka import KafkaConsumer
import sys


app = flask.Flask(__name__)
app.config["DEBUG"] = False


#    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
#    try:

@app.route("/messagesKafka/<topicName>")
def get_messagesKafka(topicName):
 bootstrap_servers = ['localhost:9092']
# topicName = 'discourseMessage'
#consumer = KafkaConsumer (tTopic3', group_id ='group1',bootstrap_servers=bootstrap_servers,auto_offset_reset = 'earliest',consumer_timeout_ms=5000)
 #consumer = KafkaConsumer ('discourseMessage', group_id ='group1',bootstrap_servers =bootstrap_servers,auto_offset_reset='earliest')
 consumer = KafkaConsumer (topicName, group_id ='group1',bootstrap_servers =bootstrap_servers,enable_auto_commit=False, auto_offset_reset='earliest',
    consumer_timeout_ms=10000, )

        # Initialize a employee list
 messageList = []
#messDict = {
# 'Le nom du Topic ': 'top',
# 'Message value': 'val'}
#messageList.append(messDict)

        # create a instances for filling up employee list
 for msg in consumer:
  messDict = {
  'Le nom du Topic ': msg.topic,
  'Message value': msg.value}
# print("Topic Name=%s,Message=%s"%(msg.topic,msg.value))
  messageList.append(messDict)
# sleep(5)
        # convert to json data
 jsonStr = json.dumps(messageList)

 #   except Exception as e:
 #    print (e)

 return jsonify(Messages=jsonStr)
#    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
app.run(debug=False, host='0.0.0.0')
