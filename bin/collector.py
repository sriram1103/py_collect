#!/usr/bin/python

import sys
import os

my_dir = sys.path[0]
conf_dir = os.path.dirname(my_dir) +'/conf/'
conf_file = conf_dir + 'host_config.json'
cmds_file = conf_dir + 'command_list.json'
lib_dir = os.path.dirname(my_dir) + '/lib'

sys.path.append(lib_dir)

from config_parser import Config
from ssh_conn import SSH
from gather import Gather
from pretty_print import PrettyPrint

def main():
    conf_parser = Config(conf_file)
    ssh_client = SSH()
    pp = PrettyPrint()
    #output_data = {}
    for host in conf_parser.get_allHosts():
        host_params = conf_parser.get_host(host)
        host_params['host'] = host
        ssh_client.connect(host_params)
        gather_obj = Gather(ssh_client,cmds_file)
        host_data = gather_obj.gather_all()
        pp.fprint({host:host_data})


if __name__ == "__main__":
    main()