import logging
import azure.functions as func
import requests
from pymongo import MongoClient

def send_line_notify(message):
    token = 'ACfI4LbD8JP5KhDqsPcLoYnV10Gw7Ho9S6CKCz6REXH'
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': message}
    response = requests.post(url, headers=headers, data=data)
    logging.info(response.text)

app = func.FunctionApp()

@app.schedule(schedule="0 */1 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_temp(myTimer: func.TimerRequest) -> None:
    client = MongoClient('mongodb+srv://nisamanee:passw0rd!@ct-pj-iot.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')
    db = client['Project']
    collection = db['Temp']
    cursor = collection.find().sort("_id", -1).limit(1)
    last_document = next(cursor, None)
    Temp = last_document.get("Status")

    if Temp >= 27:
        message = "\nTemperature Alert\nTemp now : " + str(Temp) + " ํC" + "\nStatus : Red ("+str(Temp)+">27 ํC)" 
        send_line_notify(message)
    else:
        logging.info("Not Alert")

@app.schedule(schedule="0 */1 * * * *", arg_name="myTimer1", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_humi(myTimer1: func.TimerRequest) -> None:
    client = MongoClient('mongodb+srv://nisamanee:passw0rd!@ct-pj-iot.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')
    db = client['Project']
    collection = db['Humidity']
    cursor = collection.find().sort("_id", -1).limit(1)
    last_document = next(cursor, None)
    Humi = last_document.get("Status")

    if Humi >= 55:
        message = "\nHumidity Alert\nHumi now : " + str(Humi) + " %H" + "\nStatus : Red ("+str(Humi)+">55 %H)"
        send_line_notify(message)
    else:
        logging.info("Not Alert")

