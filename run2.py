import socket
import time

from http.server import BaseHTTPRequestHandler
from io import BytesIO
import cgi
import json
import xmltodict
import cv2
from datetime import datetime
import requests
import requests
from pprint import pprint
import string
from datetime import datetime
import json
import argparse
import time
from pathlib import Path
import base64
import cv2
import numpy as np
import random


def ParseLineCrossing(json_data):
    print(json_data["EventNotificationAlert"]["ipAddress"])
    print(json_data["EventNotificationAlert"]["portNo"])
    print(json_data["EventNotificationAlert"]["protocol"])
    print(json_data["EventNotificationAlert"]["macAddress"])
    print(json_data["EventNotificationAlert"]["channelID"])
    
    print(json_data["EventNotificationAlert"]["dateTime"])
    print(json_data["EventNotificationAlert"]["activePostCount"])
    print(json_data["EventNotificationAlert"]["eventType"])
    print(json_data["EventNotificationAlert"]["eventState"])
    print(json_data["EventNotificationAlert"]["eventDescription"])
    
    print(json_data["EventNotificationAlert"]["channelName"])
    print(json_data["EventNotificationAlert"]["detectionPictureTransType"])
    print(json_data["EventNotificationAlert"]["detectionPicturesNumber"])
    print(json_data["EventNotificationAlert"]["isDataRetransmission"])
    
    print(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["regionID"])
    print(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["sensitivityLevel"])
    print(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["RegionCoordinatesList"])
    print(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["detectionTarget"])
    print(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["TargetRect"])




def sendLPRQuery(xd,Action,LocationType,Location,Camera):
    if Action == "OUT":
        sx = {
            "Action" : Action,
            "LocationType": LocationType,
            "Camera": Camera,
            "Location": Location,
            #"EntryTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "ExitTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            #"LPRResult": json.dumps(js),
        }
        url = 'https://52.90.249.216/api/events/'
        data = sx
        r = requests.post(url = url, json = data,verify=False)
        print(r)
        result = json.loads(r.text)
        print(result)
        return
    elif Action == "IN":
        PlateNo = ""
        Region = ""
        RegionScore = ""
        PlateCrop = ""
        PlateScore = ""

        VehicleType = ""
        VehicleCrop = ""
        VehicleScore = ""
        Timestamp = ""
        js = ""
        RegionS = "Unknown"
        with open(xd, "rb") as fid:
            data = fid.read()
        try:
            regions = ['ae', 'sa',] # Change to your country
            with open(xd, 'rb') as fp:
                response = requests.post(
                    'https://api.platerecognizer.com/v1/plate-reader/',
                    data=dict(regions=regions),  # Optional
                    files=dict(upload=fp),
                    headers={'Authorization': 'Token f8956676cd215ab0b3e118c4d3da077f30c012f0'})
            js = response.json()
            print(js)
            try:
                PlateNo = js['results'][0]['plate'].upper()
            except:
                pass
            try:
                RegionS = "Unknown"
                Region = js['results'][0]['region']['code']
                if Region == "ae-az":
                    RegionS = "Abu Dhabi"
                elif Region == "ae-aj":
                    RegionS = "Ajman"
                elif Region == "ae-du":
                    RegionS = "Dubai"
                elif Region == "ae-fu":
                    RegionS = "Fujairah"
                elif Region == "ae-rk":
                    RegionS = "Ras Al Khaimah"
                elif Region == "ae-sh":
                    RegionS = "Sharjah"
                elif Region == "ae-uq":
                    RegionS = "Umm Al Quwain"
                else:
                    RegionS = "Unknown"
            except:
                pass
            try:
                RegionScore = js['results'][0]['region']['score']
            except:
                pass
            try:
                PlateCrop = js['results'][0]['box']
            except:
                pass
            try:
                PlateScore = js['results'][0]['score']
            except:
                pass
            try:
                VehicleType = js['results'][0]['vehicle']['type']
            except:
                pass
            try:
                VehicleCrop = js['results'][0]['vehicle']['box']
            except:
                pass
            try:
                VehicleScore = js['results'][0]['vehicle']['score']
            except:
                pass
            try:
                Timestamp = js['timestamp']
            except:
                pass 
        except:
            pass
        if(PlateNo != ""):
            try:
                sx = {
                    "Action" : "IN",
                    "LocationType": LocationType,
                    "Camera": Camera,
                    "Location": Location,
                    "PlatesNo": PlateNo,
                    "PlatesRegion": RegionS,
                    "PlatesScore": PlateScore,
                    "VehicleType": VehicleType,
                    "PlateImage":  base64.b64encode(data).decode("utf-8"),
                    "VehicleImage": base64.b64encode(data).decode("utf-8"),
                    "EntryTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    #"ExitTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "LPRResult": json.dumps(js),
                }
                url = 'https://52.90.249.216/api/events/'
                data = sx
                r = requests.post(url = url, json = data,verify=False)
                print(r)
                result = json.loads(r.text)
                print(result)
            except Exception as e:
                print("Problem Occured while Sending data to AWS" + str(e))
            return
    else:
        print("This is not IN/OUT")
        return 
    



