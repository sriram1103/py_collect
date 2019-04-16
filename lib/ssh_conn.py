#!/usr/bin/python

from paramiko import AuthenticationException
from paramiko import AutoAddPolicy
from paramiko.client import SSHClient
from paramiko.client import SSHException
from paramiko.client import BadHostKeyException
import socket

class SSH():
    def __init__(self):
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.conn = ''
    
    def connect(self,params):
        host = params['host']
        user_name = params['user_name']
        use_pass = False
        if 'password' in params.keys():
            password = params['password']
            use_pass = True
        else:
            key_file = params['key_file']
        
        try:
            if use_pass:
                self.client.connect(host,username=user_name,password=password)
            else:
                self.client.connect(host,username=user_name,key_filename=key_file)
        except (BadHostKeyException,AuthenticationException,SSHException,socket.error) as e:
            print "Unable to connect to host - " + host
            raise e


    def execute(self,cmd):
        try:
            _ , stdout, stderr =  self.client.exec_command(cmd)
            err = stderr.readlines()
            if err:
                raise Exception(err)
            return stdout.read()
        except (SSHException) as e:
            raise e

    def close(self):
        self.client.close()
    
