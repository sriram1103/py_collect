#!/usr/bin/python

from ssh_conn import SSH
from collections import OrderedDict
import json

class Gather():
    def __init__(self,ssh_client,cmd_list):
        self.ssh_client = ssh_client
        with open(cmd_list,'r') as fd:
           self.cmd = json.load(fd)
        self.os_cmd = "uname -o"

    def get_output(self,cmd):
        return self.ssh_client.execute(cmd).strip()

    def gather_all(self):
        os = self.get_output(self.os_cmd)
        if not os in self.cmd.keys():
            raise Exception('No commands found for OS - ' +os)
        os_cmds = self.cmd[os]
        section_output = OrderedDict()
        for section in os_cmds.keys():
            output = OrderedDict()
            for des,cmd in os_cmds[section].iteritems():
                output[des] = self.get_output(cmd)
            section_output[section] = output
        return section_output

        