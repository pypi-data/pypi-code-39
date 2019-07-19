# Copyright 2019 Cochlear.ai Ltd. All Rights Reserved.

import grpc

from cochl import SenseClient_pb2
from cochl import SenseClient_pb2_grpc

import pyaudio
from six.moves import queue

host_address = '34.80.243.56:50051'
list_of_tasks = ['event']
list_of_fileformats = ['mp3','wav','ogg','flac','mp4']

class TaskError(Exception) : 
    def __init__(self, message):
        self.msg = message
    def __str__(self):
        return self.msg

def checkTask_tasks(task) : 
	if not task in list_of_tasks:	
		raise TaskError('Wrong Task : {}'.format(task))

def checkTask_file_format(file_format) : 
	if not file_format in list_of_fileformats:	
		raise TaskError('Wrong File Format : {}'.format(file_format))

def sense(filename,apikey,file_format,task):

	checkTask_tasks(task=task)
	checkTask_file_format(file_format=file_format)
	host = host_address
	channel = grpc.insecure_channel(host)
	stub = SenseClient_pb2_grpc.SenseStub(channel)

	CHUNK = 1024*1024

	def get_file_chunks(filename):
		with open(filename,'rb') as f:
			while True:
				piece = f.read(CHUNK);
				if len(piece) == 0:
					return
				yield SenseClient_pb2.Request(data=piece,apikey=apikey,format=file_format,task=task)

	chunks_generator = get_file_chunks(filename)
	response = stub.sense(chunks_generator)

	return response
	

class SenseStreamer(object):
	def __init__(self,task):

		rate = 22050
		chunk = int(rate / 2)

		self._rate = rate
		self._chunk = chunk
		self._buff = queue.Queue()
		self.closed = True

	def __enter__(self):
		self._audio_interface = pyaudio.PyAudio()
		self._audio_stream = self._audio_interface.open(
			format=pyaudio.paFloat32,
			channels=1, rate=self._rate,
			input=True, frames_per_buffer=self._chunk,
			stream_callback=self._fill_buffer,
		)

		self.closed = False
		return self

	def __exit__(self, type, value, traceback):
		self._audio_stream.stop_stream()
		self._audio_stream.close()
		self.closed = True
		self._buff.put(None)
		self._audio_interface.terminate()

	def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
		self._buff.put(in_data)
		return None, pyaudio.paContinue

	def generator(self):
		while not self.closed:
			chunk = self._buff.get()
			if chunk is None:
				return
			data = [chunk]
			while True:
				try:
					chunk = self._buff.get(block=False)
					if chunk is None:
						return
					data.append(chunk)
				except queue.Empty:
					break
			yield b''.join(data)

def sense_stream_request(audio_generator,apikey,task):

	checkTask_tasks(task=task)
	host = host_address
	channel = grpc.insecure_channel(host)
	stub = SenseClient_pb2_grpc.SenseStub(channel)
	sr = 22050

	requests = (SenseClient_pb2.RequestStream(data=content,apikey=apikey,sr=sr,task=task,dtype='float32') 
														for content in audio_generator)
	return requests

def sense_stream_response(requests):

	host = host_address
	channel = grpc.insecure_channel(host)
	stub = SenseClient_pb2_grpc.SenseStub(channel)

	responses = stub.sense_stream(requests)
	return responses
