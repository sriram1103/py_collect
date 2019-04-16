#!/usr/bin/python

import json
import os
import sys
import socket
import subprocess

class Config():
    def __init__(self,conf_file):
        self.check_conf(conf_file)
        self.conf_file = conf_file
        self.all_conf = self.read()
        self.gen_conf = self.get_genconf()

    def check_conf(self,conf_file):
        if os.path.exists(conf_file) and os.path.getsize(conf_file) > 0: 
            pass
        else:
            raise OSError("Config file %s not found or empty"%(conf_file))

    def read(self):
        with open(self.conf_file,'r') as f:
            try:
                all_conf = json.load(f)
            except ValueError as e:
                raise e
        return all_conf

    def get_genconf(self):
        gen_conf = self.all_conf['generic']
        if not os.path.exists(gen_conf['key_file']):
            raise OSError("%s - key file not found"%(gen_conf['key_file']))
        return gen_conf

    def get_allHosts(self):
        all_host = self.all_conf['hosts']
        return [str(host) for host in all_host.keys()]
    
    def check_host(self,host):
        try:
            #resolve ip
            ip = socket.gethostbyname(host)
            # check if valid ip
            _ = socket.inet_aton(ip)
            _ = subprocess.check_call(['ping','-c','1','-W','3',host],stdout=subprocess.PIPE)
        except (socket.gaierror,socket.error) as e:
            raise e
        except subprocess.CalledProcessError as e:
            raise Exception("Unable to reach host %s"%(host))
        
        

    def get_host(self,host):
        all_host = self.all_conf['hosts']
        if host in all_host.keys():
            self.check_host(host)
            host_conf = all_host[host]
            for key in ['user_name','key_file']:
                    if not key in host_conf.keys():
                        host_conf[key] = str(self.gen_conf[key])
            return host_conf
        else:
            raise("%s - Host info not found"%(host))

    