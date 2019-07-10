import os
import sys
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # to import util
from util.config import Config
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class ModelConfig(Config):
    _keys = [
        'model_root',
        'model_version',
        'model_path_detector_graph',
        'model_path_detector_label_map',
        'model_path_classifier_weights',
        'model_path_classifier_scheme',
        'model_path_eye_detector_graph',
        'model_path_eye_detector_label_map',
        'use_classifier',
        'use_eye_detector',
        'target_classes',
        'eye_target_classes',
        'max_detection_targets',
        'box_overlap_threshold',
        'convert_to_grayscale'
    ]

class ServerConfig(ModelConfig):
    _keys = ModelConfig._keys + [
        'protocol',
        'port',
        'secret_key',
        'tcp_server_max_conn',
        'tcp_server_buffer_size',
        'upload_buffer_max_size'
    ]

def load_config(config_class, config_file):
    return config_class(config_file or os.path.join(os.path.dirname(__file__), "config/config.json"))

class Application:
    def server_started(self, name, ip, port):
        print("{} started on {}:{}".format(name, ip, port))

    def start(self):
        """Main function"""
        parser = argparse.ArgumentParser(description='Data analysis server')
        parser.add_argument('--ip', default='127.0.0.1', help="IP address of the interface to listen on (use 0.0.0.0 for all interfaces)")
        parser.add_argument('--port', default=1217, help="Server port", type=int)
        parser.add_argument('--protocol', default='tcp', help="Server protocol", choices=['tcp', 'websocket'])
        parser.add_argument('--config-file', help="Configuration file")
        parser.add_argument('--verbose', help="Show detailed debug messages", action='store_true')
        args = vars(parser.parse_args())
        config = load_config(ServerConfig, args.get('config_file'))
        config.update(args)

        if config.protocol == 'tcp':
            from custom_tcp_server import CustomTCPServer
            server = CustomTCPServer("Custom TCP server", config)
        elif config.protocol == 'websocket':
            from websocket_server import WebSocketServer
            server = WebSocketServer("WebSocket server", config)
        else:
            raise RuntimeError("Invalid server protocol: {}".format(config.protocol))

        server.start(config.ip, config.port, self.server_started)

if __name__ == '__main__':
    Application().start()