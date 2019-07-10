from util.config import Config

class ClientConfig(Config):
    _keys = [
        'protocol',
        'ip',
        'port',
        'secret_key',
        'tcp_client_buffer_size',
        'upload_buffer_max_size',
        'color_sleep',
        'color_awake',
        'color_unknown',
        'max_detection_targets',
        'frame_dump_dir',
        'json_annotation_dir',
        'xml_annotation_dir',
        'annotation_format',
        'video_extension',
        'frame_processing_max_memory',
        'frame_processing_sleep_threshold',
        'resize_threshold',
        'send_grayscale',
        'media_source_type',
        'save_annotated_video'
    ]