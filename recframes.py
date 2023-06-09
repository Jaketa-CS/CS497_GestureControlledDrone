from djitellopy import Tello
import cv2 as cv
import os

#w = 
#h = 

d = Tello()
d.connect()

outdir = 'recImages'
filename = 'counter.txt'
myfile   = open(filename, 'r')
runcount = int(myfile.read())
myfile.close()

print('Running run #{}...'.format(runcount))

d.streamon()

recording = False

outImages = []

cv.namedWindow('LiveFeed', cv.WINDOW_NORMAL)
if not os.path.exists(outdir):
    os.mkdir(outdir)
os.chdir(outdir)
while True:
    frame = d.get_frame_read().frame
    #frame = cv.resize(frame, (w, h))
    cv.imshow('LiveFeed',frame)
    val = cv.waitKey(1)
    if val & 0xFF == ord('q'):
        break
    if val & 0xFF == ord(' '):
        recording = True if not recording else False
    if recording:
        cv.setWindowTitle('LiveFeed', 'Recording')
        outImages.append(frame)
    else:
        cv.setWindowTitle('LiveFeed', 'Not Recording')
        if len(outImages) > 0:
            newdir = 'run{}'.format(runcount)
            os.mkdir(newdir)
            os.chdir(newdir)
            for i, img in enumerate(outImages):
                cv.setWindowTitle('LiveFeed', 'Saving')
                cv.imwrite('{}.jpg'.format(i), img)
            runcount = runcount + 1
            outImages = []
            os.chdir('..')

os.chdir('..')
d.streamoff()
d.end()

myfile = open(filename, 'w')
# runcount = runcount + 1
myfile.write(str(runcount))
myfile.close()
