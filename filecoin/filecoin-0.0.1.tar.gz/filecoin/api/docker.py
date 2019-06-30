# coding: utf8
from xserver.docker_image.utils import build_docker_image
import os

orignal_docker_file_content = """FROM ubuntu:18.04
RUN mkdir -p /downloads
RUN apt-get update
RUN apt-get install wget nano -y
RUN wget -O/downloads/filecoin.tar.gz  https://github.com/filecoin-project/go-filecoin/releases/download/0.2.2/filecoin-0.2.2-Linux.tar.gz
RUN tar -zxvf /downloads/filecoin.tar.gz -C /downloads
RUN rm /downloads/filecoin.tar.gz
RUN cp /downloads/filecoin/* /usr/local/bin
RUN rm -rf /downloads/filecoin
RUN apt-get install lsof python python-pip -y
CMD ["/usr/local/bin/go-filecoin", "daemon"] 
"""



def build_filecoin_image(version='0.2.4'):
    docker_file_content = orignal_docker_file_content.replace('0.2.2', version)
    build_docker_image(image_name='fil', image_version=version, docker_file_content=docker_file_content)



def start_filecoin(node_name, port, node_id=None, image_version='0.2.4'):
    data_dir = '/data/filecoin/%s' % node_name
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    cmd = 'docker  run -it   -p %s:%s --name %s -v %s:/root/.filecoin hepochen/fil:%s /bin/bash' % (port, port, node_name, data_dir, image_version)
    print('init it first in other window!!')
    print(cmd)
    print('\n')
    cmd2 = 'go-filecoin init --devnet-user --genesisfile=http://user.kittyhawk.wtf:8020/genesis.car --auto-seal-interval-seconds=20'
    if node_id:
        cmd2 += ' --default-address=%s' % node_id
    print(cmd2)
    print('\n'*2)
    print('re_config_node("%s")' % node_name)
    print('\n' * 2)
    print('docker rm -f %s' % node_name)
    print('\n' * 2)
    new_cmd = 'docker run -d -p %s:%s --name %s -v %s:/root/.filecoin hepochen/fil:%s' % (port, port, node_name, data_dir, image_version)
    print(new_cmd)


    # docker  run -it   -p 192.99.0.225:6000:6000 --name fnode1 -v /data/filecoin/node1:/root/.filecoin hepochen/fil:0.2.2 /bin/bash