class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

def cgiFieldStorageToDict(fieldStorage):
   params = {}
   for key in fieldStorage.keys(  ):
      params[key] = fieldStorage[key].value
   return params
   


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
serv.listen(5)
while True:
    try:
        conn, addr = serv.accept()
        Requestx = b''
        while True:
            Requests = conn.recv(4096)
            if not Requests: break
            Requestx += Requests#.decode("utf-8")
        #print(Requestx)
        request = HTTPRequest(Requestx)
        ctype, pdict = cgi.parse_header(request.headers['Content-Type'])
        #pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        #pdict['CONTENT-LENGTH'] = int(request.headers['Content-Length'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage( fp=request.rfile, headers=request.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':request.headers['Content-Type'], })
            #print(cgiFieldStorageToDict(form))
            
            EventCheck = ["linedetection","fielddetection"]
            ImageCheck = ["lineCrossImage","intrusionImage"]
            EventType = ""
            ImageType = ""
            SelectedOption = -1
            
            for i in range(len(EventCheck)):
                try:
                    TempVar = form[EventCheck[i]]
                    print(f"{EventCheck[i]} parameter has been found")
                    EventType = EventCheck[i]
                    ImageType = ImageCheck[i]
                    SelectedOption = i
                    print("proceeding for further")
                    break
                except KeyError:
                    print(f"{EventCheck[i]} Could not be Found :(")
                    
             
                    
            FormDict = cgiFieldStorageToDict(form)
            TempData = FormDict[EventCheck[SelectedOption]]
            data_dict = xmltodict.parse(TempData)
            json_data = json.loads(json.dumps(data_dict))
            #ParseLineCrossing(json_data)
            
            ImageName = ""
            if EventType != "":
                try:
                    if isinstance(form[ImageType], list):
                        for record in form[ImageType]:
                            ImageName = "./Events/"+ImageType.upper()+"_%s.jpeg"%record.filename
                            open(ImageName, "wb").write(record.file.read())
                    else:
                        ImageName = "./Events/"+ImageType.upper()+"_%s.jpeg"%form[ImageType].filename
                        open(ImageName, "wb").write(form[ImageType].file.read())
                except IOError:
                        print (False, "Can't create file to write, do you have permission to write?")

            if(ImageName != ""):
                #print("I am Here")
                RecvImage = cv2.imread(ImageName)
                (Height,Width,Channels) = RecvImage.shape
                X=int(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["TargetRect"]['X'])
                Y=int(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["TargetRect"]['Y'])
                width=int(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["TargetRect"]['width'])
                height=int(json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["TargetRect"]['height'])
                

                #print(Height,Width,Channels,X,Y,width,height)
                X1c = int(Width * (X/1000))
                Y1c = int(Height * (Y/1000))
                X2c = int((Width * (X/1000)) + (Width *(width/1000)))
                Y2c = int((Height * (Y/1000)) + (Height *(height/1000)))
                #print(X1c,X2c,Y1c,Y2c)
                CropImage = RecvImage[Y1c:Y2c,X1c:X2c]
                #ImageCoord = json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["TargetRect"]
                #CroppedImage = RecvImage[int(ImageCoord['Y']):int(ImageCoord['Y'])+int(ImageCoord['height'])]

                EventTime = json_data["EventNotificationAlert"]["dateTime"]
                EventDesc = json_data["EventNotificationAlert"]["eventDescription"]
                EventCamera = json_data["EventNotificationAlert"]["channelName"]
                EventRegion = json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["regionID"]
                EventTarget = json_data["EventNotificationAlert"]["DetectionRegionList"]["DetectionRegionEntry"]["detectionTarget"]
                
                print(EventTime + " " + EventDesc + " : " + EventTarget + " at " + EventCamera + " " + EventRegion)
                cv2.imwrite(ImageName.replace("./Events","./Vehicles"), CropImage)
                
                print("|"+EventCamera+"|")
                if(EventCamera == "Lube Bay"):
                    print("Lube Bay Operation")
                    if(EventRegion == "1"): #Lube Bay 1 Entry
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 1 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"IN","Lube","Lube 928-1","ADNOC 928 Lube")
                    elif(EventRegion == "3"):  #Lube Bay 2 Entry
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 2 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"IN","Lube","Lube 928-2","ADNOC 928 Lube")
                    elif(EventRegion == "2"):  #Lube Bay 1 Exit
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 3 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"OUT","Lube","Lube 928-1","ADNOC 928 Lube")
                    elif(EventRegion == "4"):  #Lube Bay 2 Exit
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 4 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"OUT","Lube","Lube 928-2","ADNOC 928 Lube")
                elif(EventCamera == "Vacuum Bay"):
                    if(EventRegion == "1"): #Vacuum Bay 1 Entry
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 5 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"IN","Vacuum","Vacuum 928-1","ADNOC 928 Vacuum")
                    elif(EventRegion == "3"):  #Vacuum Bay 2 Entry
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 6 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"IN","Vacuum","Vacuum 928-2","ADNOC 928 Vacuum")
                    elif(EventRegion == "2"):  #Vacuum Bay 1 Exit
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 7 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"OUT","Vacuum","Vacuum 928-1","ADNOC 928 Vacuum")
                    elif(EventRegion == "4"):  #Vacuum Bay 2 Exit
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 8 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"OUT","Vacuum","Vacuum 928-2","ADNOC 928 Vacuum")
                elif(EventCamera == "Manual Washing Bay"):
                    if(EventRegion == "1"): #Vacuum Bay 1 Entry
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 9 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"IN","Washing","Washing 928-Man","ADNOC 928 Washing")
                    elif(EventRegion == "2"):  #Vacuum Bay 2 Entry
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 10 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"IN","Unknown","Washing 928-Queue","ADNOC 928 Queue")
                    elif(EventRegion == "X"):  #Vacuum Bay 1 Exit
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 11 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"OUT","Vacuum","Vacuum 928-1","ADNOC 928 Vacuum")
                    elif(EventRegion == "X"):  #Vacuum Bay 2 Exit
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 12 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"OUT","Vacuum","Vacuum 928-2","ADNOC 928 Vacuum")
                elif(EventCamera == "Auto Washing Bay"):
                    if(EventRegion == "1"): #Vacuum Bay 1 Entry
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 9 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"IN","Washing","Washing 928-Auto","ADNOC 928 Washing")
                    elif(EventRegion == "2"):  #Vacuum Bay 2 Entry
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 10 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"IN","Unknown","Washing 928-Queue","ADNOC 928 Queue")
                    elif(EventRegion == "X"):  #Vacuum Bay 1 Exit
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 11 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"OUT","Vacuum","Vacuum 928-1","ADNOC 928 Vacuum")
                    elif(EventRegion == "X"):  #Vacuum Bay 2 Exit
                        print(EventTime + " " + EventDesc + " : " + EventTarget + " at 12 " + EventCamera + " " + EventRegion)
                        sendLPRQuery(ImageName.replace("./Events","./Vehicles"),"OUT","Vacuum","Vacuum 928-2","ADNOC 928 Vacuum")
                else:
                    print("I am Here")
                '''
                cv2.imshow('image', CropImage)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                '''

        conn.close()
        print('client disconnected')
    except Exception as e: print(e)
    #exit()

