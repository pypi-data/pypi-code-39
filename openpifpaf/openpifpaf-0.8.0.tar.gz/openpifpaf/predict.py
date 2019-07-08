"""Predict poses for given images."""

import argparse
import glob
import json
import logging
import os

import numpy as np
import PIL
import torch

from .network import nets
from . import datasets, decoder, show, transforms


def cli():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    nets.cli(parser)
    decoder.cli(parser, force_complete_pose=False, instance_threshold=0.1, seed_threshold=0.5)
    parser.add_argument('images', nargs='*',
                        help='input images')
    parser.add_argument('--glob',
                        help='glob expression for input images (for many images)')
    parser.add_argument('-o', '--output-directory',
                        help=('Output directory. When using this option, make '
                              'sure input images have distinct file names.'))
    parser.add_argument('--show', default=False, action='store_true',
                        help='show image of output overlay')
    parser.add_argument('--output-types', nargs='+', default=['skeleton', 'json'],
                        help='what to output: skeleton, keypoints, json')
    parser.add_argument('--batch-size', default=1, type=int,
                        help='processing batch size')
    parser.add_argument('--long-edge', default=None, type=int,
                        help='apply preprocessing to batch images')
    parser.add_argument('--loader-workers', default=2, type=int,
                        help='number of workers for data loading')
    parser.add_argument('--disable-cuda', action='store_true',
                        help='disable CUDA')
    parser.add_argument('--figure-width', default=10.0, type=float,
                        help='figure width')
    parser.add_argument('--dpi-factor', default=1.0, type=float,
                        help='increase dpi of output image by this factor')
    group = parser.add_argument_group('logging')
    group.add_argument('-q', '--quiet', default=False, action='store_true',
                       help='only show warning messages or above')
    group.add_argument('--debug', default=False, action='store_true',
                       help='print debug messages')
    args = parser.parse_args()

    log_level = logging.INFO
    if args.quiet:
        log_level = logging.WARNING
    if args.debug:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    # glob
    if args.glob:
        args.images += glob.glob(args.glob)
    if not args.images:
        raise Exception("no image files given")

    # add args.device
    args.device = torch.device('cpu')
    args.pin_memory = False
    if not args.disable_cuda and torch.cuda.is_available():
        args.device = torch.device('cuda')
        args.pin_memory = True

    return args


def bbox_from_keypoints(kps):
    m = kps[:, 2] > 0
    if not np.any(m):
        return [0, 0, 0, 0]

    x, y = np.min(kps[:, 0][m]), np.min(kps[:, 1][m])
    w, h = np.max(kps[:, 0][m]) - x, np.max(kps[:, 1][m]) - y
    return [x, y, w, h]


def read_bag(input_file):
    """Helpful example:
    https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/align-depth2color.py
    """
    import pyrealsense2 as rs

    print('====================')
    print(input_file)

    pipeline = rs.pipeline()

    config = rs.config()
    rs.config.enable_device_from_file(config, input_file)
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)
    profile = pipeline.start(config)
    d = profile.get_device().as_playback()
    for s in d.query_sensors():
        print(s.get_stream_profiles())
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print('Depth Scale is: ', depth_scale)

    align = rs.align(rs.stream.color)

    i = 0
    try:
        while True:
            # Get frameset of color and depth
            frames = pipeline.wait_for_frames()
            # frames.get_depth_frame() is a 640x360 depth image

            i += 1
            if i < 10:
                continue

            # Align the depth frame to color frame
            aligned_frames = align.process(frames)

            # Get aligned frames
            # aligned_depth_frame is a 640x480 depth image
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                break

            depth_image = np.asanyarray(aligned_depth_frame.get_data()).astype(np.float)
            depth_image[depth_image < 0.5 / depth_scale] = 0.5 / depth_scale
            depth_image[depth_image > 2.0 / depth_scale] = 0.5 / depth_scale
            print(np.min(depth_image), np.max(depth_image))
            color_image = np.asanyarray(color_frame.get_data())
            # yield color_image, depth_image
            with show.image_canvas(depth_image, show=True) as ax:
                pass

            yield PIL.Image.fromarray(color_image)

            break
    except KeyboardInterrupt:
        pass


def main():
    args = cli()

    # load model
    model, _ = nets.factory_from_args(args)
    model = model.to(args.device)
    processor = decoder.factory_from_args(args, model)

    # data
    preprocess = None
    if args.long_edge:
        preprocess = transforms.Compose([
            transforms.Normalize(),
            transforms.RescaleAbsolute(args.long_edge),
            transforms.CenterPad(args.long_edge),
        ])
    if len(args.images) == 1 and args.images[0].endswith('.bag'):
        data = datasets.PilImageList(list(read_bag(args.images[0])), preprocess=preprocess)
    else:
        data = datasets.ImageList(args.images, preprocess=preprocess)
    data_loader = torch.utils.data.DataLoader(
        data, batch_size=args.batch_size, shuffle=False,
        pin_memory=args.pin_memory, num_workers=args.loader_workers)

    # visualizers
    keypoint_painter = show.KeypointPainter(show_box=False)
    skeleton_painter = show.KeypointPainter(show_box=False, color_connections=True,
                                            markersize=1, linewidth=6)

    for image_i, (image_paths, image_tensors, processed_images_cpu) in enumerate(data_loader):
        images = image_tensors.permute(0, 2, 3, 1)

        processed_images = processed_images_cpu.to(args.device, non_blocking=True)
        fields_batch = processor.fields(processed_images)
        pred_batch = processor.annotations_batch(fields_batch, debug_images=processed_images_cpu)

        # unbatch
        for image_path, image, processed_image_cpu, pred in zip(
                image_paths,
                images,
                processed_images_cpu,
                pred_batch):

            if args.output_directory is None:
                output_path = image_path
            else:
                file_name = os.path.basename(image_path)
                output_path = os.path.join(args.output_directory, file_name)
            logging.info('image %d: %s to %s', image_i, image_path, output_path)

            processor.set_cpu_image(image, processed_image_cpu)
            keypoint_sets, scores = processor.keypoint_sets_from_annotations(pred)

            if 'json' in args.output_types:
                with open(output_path + '.pifpaf.json', 'w') as f:
                    json.dump([
                        {
                            'keypoints': np.around(kps, 1).reshape(-1).tolist(),
                            'bbox': bbox_from_keypoints(kps),
                        }
                        for kps in keypoint_sets
                    ], f)

            if 'keypoints' in args.output_types:
                with show.image_canvas(image,
                                       output_path + '.keypoints.png',
                                       show=args.show,
                                       fig_width=args.figure_width,
                                       dpi_factor=args.dpi_factor) as ax:
                    keypoint_painter.keypoints(ax, keypoint_sets)

            if 'skeleton' in args.output_types:
                with show.image_canvas(image,
                                       output_path + '.skeleton.png',
                                       show=args.show,
                                       fig_width=args.figure_width,
                                       dpi_factor=args.dpi_factor) as ax:
                    skeleton_painter.keypoints(ax, keypoint_sets, scores=scores)


if __name__ == '__main__':
    main()
