import paho.mqtt.client as mqtt
import time
from threading import Thread, Lock
import logging


class Manager:
    def __init__(self, config, connection_handler,
                 subscriptions, publish_callback_handler, publish_lock, queue):
        self.keepalive_interval = 60
        self.connected_to_broker = False
        self.broker_connection_thread = None
        self.mqtt_client = None
        self.connection_handler = connection_handler
        self.subscriptions = subscriptions
        self.publish_callback_handler = publish_callback_handler
        self.publish_lock = publish_lock
        self.current_mqtt_host = config['mqtt_broker']['host']
        self.ipc_queue = queue
        self.config = config

    def start_broker_connection_thread(self):
        self.broker_connection_thread = Thread(target=self.manage_broker_connection, args=())
        self.broker_connection_thread.start()

    def _connect_to_broker(self):
        try:
            if self.mqtt_client != None:
                self.mqtt_client.loop_stop()
            # Setup MQTT Client object
            self.mqtt_client = mqtt.Client(client_id=self.config['mqtt_client']['client_id'], clean_session=False,
                                           protocol=mqtt.MQTTv311, transport="tcp")
            self.mqtt_client.username_pw_set(self.config['mqtt_client']['username'],
                                             self.config['mqtt_client']['password'])

            # Setup asynchronous client callback functions
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_disconnect = self.on_disconnect
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.on_publish = self.on_publish

            # Connect to the broker now
            self.mqtt_client.connect(self.current_mqtt_host, self.config['mqtt_broker']['port'],
                                     self.keepalive_interval)
            self.mqtt_client.loop_start()
        except Exception as error:
            print('Failed to connect to {}'.format(self.current_mqtt_host))

    def manage_broker_connection(self):
        while True:
            if self.connected_to_broker:
                # print('MQTT client is connected to {}, not doing anything'.format(self.current_mqtt_host))
                time.sleep(5)
            else:
                self._connect_to_broker()
                timeout_secs = 0
                max_timeout_secs = 7;
                while (not self.connected_to_broker) and timeout_secs < max_timeout_secs:
                    print('current_mqtt_host = {}. Waiting {} of {} seconds ...'.format(self.current_mqtt_host,
                                                                                        timeout_secs, max_timeout_secs))
                    time.sleep(1)
                    timeout_secs += 1
                if not self.connected_to_broker:
                    # Try the other host.
                    if (self.current_mqtt_host == self.config['mqtt_broker']['host']):
                        self.current_mqtt_host = self.config['mqtt_broker']['fallback']
                    else:
                        self.current_mqtt_host = self.config['mqtt_broker']['host']

                    print('Timed out. Changing MQTT host to {}'.format(self.current_mqtt_host))

    def _update_connection_status(self, status):
        if status:
            self.connected_to_broker = True
            if self.config['pi']['print_debug_messages']:
                print('Connected to broker')
        else:
            self.connected_to_broker = False
            if self.config['pi']['print_debug_messages']:
                print('Broker connection disconnected')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print('Successfully connected to {}'.format(self.current_mqtt_host))
            self._update_connection_status(True)

            self.connection_handler.on_connect()

            for subscription in self.subscriptions:
                self.mqtt_client.subscribe(topic=subscription.get_topic(), qos=subscription.get_qos())
        else:
            self._update_connection_status(False)
            print('Broker connection refused. Code = {}'.format(rc))
            self.mqtt_client.loop_stop()

    def on_disconnect(self, client, userdata, rc):
        self._update_connection_status(False)
        print('Broker disconnected. Code = {}'.format(rc))
        self.mqtt_client.loop_stop()

    def on_message(self, client, userdata, msg):
        self.ipc_queue.put(msg)

    def on_publish(self, client, userdata, mid):
        logging.debug("mid: " + str(mid))

    def publish(self, msg, topic, qos, retain, wait_for_completion=True):
        print('Publishing msg {} on topic {} with qos {} and retain {}'.format(msg, topic, qos, retain))
        with self.publish_lock:
            response = self.mqtt_client.publish(topic, payload=msg, qos=qos, retain=retain)
            if wait_for_completion:
                response.wait_for_publish()
            logging.debug('Publish msg: {} to topic: {} status: {} rc:{}'.format(str(msg), topic, response.is_published(), response.rc))

    def broker_connected(self):
        return self.connected_to_broker


class PeriodicPublish:
    def __init__(self, config, periodic_publish_handler):
        self.periodic_publish_handler = periodic_publish_handler
        self.periodic_publish_thread = None
        self.config = config

    def start(self):
        self.periodic_publish_thread = Thread(target=self.run, args=())
        self.periodic_publish_thread.start()

    def run(self):
        while True:
            self.periodic_publish_handler.handle()
            time.sleep(self.config['pi']['timers']['mqtt_publish_rate'])



