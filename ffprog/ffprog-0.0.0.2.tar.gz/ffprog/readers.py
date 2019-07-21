import json
import os
import re
import subprocess as sp
import sys
from datetime import datetime
from os.path import basename, splitext
from tempfile import mkstemp
from time import sleep

from ffprog.exceptions import FFmpegError, FFprogError


class FFmpegProgressInfo:
    def __init__(self, command):
        self.command = command
        self.ffmpeg_process = None

    # TODO improve validation
    def validate_ffmpeg_command(self):
        command = self.command

        if not isinstance(command, list):
            raise FFmpegError("Command should be list with strings. For example ['ffmpeg', '-y'].")

        elif len(command) == 0 or 'ffmpeg' not in command or command[0] != 'ffmpeg':
            raise FFmpegError('Wrong command.')

        return command

    def on_message(self, percent, fr_cnt, total_frames, elapsed, left):
        bar = list('|' + (20 * ' ') + '|')
        total_percent = int(percent / 5) or 1
        to_fill = total_percent if total_percent < 100 else 20

        for x in range(1, to_fill):
            bar[x] = '░'
        bar[to_fill] = '░'
        bar = ''.join(bar)

        sys.stdout.write(
            f'\r{bar} {percent}% {fr_cnt} / {total_frames} frames; '
            f'elapsed time: {elapsed} seconds; '
            f'left time: {left} seconds;'
        )
        sys.stdout.flush()

    def on_done(self, infile, outfile):
        sys.stdout.write(
            f'\ninfile: {self.ffprobe(infile)};'
            f'\noutfile: {self.ffprobe(outfile)};'
        )
        sys.stdout.flush()

    @staticmethod
    def calculate_percent(fr_cnt, total_frames):
        real_percent = (fr_cnt / total_frames) * 100
        return round(real_percent, 2) if real_percent <= 100 else 100

    @staticmethod
    def calculate_elapsed_time(start):
        return round((datetime.now() - start).total_seconds(), 2)

    @staticmethod
    def calculate_left_time(elapsed, percent):
        try:
            left = elapsed * ((100 - percent) / percent)
        except ZeroDivisionError:
            left = 0
        return round(left, 2)

    def display_progress(self, total_frames, vstats_handle, wait_time, countdown_time):
        start = datetime.now()
        fr_cnt = left = elapsed = percent = 0

        while self.ffmpeg_process.poll() is None:
            sleep(wait_time)

            vstats_handle.seek(-2, os.SEEK_END)
            while vstats_handle.read(1) != b'\n':
                vstats_handle.seek(-2, os.SEEK_CUR)
            last = vstats_handle.readline().decode('utf-8').strip()

            try:
                vstats = int(re.sub(r'\s+', ' ', last).split(' ')[1])
            except IndexError:
                vstats = 0

            if vstats > fr_cnt:
                fr_cnt = vstats
                percent = self.calculate_percent(fr_cnt, total_frames)
                elapsed = self.calculate_elapsed_time(start)
                left = self.calculate_left_time(elapsed, percent)

            self.on_message(percent, fr_cnt, total_frames, elapsed, left)

        sleep(countdown_time)

    @staticmethod
    def ffprobe(file):
        proc = sp.run(['ffprobe',
                       '-v', 'quiet',
                       '-print_format', 'json',
                       '-show_format',
                       '-show_streams',
                       file], encoding='utf-8', stdout=sp.PIPE)
        return json.loads(proc.stdout)

    @staticmethod
    def get_infile(validated_command):
        index = validated_command.index('-i')
        try:
            infile_path = validated_command[index + 1]
        except IndexError:
            raise FFprogError('Sorry, infile path does not exist.')
        return infile_path

    @staticmethod
    def get_outfile(validated_command):
        try:
            outfile_path = validated_command[-1]
        except IndexError:
            raise FFprogError('Sorry, outfile path does not exist.')
        return outfile_path

    def ffmpeg_callback(self, validated_command, vstats_path):
        final_command = [validated_command[0]] + ['-vstats_file', vstats_path] + validated_command[1:]
        self.ffmpeg_process = sp.Popen(final_command, stdout=sp.PIPE, stderr=sp.PIPE)
        return self.ffmpeg_process

    @staticmethod
    def calculate_total_frames(probe, index):
        try:
            probe['streams'][index]
        except (IndexError, KeyError):
            raise FFprogError('Probe failed.')

        try:
            fps = eval(probe['streams'][index]['avg_frame_rate'])
        except ZeroDivisionError:
            raise FFprogError('Cannot use input FPS.')

        if fps == 0:
            raise FFprogError('Unexpected zero FPS.')

        dur = float(probe['format']['duration'])
        total_frames = int(dur * fps)

        if total_frames <= 0:
            raise FFprogError('Unexpected total frames value')

        return total_frames

    def progress_info_run(self, start_timeout=2, wait_time=2, countdown_time=5):
        index = 0
        validated_command = self.validate_ffmpeg_command()
        infile = self.get_infile(validated_command)
        outfile = self.get_outfile(validated_command)
        probe = self.ffprobe(infile)
        total_frames = self.calculate_total_frames(probe, index)
        prefix = 'ffprog-{}'.format(splitext(basename(infile))[0])

        # Take status file descriptor and file path
        vstats_fd, vstats_path = mkstemp(suffix='.vstats', prefix=prefix)

        self.ffmpeg_callback(validated_command, vstats_path)
        sleep(start_timeout)

        with open(vstats_fd, 'rb') as f:
            self.display_progress(total_frames, f, wait_time, countdown_time)

        if self.on_done:
            self.on_done(infile, outfile)


class FlvToMp4ProgressInfo(FFmpegProgressInfo):

    def calculate_total_frames(self, probe, index):
        parent_total_frames = super().calculate_total_frames(probe, index)
        return int(parent_total_frames / 2)