'''
FieldStorage('linedetection', None, '<?xml version="1.0" encoding="UTF-8"?>\r\n<EventNotificationAlert version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">\r\n<ipAddress>192.168.70.66</ipAddress>\r\n<portNo>8080</portNo>\r\n<protocol>HTTP</protocol>\r\n<macAddress>24:0f:9b:9c:e4:6b</macAddress>\r\n<channelID>1</channelID>\r\n<dateTime>2022-10-15T23:07:58+08:00</dateTime>\r\n<activePostCount>1</activePostCount>\r\n<eventType>linedetection</eventType>\r\n<eventState>active</eventState>\r\n<eventDescription>linedetection alarm</eventDescription>\r\n<DetectionRegionList>\r\n<DetectionRegionEntry>\r\n<regionID>3</regionID>\r\n<sensitivityLevel>50</sensitivityLevel>\r\n<RegionCoordinatesList>\r\n<RegionCoordinates>\r\n<positionX>539</positionX>\r\n<positionY>444</positionY>\r\n</RegionCoordinates>\r\n<RegionCoordinates>\r\n<positionX>848</positionX>\r\n<positionY>431</positionY>\r\n</RegionCoordinates>\r\n</RegionCoordinatesList>\r\n<detectionTarget>vehicle</detectionTarget>\r\n<TargetRect>\r\n<X>615</X>\r\n<Y>297</Y>\r\n<width>187</width>\r\n<height>281</height>\r\n</TargetRect>\r\n</DetectionRegionEntry>\r\n</DetectionRegionList>\r\n<channelName>Vacuum Bay</channelName>\r\n<detectionPictureTransType>binary</detectionPictureTransType>\r\n<detectionPicturesNumber>1</detectionPicturesNumber>\r\n<isDataRetransmission>false</isDataRetransmission>\r\n</EventNotificationAlert>\r\n') parameter has been found
Procedding for further
192.168.70.66
8080
HTTP
24:0f:9b:9c:e4:6b
1
2022-10-15T23:07:58+08:00
1
linedetection
active
linedetection alarm
Vacuum Bay
binary
1
false
3
50
{'RegionCoordinates': [{'positionX': '539', 'positionY': '444'}, {'positionX': '848', 'positionY': '431'}]}
vehicle
{'X': '615', 'Y': '297', 'width': '187', 'height': '281'}




(1080, 1920, 3) 705 395 108 541
intrusionImage

fielddetection

'fielddetection': '<?xml version="1.0" encoding="UTF-8"?>\r\n<EventNotificationAlert version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">\r\n<ipAddress>192.168.10.64</ipAddress>\r\n<portNo>8080</portNo>\r\n<protocol>HTTP</protocol>\r\n<macAddress>ac:b9:2f:63:d7:5c</macAddress>\r\n<channelID>1</channelID>\r\n<dateTime>2022-10-15T03:05:57+04:00</dateTime>\r\n<activePostCount>1</activePostCount>\r\n<eventType>fielddetection</eventType>\r\n<eventState>active</eventState>\r\n<eventDescription>fielddetection alarm</eventDescription>\r\n<DetectionRegionList>\r\n<DetectionRegionEntry>\r\n<regionID>1</regionID>\r\n<sensitivityLevel>50</sensitivityLevel>\r\n<RegionCoordinatesList>\r\n<RegionCoordinates>\r\n<positionX>685</positionX>\r\n<positionY>243</positionY>\r\n</RegionCoordinates>\r\n<RegionCoordinates>\r\n<positionX>694</positionX>\r\n<positionY>934</positionY>\r\n</RegionCoordinates>\r\n<RegionCoordinates>\r\n<positionX>983</positionX>\r\n<positionY>942</positionY>\r\n</RegionCoordinates>\r\n<RegionCoordinates>\r\n<positionX>981</positionX>\r\n<positionY>249</positionY>\r\n</RegionCoordinates>\r\n</RegionCoordinatesList>\r\n<detectionTarget>human</detectionTarget>\r\n<TargetRect>\r\n<X>744</X>\r\n<Y>411</Y>\r\n<width>124</width>\r\n<height>581</height>\r\n</TargetRect>\r\n</DetectionRegionEntry>\r\n</DetectionRegionList>\r\n<channelName>Camera 01</channelName>\r\n<detectionPictureTransType>binary</detectionPictureTransType>\r\n<detectionPicturesNumber>1</detectionPicturesNumber>\r\n<isDataRetransmission>false</isDataRetransmission>\r\n</EventNotificationAlert>\r\n'

linedetection

'linedetection': '<?xml version="1.0" encoding="UTF-8"?>\r\n<EventNotificationAlert version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">\r\n<ipAddress>192.168.10.64</ipAddress>\r\n<portNo>8080</portNo>\r\n<protocol>HTTP</protocol>\r\n<macAddress>ac:b9:2f:63:d7:5c</macAddress>\r\n<channelID>1</channelID>\r\n<dateTime>2022-10-15T03:02:17+04:00</dateTime>\r\n<activePostCount>1</activePostCount>\r\n<eventType>linedetection</eventType>\r\n<eventState>active</eventState>\r\n<eventDescription>linedetection alarm</eventDescription>\r\n<DetectionRegionList>\r\n<DetectionRegionEntry>\r\n<regionID>1</regionID>\r\n<sensitivityLevel>50</sensitivityLevel>\r\n<RegionCoordinatesList>\r\n<RegionCoordinates>\r\n<positionX>275</positionX>\r\n<positionY>878</positionY>\r\n</RegionCoordinates>\r\n<RegionCoordinates>\r\n<positionX>741</positionX>\r\n<positionY>666</positionY>\r\n</RegionCoordinates>\r\n</RegionCoordinatesList>\r\n<detectionTarget>human</detectionTarget>\r\n<TargetRect>\r\n<X>700</X>\r\n<Y>340</Y>\r\n<width>162</width>\r\n<height>598</height>\r\n</TargetRect>\r\n</DetectionRegionEntry>\r\n</DetectionRegionList>\r\n<channelName>Camera 01</channelName>\r\n<detectionPictureTransType>binary</detectionPictureTransType>\r\n<detectionPicturesNumber>1</detectionPicturesNumber>\r\n<isDataRetransmission>false</isDataRetransmission>\r\n</EventNotificationAlert>\r\n'
'''
