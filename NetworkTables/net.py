import time
from networktables import NetworkTable

# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)


NetworkTable.setIPAddress("10.23.95.2") #Change the address to your own
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable("SmartDashboard")
sd.putNumber('cX',200)
sd.putNumber('cY',200)

try:
    while True:
        x=0
        for x in range(100):
            sd.putNumber('cX',x)
            time.sleep(1)
            print x

        time.sleep(1)
except:
    exit();
