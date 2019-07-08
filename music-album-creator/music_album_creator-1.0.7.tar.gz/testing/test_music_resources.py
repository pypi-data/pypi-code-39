import os
import pytest

# from music_album_creation.durations_acquisition import DurationsHandler, TheAudioDB

api_key = '195003'
resources = ['the-audio-db']
album = 'gav'

args_in = [resources, ]


resources_data = {'the-audio-db': {'args': [api_key], 'kwargs': {}}}

# dh = DurationsHandler(resources_data)

# @pytest.fixture(scope='module')
# def the_audio_db():
#     return TheAudioDB('195003')
#
# @pytest.fixture(scope='module', params=['the-audio-db'])
# def request_to_resource():
#     return dh.query()
#
# class QueryResource:
#     def test_existing_album(self):
#
#     def non_existing_album(self):



# class TestYoutubeDownloader:
#     NON_EXISTANT_YOUTUBE_URL = 'https://www.youtube.com/watch?v=alpharegavgav'
#     duration = '3:43'
#     duration_in_seconds = 223
#
#     def test_downloading_false_url(self, youtube):
#         with pytest.raises(WrongYoutubeUrl):
#             youtube.download(self.NON_EXISTANT_YOUTUBE_URL, '/tmp/', spawn=False, verbose=False, supress_stdout=True)
#
#     @pytest.mark.parametrize("url, target_file", [('https://www.youtube.com/watch?v=Q3dvbM6Pias', 'Rage Against The Machine - Testify')])
#     def test_downloading_valid_url(self, url, target_file, youtube):
#         youtube.download(url, '/tmp', spawn=False, verbose=False, supress_stdout=True)
#         assert os.path.isfile('/tmp/'+target_file+'.mp3')