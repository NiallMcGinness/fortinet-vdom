import paramiko
import time
import sys
import re

class nonvdom(object):
    def __init__(self, channel, modem_password):
        self.channel = channel
        self.modem_password = modem_password
        self.output = ""
	
    def getWanIp(self):
        wan_output = ""
        self.channel.send('get sys arp \r')
        time.sleep(2)
        wan_output = self.channel.recv(9999).decode('utf-8')
        print("wan output ", wan_output)
        ip = self.parseARP(wan_output)
        return ip

    def parseARP(self,arplist):
        lines = arplist.splitlines()
        match = ""
        ip = None
        for line in lines:
            match = re.search('wan1', line, re.IGNORECASE)
            if match is not None:
                split = line.split()
                ip =  split[0]
        return ip
    
   
    def getOutput(self):
        return self.output