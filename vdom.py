import paramiko
import time
import sys
import re

class vdom(object):
    def __init__(self, channel, modem_password):
        self.channel = channel
        self.modem_password = modem_password
        self.output = ""
    
    def listAll(self):
        self.channel.send('config global \r')
        #exit_status = self.channel.recv_exit_status()
        #print("exit_status {} ".format(exit_status))
        time.sleep(2)
        vdom_list = self.channel.send('get sys vdom-property \r')
        time.sleep(2)
        self.channel.send('end \r')
        return vdom_list  

    def getWanIp(self):
        self.channel.send('conf vdom \r')
        time.sleep(2)
        self.channel.send('edit WAN1 \r')
        time.sleep(2)
        self.channel.send('get sys arp \r')
        time.sleep(2)
        arplist = self.channel.recv(9999).decode('utf-8')
        print("arplist ", arplist)
        self.output += arplist
        reip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', arplist )
        if len(reip) > 0:
            ip = reip[0]
        else:
            ip = None
        return ip

    def getOutput(self):
        return self.output