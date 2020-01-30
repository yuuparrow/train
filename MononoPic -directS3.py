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

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Greengrass Coreが入っているデバイスの情報を取得
my_platform = platform.platform()

# このLambda関数がデプロイされ、ラズパイが起動すると、5秒おきにずっと動き続ける。
# "hello/world"というtopicをAWS IoT上でサブスクライブすると、メッセージが返ってくる
    #写真を撮る
def capture_image():
    camera = picamera.PiCamera()
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

        s3 = boto3.resource('s3')
        s3.Object("バケット名","S3上での画像名").upload_file('ローカル画像のパス')
        return imageData

    finally:
        camera.close()
        raise RuntimeError("There is problem to use your camera.")

    Timer(5, capture_image).start()



# 5秒ごとに非同期にこの関数を実行する
# while True:
#     capture_image()
#     time.sleep(5)


