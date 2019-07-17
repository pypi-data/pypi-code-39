import subprocess
from tempfile import TemporaryDirectory
import os
import glob
from tqdm import tqdm
from datetime import datetime
import json
from shutil import copyfile
import csv

from tidkvideochange import detection_batch as detection
from tidkvideochange import recognition_batch as recognition

import importlib
importlib.reload(detection)

def infer_frames_with_batches(input_frames_path, batch_size=4):

    # Create a function called "chunks" with two arguments, l and n:
    def chunks(l, n):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            yield l[i:i+n]

    

    frame_files = sorted(glob.glob(input_frames_path + '/*.jpg'))

    num_frames = len(frame_files)
    detect_time = 0
    recognize_time = 0
    print('!!Detecting and recognizing text from {} frames: {}'.format(num_frames, str(datetime.now())))
    wordBB = None
    score = None
    text = None

    batches = list(chunks(frame_files, batch_size)) + [["\\-1-"]]
    print(batches)

    def getFileIdInBatch(num_batch, pos): # args: batch number, position in batch
        return int(batches[num_batch][pos].split("\\")[-1].split("-")[-2])

    next_batch = 0
    batch_results = dict()
    for index, filename in tqdm(enumerate(frame_files), total=num_frames):
        if(index+1 == getFileIdInBatch(next_batch, 0)):
            
            detectedOnImages = []
            wordBBs, scores = detection.detect(batches[next_batch])
            for i, wordBB, score in zip(range(len(batches[next_batch])), wordBBs[:len(batches[next_batch])], scores[:len(batches[next_batch])]):
                if score.shape[0] == 0:
                    batch_results[getFileIdInBatch(next_batch, i)] = {'wordBB': None, 'score': None, 'text': ""}
                else:
                    batch_results[getFileIdInBatch(next_batch, i)] = {'wordBB': wordBB, 'score': score.tolist(), 'text': ""}
                    detectedOnImages.append(i)
            if len(detectedOnImages) > 0:
                texts = recognition.recognize([batches[next_batch][i] for i in detectedOnImages], [wordBBs[i] for i in detectedOnImages])
                for i, text in zip(detectedOnImages, texts[:len(batches[next_batch])]):
                    batch_results[getFileIdInBatch(next_batch, i)]['text'] = text
            next_batch += 1
    
        for i in sorted(batch_results.keys()):
            if i >= index:
                wordBB = batch_results[i]['wordBB']
                try: 
                    text = batch_results[i]['text']
                except:
                    pass
                break

    return batch_results


def VideoChangeVideoText(path, threshold, output, pred):
    """Runs PySceneDetect on video and can feed the results into VideoText

    Processes an input video using PySceneDetect determining scences in that video. For every scene the middle frame is selected. 
    These frames can then be saved, and text detection/recognition can be run on them using modified VideoText that operates on batches on data.

    Parameters:
        path (str): The file location of the video
        threshold (int): The threshold value for PySceneDetect. Values between 0 and 100 are supported, with values closer to 0 causing more scenes to be produced
        output (str): The output folder location for detected scenes to be saved into
        pred (bool): A flag used to determine whether to run prediction on detected frames

    Returns:
        dict: A dict containing prediction results, or empty if prediction was not run
    """

    with TemporaryDirectory() as temp_dir:
        output_frames_path = os.path.join(temp_dir,"out_frames")
        subprocess.run(["scenedetect", "--input", path, "--output", output_frames_path, "--stats", "{}.stats.csv".format(output), "detect-content", "-t", str(threshold), "save-images", "-n", "1", "list-scenes", "-f", "{}.scenes.csv".format(output)])
        
        # Copying detected frames to the directory specified. Will not override contents of a directory if one exists aready.
        if output is not None:
            if not os.path.exists(output):
                os.makedirs(output)
                for f in [ff for ff in os.listdir(output_frames_path) if ff.endswith(".jpg")]:
                    copyfile(os.path.join(output_frames_path,f), os.path.join(output,f))
            else:
                print("{} folder already exists. No files were copied!".format(output))

            # Infering on detected frames.
            if pred:
                # Loading models required for prediction.
                recognition.prepare_model()
                detection.prepare_model()

                # Run prediction and return the results.
                results = infer_frames_with_batches(output_frames_path)
                print(results.keys())
                # Add information on timestamp of the frame w.r.t. original video
                with open(os.path.join(output_frames_path, "{}.scenes.csv".format(output))) as csv_file:
                    line_count = 0
                    for line in csv_file:
                        if line_count > 1:
                            lines_splitter = line.split(",")
                            idx = int(lines_splitter[0])
                            s = float(lines_splitter[3])
                            e = float(lines_splitter[6])
                            results[idx]['timestamp'] = (s+e)/2
                        line_count += 1

                return results


        # If no prediction was issued an empty dict is returned.
        return dict()


#Example usage
#res = VideoChangeVideoText("test\\AllMajorMovieStudiosLogosinHd.mp4", 10, "res_res", 1)
#print(json.dumps(res, indent=4))

#with open('out.json', 'w') as outfile:
#    json.dump(res, outfile)
