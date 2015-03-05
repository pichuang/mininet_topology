#!/usr/bin/env python2                                                                       
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController
from mininet.cli import CLI 
from mininet.link import Intf
from mininet.util import dumpNodeConnections
import os
import shutil

REMOTE_CONTROLLER_IP="10.211.55.56"
TEST_DIR_PATH="/tmp/"

str1 = '''\
11111111111111
11111111111111
11111111111111
'''

str2 = '''\
22222222222222
22222222222222
22222222222222
'''


def CreateTestFile():
    ''' 
    mkdir & create file
    '''
    if os.path.isdir(TEST_DIR_PATH + "mininet_two_web") == False:
        os.mkdir(TEST_DIR_PATH + "mininet_two_web/")
        os.mkdir(TEST_DIR_PATH + "mininet_two_web/web1")
        os.mkdir(TEST_DIR_PATH + "mininet_two_web/web2")
        file_1 = open(TEST_DIR_PATH + "mininet_two_web/web1/index.html", "w")
        file_1.writelines(str1)
        file_1.close()
        file_2 = open(TEST_DIR_PATH + "mininet_two_web/web2/index.html", "w")
        file_2.writelines(str2)
        file_2.close()
    
    else:
        print "You have the same name directory"
        print "Please check: " + TEST_DIR_PATH + "mininet_two_web\n"

def CleanTestFile():
    ''' 
    deldir
    '''
    if os.path.isdir(TEST_DIR_PATH + "mininet_two_web") == True:
            shutil.rmtree(TEST_DIR_PATH + "mininet_two_web")
    else:
        print "Nothing can be delete" 


def MininetTopo():
    '''
    Prepare Your Topology
    '''
    net = Mininet (topo=None, build=False)
    
    controller = net.addController(name='controller0', 
                                    controller=RemoteController, 
                                    ip=REMOTE_CONTROLLER_IP,
                                    port=6633)
     
    info("Create Host node\n")
    host1 = net.addHost('h1', ip='10.0.0.1')
    host2 = net.addHost('h2', ip='10.0.0.2')
    web1 = net.addHost('web1', ip='10.0.0.3')
    web2 = net.addHost('web2', ip='10.0.0.4')
            
    info("Create Switch node\n")
    switch = net.addSwitch('ovs1')
            
    info("Link switch to host\n")
    net.addLink(switch, host1)
    net.addLink(switch, host2)
    net.addLink(switch, web1)
    net.addLink(switch, web2)


    '''
    Working your topology
    '''
    info("Start network\n")
    net.start()

    info("Dumping host connections\n")
    dumpNodeConnections(net.hosts)

    info("Testing network connectivity\n")
    net.pingAll()

    info("Build web server\n")
    web1.cmdPrint('cd ' + TEST_DIR_PATH +'mininet_two_web/web1/ && python2 -m SimpleHTTPServer 80 >& '+ TEST_DIR_PATH +'mininet_two_web/web1/http-web1.log &')
    web2.cmdPrint('cd ' + TEST_DIR_PATH +'mininet_two_web/web2/ && python2 -m SimpleHTTPServer 80 >& '+ TEST_DIR_PATH +'mininet_two_web/web2/http-web2.log &')
    
    info("Help yourself\n")
    info("Try it: h1 wget -O - 10.0.0.3\n")
    info("Try it: h1 wget -O - web2\n")
    CLI(net)
    
    
    '''
    Clean mininet
    '''
    web1.cmdPrint('kill %python')
    web2.cmdPrint('kill %python')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    CreateTestFile()
    MininetTopo()
    CleanTestFile()                                                                                                                                                                   
