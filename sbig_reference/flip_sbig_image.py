#!/usr/bin/python
#flips the SBIG images for the f9 wfs 180 degrees. 
import pyfits
import sys

def main(argv):

    infile = argv[0]
    outfile = argv[1]

    hdulist = pyfits.open(infile)
    scidata = hdulist[0].data
    imagesize = scidata.shape
    
    xcen = 1679
    ycen = 1268
    
    
    newimage = scidata*0.0
    for icol in range(0,imagesize[0]):
        for irow in range(0, imagesize[1]):
            newimage[icol-xcen,irow-ycen] = scidata[xcen-icol, ycen-irow]

    hdu = pyfits.PrimaryHDU(newimage)
    hdu.writeto(outfile)



if __name__ == "__main__":
    main(sys.argv[1:])
