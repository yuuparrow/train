import os
import boto3
from datetime import datetime
from io import BytesIO
from base64 import b64decode

def upload_img(img_binary):
   s3 = boto3.resource('s3')
   bucket = os.environ["BUCKET"]
   dir = "images"
   filename = 'img_{}.jpg'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))
   obj = s3.Object(bucket, os.path.join(dir,filename))
   print("put",filename,"to",bucket)
   obj.put(Body=BytesIO(img_binary),ContentType="image/jpg")
   return


def lambda_handler(event, context):
  print("test",event)
  img = event["data"]
  img_binary = b64decode(img)
  upload_img(img_binary)
  return 0