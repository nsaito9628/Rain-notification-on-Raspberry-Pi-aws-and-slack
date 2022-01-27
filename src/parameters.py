import os
import paho.mqtt.client as mqtt

client = mqtt.Client(protocol=mqtt.MQTTv311)
HOST = os.environ['HOST_ENDPOINT']  # AWS IoT Endpoint
PORT = 8883  # mqtts port
CACERT = os.environ['CACERT']  # root ca
CLIENTCERT = os.environ['CLIENTCERT']  # certificate
CLIENTKEY = os.environ['CLIENTKEY']  # private key

DEVICE = os.environ['DEVICE']#'rain_notifier'
TOPIC_LAMBDA = os.environ['TOPIC_LAMBDA']#'lambda'
TOPIC_DASHBOARD = os.environ['TOPIC_DASHBOARD']#'dashboard'

RAIN_PIN = 21

SENSOR_NO = int(os.environ['SENSOR_NO'])