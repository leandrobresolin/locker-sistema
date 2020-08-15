from django.core.management.base import BaseCommand
from django.utils import timezone

import datetime
import optparse
import json

import paho.mqtt.client as mqtt

from binascii import hexlify
from locker.models import User, Device

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "MQTT Service"
    
    TOPICO_STATUS = "/unisal/lorena/projeto/2020/status/"
    TOPICO_SERVER = "/unisal/lorena/projeto/2020/server/"
    
    client = mqtt.Client(client_id="lele_locker_test")

    def add_arguments(self, parser):
        parser.add_argument('broker', type=str, help='Endereço do Broker.')
        parser.add_argument('port', type=int, help='Porta de comunicação do Broker.')

    def handle(self, *args, **options):
        broker = options['broker']
        port = options['port']
        if broker != "":
            if port >= 0 and port <= 65535:
                
                self.client.on_connect = self.on_connect
                self.client.on_message = self.on_message
                self.client.on_disconnect = self.on_disconnect
                self.client.connect(broker, port)
                self.client.subscribe(self.TOPICO_STATUS)
                self.client.loop_forever()
                
            else:
                logger.debug('{0} - Error: Port number is invalid!'.format(self.dateTimeStamp()))
                logger.debug('{0} - Status: Server is not running!'.format(self.dateTimeStamp()))
                #print ('%s - Status: Server is not running!' % (dateTimeStamp()))
        else:
            logger.debug('{0} - Error: Broker address cannot be empty!'.format(self.dateTimeStamp()))
            logger.debug('{0}- Status: Server is not running!'.format(self.dateTimeStamp()))

    def on_connect(self, client, userdata, flags, rc):
        logger.debug('%s - Status: Connected!' % (self.dateTimeStamp()))
        
    def on_disconnect(self, client, userdata, rc):
        logger.debug('%s - Status: Disconnected!' % (self.dateTimeStamp()))
  
    def on_message(self, client, obj, msg):
        #logger.debug('{0} - TOPIC: {1} '.format(self.dateTimeStamp(), msg.topic))
        #logger.debug('{0} - DATA: {1} '.format(self.dateTimeStamp(), json.loads(msg.payload)))
        logger.debug('{0} - DEVICE -> SERVER: {1}'.format(self.dateTimeStamp(), json.loads(msg.payload)))
        self.parseData(msg.topic, msg.payload)

    # Função que formata e retorna data e hora
    def dateTimeStamp(self):
        ts = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        return ts

    def parseData(self, topic, payload):
        mqtt_resp = {}

        if (topic == self.TOPICO_STATUS):
            payload_dic = json.loads(payload)

            res = Device.objects.create(
                device_id = payload_dic['device_id'],
                door_status = payload_dic['door_status'],
                uid = payload_dic['uid'], 
                date_time = timezone.now()
            )
            
            if (payload_dic['uid'] > 0):
                try:
                    usr = User.objects.get(uid=payload_dic['uid'])
                    mqtt_resp["device_id"] = payload_dic['device_id']
                
                    if usr.enabled == True:
                        mqtt_resp["card_status"] = 1
                    else:
                        mqtt_resp["card_status"] = 0
                    
                    if usr.autorized == True:
                        mqtt_resp["autorization"] = 1
                    else:
                        mqtt_resp["autorization"] = 0
                                
                    self.client.publish(self.TOPICO_SERVER, json.dumps(mqtt_resp), 1)
                    
                    logger.debug('{0} - SERVER -> DEVICE: {1}'.format(self.dateTimeStamp(), json.dumps(mqtt_resp)))
                
                except Exception as ex:
                    logger.debug('{0} - SERVER -> DEVICE: {1}'.format(self.dateTimeStamp(), json.dumps(mqtt_resp)))
          

