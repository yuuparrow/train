import StringIO
from io import BytesIO
import logging
import picamera
import time
import platform
import json
import base64
import sys
from threading import Timer
import greengrasssdk
from test.test_functools import capture
import AWSIoTPythonSDK.MQTTLib import AWSItOMQTTClient
from idlelib.CodeContext import FONTUPDATEINTERVAL


# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#MQTTクライアントの作成
myMQTTClient = AWSIoTMQTTClient("ラズパイの名前")
myMQTTClient.configureEndpoint("エンドポイントのURL", 8080)
myMQTTClient.configureCredentials("各種証明書ローカルパス")
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

# sdk clientを作成
client = greengrasssdk.client("iot-data")

# Greengrass Coreが入っているデバイスの情報を取得
my_platform = platform.platform()

# このLambda関数がデプロイされ、ラズパイが起動すると、5秒おきにずっと動き続ける。
# "hello/world"というtopicをAWS IoT上でサブスクライブすると、メッセージが返ってくる
class Camera(object):
    #写真を撮る
    def capture_image(self):
        camera = picamera/PiCamera()
        imageData = StringIO.StringIO()

        #解像度の設定
        try:
            camera.resolution = (1024, 1024)
            camera.brightness = 70
            camera.start_preview()
            time.sleep(2)
            camera.capture(imageData, format="jpeg", resize = (1024, 1024))
            camera.stop_preview()

            imageData.seek(0)
            return imageData
        finally:
           camera.close()
       raise RuntimeError("There is problem to use your camera.")

def send_mqtt_picture(selfimgdata):
       iot_client.publish(topic=topic_pic, payload=json.dumps({"data": imgdata}))

def take_pic():
    my_camera = Camera()
    imagebinary = my_camera.capture_image()
    #エンコード
    image64 = base64.test_b64encode(imagebinary.getvalue())
    image_str = image64.decode("utf-8")
    send_mqtt_picture(image_str)



       # 5秒ごとに非同期にこの関数を実行する
while True:
    take_pic()
    time.sleep(5)


