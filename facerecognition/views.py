# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import requests, base64, json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from django.templatetags.static import static
import os
from django.conf import settings
import os.path
import requests, base64, json,time , picamera, RPi.GPIO as GPIO, sys
from requests_toolbelt.multipart.encoder import MultipartEncoder
from relay import Relay
from Lcd import Lcd
import pyttsx
camera = picamera.PiCamera()
engine = pyttsx.init()




def index(request):
    template = loader.get_template('facerecognition/index.html')
    return HttpResponse(template.render({}, request))

def greet(request):
    BASE = os.path.dirname(os.path.abspath(__file__))
    image_url=BASE+"/static/images/ot.jpg"
    
    camera.start_preview()
    time.sleep(2)
    os.chdir(BASE+"/static/images")
    camera.capture('ot.jpg')
    camera.stop_preview()
    relay = Relay()
    relay.switch(0, 0)
    relay.switch(1, 0)
    relay.switch(2, 0)
    relay.switch(3, 0)
    lcd = Lcd()
    lcd.clear()

    
    multipart_data = MultipartEncoder(
      fields={
            'image': ('ot.jpg', open(image_url, 'rb'), 'image/*'),
            'gallery_name': 'MyGallery'
           }
    )
    headers = {'content-type': multipart_data.content_type, 'app_id': '02cb4d84', 'app_key': '2dd083ecb88d76c99ffe59b16570239c'}
    url = 'http://api.kairos.com/recognize'
    response = requests.post(url, data=multipart_data,headers=headers)
    data = json.loads(response.content)
    error_msg = ''
    name = ''
    if 'Errors' in data:
	lcd.display_string(data["Errors"][0]["Message"],1)
	error_msg = data["Errors"][0]["Message"]
    elif data["images"][0]["transaction"]["status"] == "failure":
        lcd.display_string(data["images"][0]["transaction"]["message"],1)
        error_msg =  "No Match found please try again"
    elif str(data["images"][0]["transaction"]["subject_id"]) == 'ethiraj':
	lcd.display_string("ethiraj",1)
	relay.switch(0,1)
	name =  "Hey ethiraj Welcome"
    elif str(data["images"][0]["transaction"]["subject_id"]) == 'vimal':
	lcd.display_string("vimal",1)
	relay.switch(1,1)
	name = "Hey vimal Welcome"
    elif str(data["images"][0]["transaction"]["subject_id"]) == 'sowndarya':
	lcd.display_string("sowndarya",1)
	relay.switch(2,1)
	name = "Hey sowndarya Welcome"
    if name:
        engine.say(name)
        engine.runAndWait()
    template = loader.get_template('facerecognition/greet.html')
    return HttpResponse(template.render({'name': name, 'error_msg': error_msg, 'image_dir': image_url}, request))



    
    
