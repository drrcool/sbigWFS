#!/usr/bin/python
from urllib2 import urlopen
from time import gmtime, strftime, localtime
import sys


#This is a basic wrapper that calls the API 
def SendSBIGCommand(command):

    #The default hostname for the camera.
    campath = 'http://f9sbig.mmto.arizona.edu/'
    campath = campath + 'api/' # Just for ease later

    #Send the HTTP API request
    request = urlopen(campath + command)

    return request


#This program will download the last image taken by the
#SBIG camera
def DownloadImage(outname):

    #This is the default test image name (if one is not provided)
    
    

    #Down the image
    imagedata = SendSBIGCommand("Imager.FIT")
    f = open(outname, "wb")
    f.write(imagedata.read())
    f.close()

#Expose an image
#Inputs -- expTime : exposure time in seconds
#          imType : integer (0 = Dark, 1 = Light, 2=Bias, 3=Flat Field)
def ExposeImage(expTime, imType):
    
    time = strftime("%Y-%m-%dT%H:%M:%S.000", localtime())
    req = SendSBIGCommand("ImagerStartExposure.cgi?Duration=%.2f&FrameType=%d&DateTime=%s" % (expTime, imType,time))
    err_code = req.read()
    
    print("Starting Exposure.")
    ImagerState = -1
    PostedReadOut = 0
    while (ImagerState != 0) and (ImagerState != 5):
        req = SendSBIGCommand("ImagerState.cgi")
        if req:
            ImagerState = int(req.read())
            
        if (ImagerState == 3) and (PostedReadOut == 0):
            print("Reading out") 
            PostedReadOut = 1

    #ImagerState = 5 is an error mode
    if (ImagerState == 5):
        print("Imager State Error.")
        return
    



#Turn on cooling
def EnableCooling():
    
    req = SendSBIGCommand("ImagerSetSettings.cgi?CoolerState=1&CCDTemperatureSetpoint=25&FanState=2")
    

#Turn off cooling
def DisableCooling():
    req = SendSBIGCommand("ImagerSetSettings.cgi?CoolerState=0")
    

def main(argv):

    try:
        command = argv[0].lower()
        

    except:
        print("SBIG Encountered a Problem!\n")
        print("No Command line options set.:")
        print("TAKE AN EXPOSURE : ./sbig.py observe EXPTIME OUTNAME (imagetype -- optional)")
        print("TURN ON COOLING : ./sbig.py CoolerOn")
        print("TURN OFF COOLING : ./sbig.py CoolerOff")
        return

    if command == 'observe':
        try :
            expTime = float(argv[1])
        except :     
            print("SBIG Encountered a Problem!\n")
            print("Bad (or no) exposure time provided.")
            print("TAKE AN EXPOSURE: ./sbig.py observe EXPTIME OUTNAME (imagetype -- optional)")
            print("If taking a bias, use an exposure time of 0")
            return

                
        try : 
            outname = argv[2]
        except:
            print("SBIG Encountered a Problem!\n")
            print("Bad (or no) output filename provided.")
            print("TAKE AN EXPOSURE: ./sbig.py observe EXPTIME OUTNAME (imagetype -- optional)")
            return

        imagetype = 'object'
        if len(argv) > 3:
            imagetype = argv[3].lower()
            if ( (imagetype != 'object') and                   
                 (imagetype != 'dark') and 
                 (imagetype != 'bias') and 
                 (imagetype != 'zero')):
                
                print("The only image types allowed are object, dark, bias, zero. Not setting an image type defaults to object.")
                return
                        
        if imagetype == 'object':
            imType = 1
        if imagetype == 'dark' : 
            imType = 0
        if imagetype == "bias" : 
            imType = 2
            expTime = 0
        if imagetype == 'zero' : 
            imType = 2
            expTime = 0
                          
        ExposeImage(expTime, imType)
        DownloadImage(outname)
        
                    
          
                


           
        
            
    


if __name__ == "__main__":
    main(sys.argv[1:])    
       

    
