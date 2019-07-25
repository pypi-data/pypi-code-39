import site
import importlib
import glob

class Engine:
    def __init__(self):
        self._model_ = {}
        self._extension_ = self.extension_update()

    def _import_extension_(self, identifier="deepgeo_ext"):
        paths = site.getsitepackages()
        Extension = {}
        for path in paths:
            path = path.replace("\\\\","/")
            folder_list = glob.glob(path+"/"+ identifier +"_*")
            for folder in folder_list:
                moduleName = folder.replace("\\","/").split("/")[-1]
                if ".dist-info" in moduleName:
                    continue
                try:
                    Ext = importlib.import_module(moduleName)
                    title = moduleName.replace(identifier+"_","")
                    Extension.update({title:Ext})
                except Exception as e:
                    print(e)
        return Extension

    def _get_model_(self, name):
        assert name is not None, "Engine -> NAME 값이 NULL 입니다."
        assert name != "", "Engine -> NAME 값이 비어있습니다."
        assert name in list(self._model_.keys()), "Engine -> 존재하지 않은 Model 이름입니다."

        return self._model_[name]

    def _get_class_(self, _name, _type):
        _name = _name.lower()
        _type = _type.lower()
        if _name in self._extension_:
            if _type == "model":
                return self._extension_[_name].Model
            elif _type == "dataset":
                return self._extension_[_name].Dataset
            elif _type == "config":
                return self._extension_[_name].Config
        return None

    def extension_update(self):
        return self._import_extension_()

    def get_model_list(self):
        return list(self._model_.keys())

    def add_model(self, model_name, lib_name, config_data):
        config = self._get_class_(lib_name, "config")()

        assert config is not None, "해당 라이브러리가 존재하지 않습니다."
        
        config.load_config(config_data)
        model = self._get_class_(lib_name, "model")(config)

        assert model is not None, "해당 라이브러리가 존재하지 않습니다."

        self._model_.update({model_name:model})        
    
    def set_config(self,model_name, data:dict):
        model = self._get_model_(model_name)
        for key in list(data.keys()):
            model.get_config().set_config(key,data[key])

    def get_config(self, model_name, key):
        model = self._get_model_(model_name)
        return model.get_config().get_value(key)

    def delete_model(self, name):
        if name in list(self._model_.keys()):
            del self._model_[name]
        else:
            print("해당 모델이름을 가진 모델이 존재하지 않습니다.")
        
    def add_dataset(self, model_name, dataset_name, lib_name):
        model = self._get_model_(model_name)
        dataset = self._get_class_(lib_name,"dataset")()
        dataset.set_config(model.get_config())
        model.add_dataset(dataset_name, dataset)

    def delete_dataset(self, model_name, dataset_name):
        model =self._get_model_(model_name)
        model.delete_dataset(dataset_name)

    def add_data(self, model_name, dataset_name, data):
        model = self._get_model_(model_name)
        model.add_data(dataset_name, data)

    def train(self, name, train_dataset_name, validation_dataset_name, weight):
        model = self._get_model_(name)
        if model.get_dataset(train_dataset_name) is None or model.get_dataset(validation_dataset_name) is None:
            return None
        model.train(train_dataset_name, validation_dataset_name, weight)
        return model.get_config()
    
    def detect(self, name, row_data, option=1):
        result= []
        model = self._get_model_(name)
        if not isinstance(row_data,list):
            row_data = [row_data]
        for data in row_data:
            result.append(model.detect(data,option))
        return result
