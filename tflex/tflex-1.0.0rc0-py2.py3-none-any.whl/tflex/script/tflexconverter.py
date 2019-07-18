# -*- coding: utf-8 -*-
import tflex
import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description='Convert source model(.pb,.h5,SavedModel) to target model(.tflex graph) supported on EPU.')
    parser.add_argument(
        '--keras_model', '-km',
        type=str,
        default='',
        help="Source model with .h5 file to be converted.")
    parser.add_argument(
        '--frozen_model', '-fm',
        type=str,
        default='',
        help="Source model with .pb file to be converted.")
    parser.add_argument(
        '--saved_model', '-sm',
        type=str,
        default='',
        help="Source SavedModel with .pb file and variables to be converted.")
    parser.add_argument(
        '--export_dir', '-ed',
        type=str,
        default='tflex/models/model.tflex',
        help="Directory to save the optimized graph(i.e.,model.tflex file will be saved here).")
    parser.add_argument(
        '--input_arrays', '-i',
        type=str,
        default='input',
        help="String of input node names. If your model has more inputs, please use tflexconverter -i input_1,input_2.")
    parser.add_argument(
        '--output_arrays', '-o',
        type=str,
        default='output',
        help="String of output node names. If your model has more outputs, please use tflexconverter -o output_1,output_2.")
    return parser


def main():
    parser = get_parser()
    flags = parser.parse_args()
    input_arrays = []
    output_arrays = []
    for name in flags.input_arrays.split(','):
        input_arrays.append(name)
    for name in flags.output_arrays.split(','):
        output_arrays.append(name)

    if flags.keras_model:
        converter = tflex.Converter.from_keras_model(flags.keras_model)
    elif flags.frozen_model:
        if input_arrays and output_arrays:
            converter = tflex.Converter.from_frozen_graph(flags.frozen_model, input_arrays, output_arrays)
        else:
            raise Exception(
                'input_arrays(input node names) and output_arrays(output node names) are required. Please use tflexconverter --help to view')
    elif flags.saved_model:
        converter = tflex.Converter.from_saved_model(flags.saved_model)
    else:
        raise Exception(
            'keras_model or frozen_model or saved_model are required. Please use tflexconverter --help to view.')

    converter.convert(flags.export_dir)


if __name__ == '__main__':
    main()
