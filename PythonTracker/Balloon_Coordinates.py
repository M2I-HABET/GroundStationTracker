"""
-------------------------------------------------------------------------------
MIT License
Copyright (c) 2021 Ronnel Walton
Modified: Mathew Clutter
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-------------------------------------------------------------------------------
"""
from calendar import timegm

import requests
import time
import sys
import gps
import pandas as pd
import folium

#session = gps.gps()
#session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
#report = session.next()
home_lat = 42.0276
home_lon = -93.3460
map = folium.Map(location = [home_lat,home_lon], zoom_start=10)



class Balloon_Coordinates:
    BOREALIS_EPOCH = 1357023600
    
        
    
    #session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    

    def __init__(self, imei):

        self.imei = imei

        try:
            # Grab and Define IMEI's Latest Flight
            req = requests.get("https://borealis.rci.montana.edu/meta/flights?imei={}".format(self.imei))
        except requests.exceptions.RequestException:  # does not catch if there is no internet
            print("No internet connection detected")
            sys.exit(-1)

        self.latest_flight = req.json()[-1]

        # Define UID
        flightTime = timegm(time.strptime(self.latest_flight, "%Y-%m-%d")) - Balloon_Coordinates.BOREALIS_EPOCH
        self.uid = (int(flightTime) << 24) | int(self.imei[8:])

        return


    @staticmethod
    def list_IMEI():
    # grab the list of all of the imei's on the borealis server

        # Request IMEI List
        try:
            req = requests.get('https://borealis.rci.montana.edu/meta/imeis')
        except requests.exceptions.RequestException:
            print("couldn't connect to internet")
            print("Please connect to internet and relaunch")
            sys.exit(-1)

        data = req.json()
        IMEIs = []

        for imei in data:
                IMEIs.append(imei)
        return IMEIs
    
    
        
        
        
    def get_coor_alt(self):
        
        #HAR gps tracking code
        data = pd.read_csv('HAR_GPS.csv', header = None)
        try:
            last_row = data.iloc[-1]
            lat = int(last_row[1]) / 10000000
            long = int(last_row[2]) / 10000000
            alt = int(last_row[3]) / 1000
            pressure = int(last_row[4]) / 100
            temperature = int(last_row[5]) / 100
            humidiity = int(last_row[6]) / 1000
            print(f"lat = {lat}, long = {long}, alt = {alt} meters, pressure = {pressure} Pa, temperature = {temperature} C, humididty = {humidiity} %H")
            self.coor_alt = [lat,long,alt]
            #make a map
            last_cord = data.iloc[-1]
            lat = int(last_cord[1]) / 10000000
            long = int(last_cord[2]) / 10000000
            alt = int(last_cord[3]) / 1000
            balloon_cord = [lat,long,alt]
            folium.Marker([lat,long],popup= (lat,long,alt)).add_to(map)
            map.save('map.html')
            
            return self.coor_alt
            
        except ValueError:
            self.coor_alt = None
            return self.coor_alt
        # try:
        #     folium.Marker([lat,long], popup= (lat,long,alt)).add_to(map)
        #     map.save('map.html')
        # except ValueError:
        #     return None

        
        '''
        #test gps tracking code
        numbers = []

        with open('Fakegpsdata.txt', 'r') as file:
            for line in file:
                # Remove any leading/trailing whitespace and split the line into individual numbers
                line = line.strip()
                nums = line.split(',')

                # Convert each number from string to float and add it to the array
                for num in nums:
                    numbers.append((num))
        num1 = float(numbers[0])
        num2 = float(numbers[1])
        num3 = float(numbers[2])
        self.coor_alt =[num1,num2,num3]
        print('coor_alt: ', self.coor_alt)
        print(numbers[0], numbers[1], numbers[2])
        return self.coor_alt
        '''
        '''

        #live gps tracking code
        
        report = session.next()
        time.sleep(1)

        
        
        if report['class'] == 'TPV' and hasattr(report, 'lat') and hasattr (report, 'lon'):
            values = [report.lat, report.lon, report.alt, report.speed, report.climb]
            print(values)
            self.coor_alt = [values[0],values[1],values[2]]
            return self.coor_alt
        else:
            self.coor_alt = [0,0,0]

        '''
        

        
        
        
        

        
            
            
        #print('latitude:',report.lat, ' longitude: ',report.lon, ' altitude: ',report.alt, ' speed: ',report.speed, ' climb: ',report.climb)
            
        
        # returns a list containing the lat, long, and alt of the latest ping from the selected IMEI
        
        # try:
        #     req = requests.get("https://borealis.rci.montana.edu/flight?uid={}".format(self.uid))
        #     print("https://borealis.rci.montana.edu/flight?uid={}".format(self.uid))
            
        #     '''
        #     if report['class'] == 'TPV' and hasattr(report, 'lat') and hasattr (report, 'lon'):
        #         values = [report.lat, report.lon, report.alt]
        #         print(values)
            
        #     else:
        #         values = [0,0,0]
        #     '''
        # except requests.exceptions.RequestException:
        #     print("couldn't get updated position (no internet probably)")
        #     return []

        # data = req.json()
        # # print(data) # for debugging server problem, will print a lot

        # # print(data['data'][-1][3])

        # # Lat, Long, Alt
        # self.coor_alt = [data['data'][-1][3], data['data'][-1][4], data['data'][-1][5]]
        # print(self.coor_alt)
        
        

    def print_info(self):
        # prints the latest lat, long and alt of the balloon
        self.get_coor_alt()
        print("IMEI: ", self.imei)
        print("Date:", self.latest_flight)
        print("Coordinates: (", self.coor_alt[0], ", ", self.coor_alt[1], ")")
        print("Altitude: ", self.coor_alt[2])

        infoStr = "IMEI: " + self.imei + " Date: " + self.latest_flight
        infoStr += "\n" + "Coordinates: (" + str(self.coor_alt[0]) + ", " + str(self.coor_alt[1]) + ")" + " Altitude: " + str(self.coor_alt[2])
        infoStr += "\n Balloon Selected!"
        return infoStr

    def getTimeDiff(self):
        # finds the difference in time between the latest ping and the one before
        req = requests.get("https://borealis.rci.montana.edu/flight?uid={}".format(self.uid))
        data = req.json()

        lastTime = [data['data'][-1][2], data['data'][-2][2]]

        print(lastTime[0])

        print(lastTime[0] - lastTime[1])
        # return lastTime[0] - lastTime[1]
        return lastTime[0] - lastTime[1]

    pass


