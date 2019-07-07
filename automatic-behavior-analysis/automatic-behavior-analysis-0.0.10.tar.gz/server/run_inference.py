import os
import sys
import json
import argparse
import pprint
import cv2
import numpy as np
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # to import util
from run_server import ModelConfig, load_config
from client.config import ClientConfig
from analitics.annotation import Video_Annotation
from analitics.analysis import preprocess_video_annotation, RT_frame_processing
from analitics.summary import summarize_video_annotation
from analitics.saver import save_annotation, FrameSaver
from util.numpy_encoder import NumpyEncoder
from util.object_dict import ObjectDict
from util.dummy_object import DummyModel, EmptyModel
from util.video_tools import VideoSaver, FrameDecorator

class Application:
    def __init__(self):
        self.pp = pprint.PrettyPrinter(indent=2)
        self.pprint = self.pp.pprint

    def process_frame(self, frame, index):
        response = self.model.process_decoded_image(frame)
        response['frame_index'] = index
        # self.pprint(response)
        return response

    @staticmethod
    def frame_stream(vidcap, skip=0, max_frame=float('inf')):
        index = 0
        success = True
        while success and index <= max_frame:
            success, image = vidcap.read()
            if success: yield index, image
            if skip > 0:
                pos = round(vidcap.get(cv2.CAP_PROP_POS_FRAMES))
                index = pos + skip
                vidcap.set(cv2.CAP_PROP_POS_FRAMES, index)
            else:
                index += 1

    def process_video(self, video_path, output_dir, file_index, file_count):
        if not os.path.exists(video_path):
            raise RuntimeError("File does not exist: '{}'".format(video_path))

        if not os.path.isfile(video_path):
            raise RuntimeError("'{}' is not a file".format(video_path))

        vidcap = cv2.VideoCapture(video_path)
        if not vidcap.isOpened():
            raise RuntimeError("Invalid file format")

        config = self.config
        frame_count = round(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = vidcap.get(cv2.CAP_PROP_FPS)
        print("- file: {} ({} of {}), frames: {}, fps: {}".format(video_path, file_index + 1, file_count, frame_count, video_fps))

        # Configure output directory
        output_dir = os.path.abspath(output_dir or os.path.dirname(video_path))
        base_filename = os.path.splitext(os.path.basename(video_path))[0]        

        if config.save_video:
            video_saver = VideoSaver.create(config, output_dir, base_filename, vidcap)
            frame_decorator = FrameDecorator(config)

        if config.real_time_analysis:
            self.request_postprocessor = RT_frame_processing(
                max_memory_len=config.frame_processing_max_memory,
                sleep_thr=config.frame_processing_sleep_threshold)

        responses = { }
        report_frequency = config.report_frequency
        save_annotation_per_frame = not config.single_json if self.frame_saver.save_json else not config.skip_processing

        frame_counter = 0
        skip_frames = config.skip_frames if config.skip_seconds < 0.0001 else round(video_fps * config.skip_seconds)

        ind_frame_generator = self.frame_stream(vidcap, skip_frames, config.max_frame or frame_count)
        if report_frequency > 0:
            ind_frame_generator = tqdm(ind_frame_generator, mininterval=1)

        for index, frame in ind_frame_generator:
            # print(frame)
            response = self.process_frame(frame, index)

            if config.real_time_analysis:
                response = self.request_postprocessor.process_frame(frame, response)

            responses[index] = response

            if config.save_frames and (not config.skip_empty or len(response.get('dogs') or []) > 0) and (config.save_delta < 1 or frame_counter % config.save_delta == 0):
                self.frame_saver.save(base_filename, index, frame, response if save_annotation_per_frame else None)

            if config.save_video:
                video_saver.add_frame(frame_decorator.decorate(frame, response))

            frame_counter += 1

        if config.save_video:
            video_saver.close()

        if config.single_json or config.produce_summary:
            annotation = Video_Annotation(video_path)
            annotation.set_frame_annotations(responses)
            annotation = preprocess_video_annotation(annotation) # Fix sleep detection

        if config.single_json:
            output_path = os.path.join(output_dir, base_filename + ".json")
            print("Saving combined annotation file:", output_path)
            annotation.save_annotation(output_path, indent=2, sort_keys=True) # Produce annotation file

        # Produce summary file
        if config.produce_summary:
            options = ObjectDict({
                'video_fps': video_fps,
                'max_detection_targets': config.max_detection_targets })
            summary = summarize_video_annotation(annotation, options)
            summary_path = os.path.join(output_dir, base_filename + ".summary.json")
            save_annotation(summary_path, summary, indent=2, sort_keys=True, cls=NumpyEncoder)

    def process_input(self, config, input_files, depth=0):
        dirs = sorted(filter(lambda item: os.path.isdir(item), input_files))
        videos = sorted(filter(lambda item: item.endswith(config.video_extension), input_files))
        count = len(videos)
        for index, file in enumerate(videos):
            try:
                self.process_video(file, config.output_dir, index, count)
            except Exception as ex:
                print("Exception while processing {}".format(file))
                import traceback
                traceback.print_exc()
        if not config.recursive and depth > 0: return
        for entry in dirs:
            children = [os.path.join(entry, item) for item in os.listdir(entry)]
            self.process_input(config, children, depth + 1)

    def set_config(self, config):
        self.config = config

    def init(self):
        self.frame_saver = FrameSaver(self.config)
        if self.config.skip_processing:
            self.model = EmptyModel()
        else:
            from model_controller import ModelController
            self.model = ModelController(self.config)
            # self.model = DummyModel("data/client-saved-frames/annotations-json/07_20180519073056_00000684.json")
        
    def run(self):
        """Main function"""
        parser = argparse.ArgumentParser(description='Batch analysis tool')
        #parser.add_argument('--output-dir', help="Directory where the output will be written to (default: frame dump directory as defined in client config)", default=argparse.SUPPRESS)
        parser.add_argument('--report-frequency', help="Print a progress report after every k frames (default: %(default)s)", default=1, type=int)
        parser.add_argument('--produce-summary', help="Calculate and save sleeping pattern statistics", action='store_true')
        parser.add_argument('--save-frames', help="Save every processed frame into an image file", action='store_true')
        parser.add_argument('--save-delta', help="Skip saving (process but don't save) every k frames (default: %(default)s)", default=0, type=int)
        parser.add_argument('--real-time-analysis', help="Run sequential image analysis algorithms (e.g. motion detection)", action='store_true')
        parser.add_argument('--save-video', help="Produce an output video with visible bounding boxes and labels", action='store_true')
        parser.add_argument('--skip-empty', help="Don't save frames with no detected objects", action='store_true')
        parser.add_argument('--skip-processing', help="Do a dry run without running the inference model", action='store_true')
        parser.add_argument('--skip-frames', help="Skip (don't process) every k frames (default: %(default)s)", default=0, type=int)
        parser.add_argument('--skip-seconds', help="Skip (don't process) every t seconds (default: %(default)s)", default=0.0, type=float)
        parser.add_argument('--max-frame', help="Finish processing after this frame was reached", default=0, type=int)
        parser.add_argument('--video-extension', help="The extension for video files (default: %(default)s)", default='mp4')
        parser.add_argument('--image-extension', help="The extension for image files (default: %(default)s)", default='jpg')
        parser.add_argument('--recursive', help="Recursively descend into subdirectories", action='store_true')
        parser.add_argument('--config-file', help="Configuration file")
        parser.add_argument('--annotation-format', help="Format of image annotation files (default: %(default)s)", default='pascal-voc', choices=['json', 'pascal-voc'])
        parser.add_argument('--single-json', help="Use a single annotation file for all images (only has effect if the json format is used)", action='store_true')
        parser.add_argument('--input_files', help="List of input files or directories", nargs='+')
        parser.add_argument('--output_dir', help="Output directory")
        args = vars(parser.parse_args())
        config = load_config(ModelConfig, args.get('config_file'))
        client_config = load_config(ClientConfig, "client/config.json")
        config.update(client_config)
        config.update(args)
        config.output_dir = args.get('output_dir', config.frame_dump_dir)
        # self.pprint(config)
        self.set_config(config)
        self.init()
        self.process_input(config, config.input_files)

if __name__ == '__main__':
    Application().run()