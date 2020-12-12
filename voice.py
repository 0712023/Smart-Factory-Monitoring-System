#python3 demo.py resources/models/snowboy1.umdl resources/models/snowboy2.umdl
#snowboydecoer.py must be at the same path with initiate.py


import snowboydecoder
import sys
import signal

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 3:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

models = sys.argv[1:]
print(models)

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

def callback1(): #initiate detected
    log = open('/home/pi/test.txt', "a")
    log.write("start function\n")
    log.close()

def callback2(): #stop detected
    log = open('/home/pi/test.txt', "a")
    log.write("break loop\n")
    log.close()

callbacks = [callback1, callback2]

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