# import requests
# import time
#
#
# class Balloon_Coordinates:
#     BOREALIS_EPOCH = 1357023600
#
#     def __init__(self, imei):
#         self.borealis_route = True
#
#         self.imei = imei
#         self.coor_alt = []
#
#         try:
#             # Grab and Define IMEI's Latest Flight
#             req = requests.get("https://borealis.rci.montana.edu/meta/flights?imei={}".format(self.imei))
#             self.latest_flight = req.json()[-1]
#
#             # Define UID
#             flightTime = int(
#                 time.mktime(time.strptime(self.latest_flight, "%Y-%m-%d")) - 21600 - Balloon_Coordinates.BOREALIS_EPOCH)
#             self.uid = (int(flightTime) << 24) | int(self.imei[8:])
#         except:
#             self.borealis_route = False
#             latestFound = False
#             days = 0
#             while not latestFound:
#                 print(days)
#                 day_countdown = time.gmtime(time.time() - (60 * 60 * 24 * days))
#                 # print(day_countdown)
#                 date_format = str(time.strftime("%Y-%m-%d", day_countdown))
#                 print(date_format)
#                 monthRemove = False
#                 if date_format[5].find('0') != -1:
#                     date_format = date_format[:5] + date_format[6:]
#                     monthRemove = True
#                     print("hello")
#                     if str(date_format[7]).find('0') != -1:
#                         print("hi")
#                         date_format = date_format[:7] + date_format[8:]
#                         print("works here")
#                         print(date_format)
#                 try:
#                     if not monthRemove and str(date_format[8]).find('0') != -1:
#                         date_format = date_format[:8] + date_format[9:]
#                 except:
#                     pass
#                 print(date_format)
#                 #date_format = date_format[8].replace("0","")
#                 dayBool = str(requests.get(
#                         "http://eclipse.rci.montana.edu/php/getTable.php?rLim=1000000&fltDate={}&imei={}".format(
#                                 date_format, self.imei)).text).find(
#                         str(self.imei)) != -1
#                 print(date_format)
#                 print(dayBool)
#                 if dayBool:
#                     self.latest_flight = date_format
#
#                     latestFound = True
#                 else:
#                     days += 1
#
#             #self.latest_flight = "2021-7-30"
#
#         return
#
#     @staticmethod
#     def list_IMEI():
#         IMEIs = []
#         try :
#             # Request IMEI List
#             req = requests.get('https://borealis.rci.montana.edu/meta/imeis')
#             data = req.json()
#
#             for imei in data:
#                 IMEIs.append(imei)
#         except:
#             IMEIs = []
#         return IMEIs
#
#     def get_coor_alt(self):
#         if self.borealis_route:
#             req = requests.get("https://borealis.rci.montana.edu/flight?uid={}".format(self.uid))
#             data = req.json()
#             # Lat, Long, Alt
#             self.coor_alt = [data['data'][-1][3], data['data'][-1][4], data['data'][-1][5]]
#         else:
#             print("in else")
#             print(self.latest_flight)
#             req = requests.get(
#                 "http://eclipse.rci.montana.edu/php/getTable.php?rLim=1000000&fltDate={}&imei={}".format(self.latest_flight,
#                                                                                             self.imei))
#             print("After req")
#             # print(req.text)
#             dataRaw = req.text.split(str(self.imei))[1]
#             # print(dataRaw)
#             self.coor_alt = []
#             for index in range(6, 11, 2):
#                 self.coor_alt.append(float(dataRaw.split(">")[index].split("<")[0].replace(",", "")))
#             print("After Grab")
#         return self.coor_alt
#
#     def print_info(self):
#         self.get_coor_alt()
#         print("IMEI: ", self.imei)
#         print("Date:", self.latest_flight)
#         print("Coordinates: (", self.coor_alt[0], ", ", self.coor_alt[1], ")")
#         print("Altitude: ", self.coor_alt[2])
#
#         infoStr = "IMEI: " + self.imei + " Date: " + self.latest_flight
#         infoStr += "\n" + "Coordinates: (" + str(self.coor_alt[0]) + ", " + str(
#             self.coor_alt[1]) + ")" + " Altitude: " + str(self.coor_alt[2])
#         infoStr += "\n Balloon Selected!"
#         return infoStr
#
#     def getTimeDiff(self):
#         lastTime = []
#         if self.borealis_route:
#             req = requests.get("https://borealis.rci.montana.edu/flight?uid={}".format(self.uid))
#             data = req.json()
#
#             lastTime = [data['data'][-1][2], data['data'][-2][2]]
#
#
#             # return lastTime[0] - lastTime[1]
#         else:
#             req = requests.get(
#                 "http://eclipse.rci.montana.edu/php/getTable.php?rLim=1000000&fltDate={}&imei={}".format(self.latest_flight,
#                                                                                             self.imei))
#             for index in range(1, 3, 1):
#                 lastTime.append(time.mktime(time.strptime(str(req.text.split(str(self.imei))[index].split(">")[2].split("<")[0]), "%H:%M:%S")))
#
#         print(lastTime[0] - lastTime[1])
#         return lastTime[0] - lastTime[1]
#
#     pass
#
#
