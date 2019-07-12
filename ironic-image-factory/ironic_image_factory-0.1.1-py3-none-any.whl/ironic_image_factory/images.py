import os
import sys
import urllib3
from keystoneauth1.identity import v3
from keystoneauth1 import session as keystone_session
from keystoneclient.v3 import client as keystone_client
from ironicclient import client as ironic_client
from novaclient import client as nova_client
import glanceclient
import wget
import tempfile
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLIENTS = {}


def load_auth_clients():
    auth_fields = {
        'auth_url': os.environ['OS_AUTH_URL'],
        'username': os.environ['OS_USERNAME'],
        'password': os.environ['OS_PASSWORD'],
        'project_name': os.environ['OS_PROJECT_NAME'],
        'user_domain_name': os.environ['OS_USER_DOMAIN_NAME'],
        'project_domain_name': os.environ['OS_PROJECT_DOMAIN_NAME']
    }

    v3_auth = v3.Password(**auth_fields)
    ks_sess = keystone_session.Session(auth=v3_auth, verify=False)
    ks_client = keystone_client.Client(session=ks_sess)
    CLIENTS['keystone'] = ks_client

    gl_client = glanceclient.Client('2', session=ks_sess)
    CLIENTS['glance'] = gl_client

    nv_client = nova_client.Client(2, session=ks_sess)
    CLIENTS['nova'] = nv_client


def upload_new_images():
    image_urls = {"Alpine Linux-3.9": "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/Alpine/3.9/2019-07-08/alpine-3.9-2019-07-08.qcow2",
                 "CentOS-6": "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/CentOS/6/2019-07-08/centos-6-2019-07-08.qcow2",
                 "CentOS-7": "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/CentOS/7/2019-07-08/centos-7-2019-07-08.qcow2",
                 "Debian-Jessie64"  : "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/Debian/jessie64/2019-07-08/debian-jessie64-2019-07-08.qcow2",
                 "Debian-Stretch64" : "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/Debian/stretch64/2019-07-08/debian-stretch64-2019-07-08.qcow2",
                 "Ubuntu-Trusty64" : "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/Ubuntu/trusty64/2019-07-08/ubuntu-trusty64-2019-07-08.qcow2",
                 "Ubuntu-Xenial64" : "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/Ubuntu/xenial64/2019-07-08/ubuntu-xenial64-2019-07-08.qcow2",
                 "Ubuntu-Bionic64" : "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/Ubuntu/bionic64/2019-07-08/ubuntu-bionic64-2019-07-08.qcow2",
                 "Ubuntu-Cosmic64" : "https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com/Ubuntu/cosmic64/2019-07-08/ubuntu-cosmic64-2019-07-08.qcow2"}
    
    glance = CLIENTS['glance']

    images = glance.images.list()
    image_checksums = [image.checksum for image in images]
    for name,url in image_urls.items():
        with tempfile.TemporaryDirectory() as tempdir:
            etag  = requests.head(url).headers['ETag']
            if etag not in image_checksums:
               image_download = wget.download(url, tempdir)
               glance_image = glance.images.create(name=name, is_public="True", disk_format="qcow2",
                       container_format="bare", tags=["RackspaceManaged"])
               print('')
               print("Uploading "+name+" to Glance")
               glance.images.upload(glance_image.id, open(image_download, 'rb'))
    
def main():
    load_auth_clients()
    upload_new_images()
    print('')
    print("Image Updates are Complete")


if __name__ == "__main__":
    main()
