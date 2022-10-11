from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from logs.models import Event
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serialisers import EventSerializer
from logs.models import Event as Events
import json,base64

from django.shortcuts import get_object_or_404
from django.http import Http404

import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.decorators import method_decorator
import requests
import random
import string

from rest_framework.permissions import AllowAny

# Create your views here.


def decodeDesignImage(data):
    try:
        data = base64.b64decode(data.encode('UTF-8'))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        return img
    except:
        return None

#@method_decorator(csrf_exempt, name='dispatch')
class Event(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        events = Events.objects.all()
        print(events.values())
        eventsSerial = EventSerializer(events, many=True)
        return Response(json.loads(json.dumps(eventsSerial.data)),status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        LocationType = self.request.data.get('LocationType')
        Camera = self.request.data.get("Camera")
        Location = self.request.data.get("Location")
        PlatesNo = self.request.data.get("PlatesNo")
        PlatesRegion = self.request.data.get("PlatesRegion")
        PlatesScore = self.request.data.get("PlatesScore")
        VehicleType = self.request.data.get("VehicleType")
        EntryTime = self.request.data.get("EntryTime")
        ExitTime = self.request.data.get("ExitTime")
        VehicleImage = self.request.data.get("VehicleImage")
        PlateImage = self.request.data.get("PlateImage")
        LPRResult = self.request.data.get("LPRResult")


        letters = string.ascii_lowercase
        post = Events()
        try:
            img1 = decodeDesignImage(VehicleImage)
            VehicleImage_io = io.BytesIO()
            img1.save(VehicleImage_io, format='JPEG')
            post.VehicleImage = InMemoryUploadedFile(VehicleImage_io, field_name=None, name="vehicle_"+''.join(random.choice(letters) for i in range(10))+".jpg", content_type='image/jpeg', size=VehicleImage_io.tell, charset=None)
        
        except:
            pass
        
        try:
            img2 = decodeDesignImage(PlateImage)
            PlateImage_io = io.BytesIO()
            img2.save(PlateImage_io, format='JPEG')
            post.PlateImage = InMemoryUploadedFile(PlateImage_io, field_name=None, name="plate_"+''.join(random.choice(letters) for i in range(10))+".jpg", content_type='image/jpeg', size=PlateImage_io.tell, charset=None)
        except:
            pass
        post.LocationType = LocationType
        post.Camera = Camera
        post.Location = Location
        post.PlatesNo = PlatesNo
        post.PlatesRegion = PlatesRegion
        post.PlatesScore = PlatesScore

        post.VehicleType = VehicleType
        post.EntryTime = EntryTime
        post.ExitTime = ExitTime
        post.LPRResult = LPRResult
        post.save()

        '''
            {
                "id": 1,
                "LocationType": "Unknown",
                "Camera": null,
                "Location": null,
                "PlatesNo": null,
                "PlatesRegion": null,
                "PlatesScore": null,
                "VehicleType": null,
                "EntryTime": null,
                "ExitTime": null,
                "VehicleImage": null,
                "PlateImage": null,
                "LPRResult": null,
                "created": "2022-10-11T19:36:14.664239Z",
                "modified": "2022-10-11T19:36:14.664239Z"
            }
        '''

        # try:
        #     device = Device.objects.get(UniqueID = deviceid, Enable=True) 
        # except Device.DoesNotExist:
        #     return Response({"success": 0 ,"detail": "device not enabled"},status=status.HTTP_401_UNAUTHORIZED)
        # except Device.MultipleObjectsReturned:
        #     return Response({"success": 0 ,"detail": "device not enabled"},status=status.HTTP_401_UNAUTHORIZED)

        # person = None
        # try:
        #     person = Personnel.objects.get(UniqueID = personid) 
        # except Personnel.DoesNotExist:
        #     person = None
        # except Personnel.MultipleObjectsReturned:
        #     person = None
        
        # rule = None
        # try:
        #     rule = Rule.objects.get(Name = ruleid) 
        # except Rule.DoesNotExist:
        #     rule = None
        # except Rule.MultipleObjectsReturned:
        #     rule = None

        # img = decodeDesignImage(image)
        # img_io = io.BytesIO()
        # img.save(img_io, format='JPEG')

        # post = Event()
        # post.Person = person
        # post.Rule = rule
        # post.Device = device
        # post.Health = health
        # post.Lattitude = lat
        # post.Longitude = lng
        # post.Photo = InMemoryUploadedFile(img_io, field_name=None, name='token'+".jpg", content_type='image/jpeg', size=img_io.tell, charset=None)
        # post.processed = True
        # post.save()
        # print(post.Photo.url)
        # try:
        #     response = requests.get('http://127.0.0.1:8000' + post.Photo.url)
        #     image = ("data:" + response.headers['Content-Type'] + ";" +"base64," + base64.b64encode(response.content).decode("utf-8"))
        #     url = 'http://127.0.0.1:8080/api/v3/scan/'
        #     data = {"image": image}
        #     r = requests.post(url = url, json = data)
        #     result = json.loads(r.text)
        #     sscan = SafetyScan()
        #     sscan.EventID = post
        #     sscan.Hat = result['Hat']
        #     sscan.Gloves = result['Gloves']
        #     sscan.Vest = result['Vest']
        #     sscan.Boot = result['Boot']
        #     sscan.Glasses = result['Glasses']
        #     sscan.Mask = result['Mask']
        #     img = decodeDesignImage(result['result'])
        #     img_io = io.BytesIO()
        #     img.save(img_io, format='JPEG')
        #     sscan.Photo = InMemoryUploadedFile(img_io, field_name=None, name='token'+".jpg", content_type='image/jpeg', size=img_io.tell, charset=None)
        #     sscan.save()
        #     post.safetyprocessed = True
        #     post.save()
        # except:
        #     print('Problem Occured while processing safety data')
        
        # try:
        #     url = 'http://127.0.0.1:5000/api/v3/qr/'
        #     data = {"qr": health}
        #     r = requests.post(url = url, json = data)
        #     result = json.loads(r.text)
        #     print(result)
        #     hscan = HealthScan()
        #     hscan.EventID = post
        #     hscan.Category = 0;
        #     hscan.Name = result['name'];
        #     hscan.IDn = result['id'];
        #     hscan.Mobile = result['mobile'];
        #     hscan.CodeType = result['code_type'];
        #     hscan.Category = 0;
        #     hscan.Typex = result['type'];

        #     hscan.GenTime = result['gen_time'];
        #     hscan.ExpTime = result['exp_time'];

        #     hscan.DPIDate = result['last_dpi_date'];
        #     hscan.PCRDate = result['last_pcr_date'];

        #     hscan.DPIResult = result['last_dpi'];
        #     hscan.PCRResult = result['last_pcr'];

        #     hscan.Excemption = result['excemption'];
        #     hscan.Junior = result['junior'];
        #     hscan.Senior = result['senior'];
        #     hscan.Vaccinated = result['vaccinated'];
        #     hscan.Visitor = result['visitor'];
        #     hscan.Volunteer = result['volunteer'];
        #     hscan.save()
        #     post.healthprocessed = True
        #     post.save()
        # except:
        #     print('Problem Occured while processing health data')
        # events = Events.objects.get(pk = post.pk)
        # eventsSerial = EventSerializer(events)
        # return Response(json.loads(json.dumps(eventsSerial.data)),status=status.HTTP_200_OK)
        return Response({"success": 1 ,"detail": "event added"})