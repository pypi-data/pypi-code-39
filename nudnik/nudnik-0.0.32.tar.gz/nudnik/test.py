#!/usr/bin/python3

import etcd3
from datetime import datetime
import time
import uuid

client = etcd3.client(host='127.0.0.1', port=2379)
print(client)

watches = {}

def watch_callback(event):
    print("Handling event callback")
    key = event.key.decode("utf-8")
    print("Key: " + key)
    if type(event) == etcd3.events.DeleteEvent:
        print("Deleting: {} {}".format(key, watches[key]))

        client.delete(key)
        client.cancel_watch(watches[key])
        del watches[key]
    else:
        print(event)
        print(event.key)

index = 0
while True:
    print(watches)
    time_now = str(datetime.utcnow())
    key = '/test/{}'.format(index)
    client.put(key, time_now)
    watch_id = client.add_watch_callback(key, watch_callback)
    watches[key] = watch_id
    index += 1
    time.sleep(5)
