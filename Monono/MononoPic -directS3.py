
import greengrasssdk
import platform
import time
import json
import picamera
import boto3
import os
from time import sleep
import datetime
from test.test_zipimport import NOW

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')


my_platform = platform.platform()

bucket = os.environ['S3_BUCKET_NAME']
thing_name = os.environ['THING_NAME']




def make_picture():

    try:

        now = datetime.datetime.now()
        camera = picamera.PiCamera()
        camera.resolution = (1024, 1024)
        camera.brightness = 60
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        camera.capture('/output/{0:%Y%m%d%H%M%S}.png'.format(now))
        s3 = boto3.resource('s3')

        # s3.meta.client.upload_file('/output/lambda-image.png',
        # 'roeland-greengrass', 'image.png')
        s3.meta.client.upload_file('/output/{0:%Y%m%d%H%M%S}.png'.format(now), bucket, 'image.png')
#         s3.Object("バケット名","S3上での画像名").upload_file('ローカル画像のパス')

    except Exception as e:
        client.publish(topic='picture/status', payload='Something went wrong!')
        print(e)

    finally:
        camera.close()

    Timer(5, make_picture).start()

#上記の関数を実行
make_picture()
