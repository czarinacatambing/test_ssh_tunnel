# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
# Ported to Airflow by Bolke de Bruin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import getpass
import os

import shlex
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook
import logging
import getpass
import os
import socket
import select
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer


class AstroSSHHook(BaseHook):

    def __init__(self):
        super().__init__(ssh_conn_id)

    def create_tunnel(self, local_port, identityfile,
                      remote_port=None, remote_host="localhost"):
        """
        Creates a tunnel between two hosts. Like ssh -L <LOCAL_PORT>:host:<REMOTE_PORT>.
        Hard coded in for now. Down the line, it will pull from connections panel.

        """
        import subprocess

        localport = '5439'
        remoteport = '5439'
        user = 'periscope'
        server = '52.10.89.212'
        incoming_port = 17386
        key = Variable.get("key_file")
        identityfile = 'key_file.pem'

        # Write the key to a file to change permissions
        # The container dies after the task executes, so don't have to
        # worry about closing/deleting it.
        with open("key_file.pem", "w") as key_file:
            key_file.write(key)

        print(os.listdir())

        # Permissions are set as an octal integer.
        os.chmod("key_file.pem", 1130)

        sshTunnelCmd = "ssh -N -L -4 {localhost}:127.0.0.1:{remote_port} -i %{identityfile} {user}@%{server}".format(
            localhost=localport,
            remoteport=remoteport,
            identityfile=identityfile,
            user=user,
            server=server
        )
        print(sshTunnelCmd)
        logging.info(sshTunnelCmd)

        args = shlex.split(sshTunnelCmd)
        tunnel = subprocess.Popen(args)