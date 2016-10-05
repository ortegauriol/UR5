#!/usr/bin/python
import PyDragonfly
from PyDragonfly import copy_from_msg
import Dragonfly_config as rc
from dragonfly_utils import respond_to_ping 

import time
import sys
import socket
from socket import gethostname, gethostbyname
from argparse import ArgumentParser

import numpy as np
import Sanity
from amcmorl_py_tools.vecgeom.transformations import Rz

MID_CONSUMER = 11

host = '192.168.56.2'
port = 30000

class UR5Interface(object):
    def __init__(self):
        # create socket
        print("Trying to connect to %s:%s" % (host, port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)
        self.c, addr = s.accept()
        self.connected = True # an assumption that is hopefully safe
        print 'Got connection from', addr       # Confirm connection
        
        
    def send_movement_command(self, position, max_velocity, acceleration, timeout=1):
        # sanity_check data # Ensuring the positions, velocity and acceleration are reasonable
        x, y, z, rx, ry, rz = position[:]
        print "x", x, "y", y, "z", z
        if Sanity.check(acceleration, max_velocity, x, y, z):       
            pos_str = ','.join([str(k) for k in position])
            acc_str = str(acceleration)
            vel_str = str(max_velocity)
            msg = '(' + ','.join([pos_str, acc_str, vel_str]) + ')'
            
            # send message to UR5
            print "Sending command:", msg
            self.c.send(msg) 
            
            # wait for (with timeout) and receive movement_complete message
            message = self.c.recv(1024)
            #time.sleep(2.)
            #message = 'movement complete'
            print "Received message", message
            return message.lower() == 'movement complete'
        else:
            print "Sanity check failed."
            return False
        
class UR5Control(object):
    def __init__(self, config_file, mm_ip):
        self.setup_dragonfly(mm_ip)
        self.ur5 = UR5Interface()
        if self.ur5.connected:
            self.mod.SendSignal(rc.MT_UR5_CONNECTED)
        
        #self.load_config(config_file)
        self.run()
        
    def setup_dragonfly(self, mm_ip):
        self.mod = PyDragonfly.Dragonfly_Module(0, 0)
        self.mod.ConnectToMMM(mm_ip)
        self.mod.Subscribe(rc.MT_PING)
        self.mod.Subscribe(rc.MT_UR5_MOVEMENT_COMMAND)
        self.mod.Subscribe(rc.MT_UR5_REQUEST_CONNECTED)
        self.mod.SendModuleReady()

    def load_config(self, config_file):
        cfg = SafeConfigParser()
        cfg.read(config_file)
        self.config = Config()

        # main section
        self.config.rz = Rz(cfg.getint('main', 'rz'))
    
    def run(self):
        while True:
            msg = PyDragonfly.CMessage()
            self.mod.ReadMessage(msg)                                    # blocking read
            print "Received message ", msg.GetHeader().msg_type

            if msg.GetHeader().msg_type == rc.MT_UR5_MOVEMENT_COMMAND:
                msg_data = rc.MDF_UR5_MOVEMENT_COMMAND()
                copy_from_msg(msg_data, msg)
                #position = np.frombuffer(msg_data.position)
                #print "  Data = [X: %d, Y: %d, Z: %f]" % \
                #    (msg_data.position[0], msg_data.position[1], msg_data.position[2])
                movement_complete = self.ur5.send_movement_command(msg_data.position, 
                                                                   msg_data.max_velocity,
                                                                   msg_data.acceleration)
                if movement_complete:
                    # send movement complete message
                    self.mod.SendSignal(rc.MT_UR5_MOVEMENT_COMPLETE)
                else:
                    # print ur5 error message
                    print "No movement complete received."
                    
            elif msg.GetHeader().msg_type == rc.MT_UR5_REQUEST_CONNECTED:
                if self.ur5.connected:
                    self.mod.SendSignal(rc.MT_UR5_CONNECTED)
                # ideally we'd capture not connected, but not today...
                
            elif msg.GetHeader().msg_type == rc.MT_PING:
                respond_to_ping(self.mod, msg, 'UR5Control')
             
    def close(self):
        self.mod.DisconnectFromMMM()
        self.c.close()

if __name__ == "__main__":
    parser = ArgumentParser(description = 'Control UR5 robot')
    parser.add_argument(type=str, dest='config')
    parser.add_argument(type=str, dest='mm_ip', nargs='?', default='')
    args = parser.parse_args()
    print("UR5 Control: Using config file=%s, MM IP=%s" % (args.config, args.mm_ip))

    ur5ctrl = UR5Control(args.config, args.mm_ip)
    print "UR5 Control running...\n"  
