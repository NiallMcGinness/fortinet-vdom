import paramiko
import time
import sys
import re
from vdom import vdom
from nonvdom import nonvdom

args = sys.argv

try:
    ip = args[1]
except IndexError:
    print("no ip provided")
    sys.exit(1)

try:
    router_username = args[2]
    router_pwd = args[3]
    modem_username = args[4]
    modem_pwd = args[5]
except IndexError:
    print("no args provided") 
    sys.exit(1)


def runSshCmd(hostname, username, password,timeout=30):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=2222 , username=username, password=password,
                allow_agent=False, look_for_keys=False, timeout=30)

    except paramiko.SSHException:
        print("ssh error")
        client.close()
    output = ""    
    channel = client.invoke_shell()
    isVDOM = checkVDOM(channel)
    if isVDOM == True:
        runVDOM(channel)
    else:
        runNonVDOM(channel)
    time.sleep(2)
    client.close()


def checkVDOM(channel):
    isVDOM = False
    cmd = "diag sys link interface wan1\r"
    channel.send(cmd)
    time.sleep(1)
    output = channel.recv(9999).decode('utf-8')
    #print(output)
    errorStringPos = output.find("Unknown action")
    if errorStringPos != -1:
        isVDOM = True
    return isVDOM


def runVDOM(channel):
    v = vdom(channel, modem_pwd)
    ip = v.getWanIp()
    print("ip  : {} ".format(ip ) )

def runNonVDOM(channel):
    nv = nonvdom(channel, modem_pwd)
    ip = nv.getWanIp()
    print("ip  : {} ".format(ip ) )
    

runSshCmd(ip, router_username, router_pwd)