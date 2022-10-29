import swagger_ui_bundle
import connexion
import os
import logging
import logging.config
import yaml
import uuid
import json
from pykafka import KafkaClient
import datetime
from connexion import NoContent
import requests

with open('.\Api project\Receiver/app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
with open('.\Api project\Receiver/log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


def postAuction(body):
    trace = str(uuid.uuid4())
    body["traceId"] = trace
    logging.info("Received event postAuction request with a trace id of " + trace)
    client = KafkaClient(hosts=f'${app_config["events"]["hostname"]}:${app_config["events"]["port"]}')
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = { "type": "postAuction",
            "datetime" :
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    # logger.info('Returned postAuction event response(Id: ' + trace + ') with status ' + str(x.status_code))
    logger.info('Returned postAuction event response(Id: ' + trace + ') with status 201 i hope')

def bidAuction(body):
    trace = str(uuid.uuid4())
    body["traceId"] = trace
    logging.info("Received event bidAuction request with a trace id of " + trace)
    client = KafkaClient(hosts=f'${app_config["events"]["hostname"]}:${app_config["events"]["port"]}')
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = { "type": "bidAuction",
            "datetime" :
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    # logger.info('Returned postAuction event response(Id: ' + trace + ') with status ' + str(x.status_code))
    logger.info('Returned bidAuction event response(Id: ' + trace + ') with status 201 i hope')

    return "response", 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
logger = logging.getLogger('basicLogger')

if __name__ == "__main__":

    app.run(port=8080)