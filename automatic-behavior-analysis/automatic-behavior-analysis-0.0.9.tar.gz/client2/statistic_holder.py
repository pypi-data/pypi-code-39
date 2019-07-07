import datetime
import pandas as pd
import numpy as np
import os
import copy

def frame2time(start_time, frame_number, fps):
    p_ms = int(1000 / fps) * frame_number
    return start_time + pd.Timedelta(np.timedelta64(p_ms, 'ms'))

def filename2time(filename):
    """
    03_20171108201654.mp4
    """
    filename = os.path.basename(filename)
    filename = os.path.basename(filename).split('.')[0][3:]
    return pd.Timestamp(filename)

class FrameAnnotation:
    def __init__(self):
        self.frame_index = -1 # Номер кадра
        self.objects = {} # Ключ -- id


class StatisticHolder():
    """
    Класс, отвечающий за хранение и обработку аннотации к видео
    """
    def __init__(self, file_name, fps):
        """
        Имя файла в формате даты-время
        """
        self.annotation_buffer = {}
        self.file_name = file_name
        self.fps = fps
        self.video_time = filename2time(file_name)

    def add_frame_annotation(self, annotation):
        """
        Добавить аннотацию кадра в буфер

        {
            'dogs': [
                {
                    'y2': 0.3626135289669037,
                    'category': 'dog',
                    'x2': 0.3295483887195587,
                    'y1': 0.07861500978469849,
                    'state': 'awake',
                    'id': 0,
                    'children': None,
                    'rate': 0.9999867677688599,
                    'x1': 0.15095321834087372
                },
                {
                    'y2': 0.4441756308078766,
                    'category': 'dog',
                    'x2': 0.3256682753562927,
                    'y1': 0.10957882553339005,
                    'state': 'awake',
                    'id': 1,
                    'children': None,
                    'rate': 0.9537808895111084,
                    'x1': 0.12371381372213364
                },
                {
                    'y2': 0.5296827554702759,
                    'category': 'dog',
                    'x2': 0.30304935574531555,
                    'y1': 0.201608344912529,
                    'state': 'awake',
                    'id': 2,
                    'children': None,
                    'rate': 0.9105631113052368,
                    'x1': 0.11796851456165314
                }
            ],
            'frame_index': 6,
            'status': 'ok',
            'event': 'load_image'
        }
        """
        fa = FrameAnnotation()
        annotation = copy.deepcopy(annotation)

        fa.frame_index = annotation['frame_index']
        for o in annotation['dogs']:
            fa.objects[o['id']] = copy.deepcopy(o)
        self.annotation_buffer[fa.frame_index] = fa

        # Наследуем значения из предыдущего фрейма
        # TODO: скорректировать на случай пропуска фреймов
        try:
            for k in self.annotation_buffer[annotation['frame_index']].objects.keys():
                if k in self.annotation_buffer[annotation['frame_index'] - 1].objects.keys():
                    src = self.annotation_buffer[int(annotation['frame_index']) - 1].objects[k]['name']
                    self.annotation_buffer[annotation['frame_index']].objects[k]['name'] = src
        except:
            pass

    def set_object_name(self, n_frame, id, name):
        """
        Установить имя для объекта. Автоматически имя распространяется
        на соседние фреймы
        """
        self.annotation_buffer[n_frame].objects[id]['name'] = name
        # Распространение имени в соседние кадры
        p_frame = n_frame
        try:
            while id in self.annotation_buffer[p_frame].objects.keys():
                self.annotation_buffer[p_frame].objects[id]['name'] = name
                p_frame -= 1
        except:
            pass #Дошли до начала файла

        p_frame = n_frame + 1
        try:
            while id in self.annotation_buffer[p_frame].objects.keys():
                self.annotation_buffer[p_frame].objects[id]['name'] = name
                p_frame += 1
        except:
            pass #Дошли до конца файла

    
    def get_object_name(self, n_frame, id):
        try:
            name = self.annotation_buffer[n_frame].objects[id]['name']
        except KeyError:
            name = ""
        return name
        
    def get_unnamed_objects_position(self):
        """
        Возвращает список кадров (номеров) с объектами без имен
        """
        frame_list = []
        for annot in self.annotation_buffer.values():
            try:
                for obj in annot.objects.values():
                    obj['name']
            except:
                frame_list.append(annot.frame_index)
        return frame_list

    def get_all_names(self):
        """
        Возвращает все имена, присвоенные объектам
        """
        name_list = []
        for key, annot in self.annotation_buffer.items():
            for n_obj, obj in annot.objects.items():
                try:
                    if obj['name'] not in name_list:
                        name_list.append(obj['name'])
                except:
                    pass
        return name_list

    def get_history_by_object_name(self, name):
        if name not in self.get_all_names():
            return None

        columns = ['DateTime', 
                    'y1',
                    'y2', 
                    'x1', 
                    'x2', 
                    'state', 
                    'rate', 
                    'moving_rate']
        history = pd.DataFrame(columns = columns)
        for annot in self.annotation_buffer.values():
            for obj in annot.objects.values():
                try:
                    if obj['name'] == name:
                        d = {
                            'DateTime' : frame2time(self.video_time, annot.frame_index, self.fps),
                             'y1' : obj['y1'],
                             'y2' : obj['y2'],
                             'x1' : obj['x1'],
                             'x2' : obj['x2'],
                             'state' : obj['state'],
                             'rate' : obj['rate'],
                             'moving_rate' : obj['moving_rate']}
                        data = pd.DataFrame(d, columns = columns, index=[annot.frame_index])
                        history = history.append(data)
                except Exception as e:
                    print(e)
        return history


    def save_all_history(self):
        """
        Сохраняет на диск в отдельные файлы все истории объектов
        в файлы с именем формата: <имя объекта>_<имя видео>.csv
        """
        for name in self.get_all_names():
            history = self.get_history_by_object_name(name)
            p = os.path.dirname(self.file_name)
            filename = os.path.basename(self.file_name).split('.')[0]
            fp = os.path.join(p, name + '_' + filename + ".csv")
            history.to_csv(fp)
