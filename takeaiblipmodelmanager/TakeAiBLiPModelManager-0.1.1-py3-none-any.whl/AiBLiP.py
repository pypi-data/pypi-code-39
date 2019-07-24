import json
import datetime
import requests
import numpy as np
import pandas as pd
from time import sleep
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score


class AiBLiP(object):
    """
    A class to automate the intents creation, examples addition, model training, publishin and 
    analysis in the BLiP platform.
    """

    def __init__(self, bot_key:str, blip_url:str, file_path:str, log_file_path:str,
                 file_name:str, intent_column, sentence_column, sep:str=';', encoding:str='utf-8'):
        """
        Parameters
        ----------
        bot_key : str
            chatbot authorization key.
        file_path : str
            the path in your OS.
        log_file_path : str
            path to save the log file in your OS.      
        file_name : str
            the name of you knowledge base file - should be used a csv file in this version.
        intent_column : int
            column containing the intents in your knowledge base.
        sentence_column : int
            column containing the examples in your knowledge base.
        sep : str
            file column separator - by default is setted as ;
        encoding : str
            file unicode - by default is setted as utf-8.
        """
        self.key = bot_key
        self.blip_url = blip_url
        self.file_path = file_path
        self.log_file_path = log_file_path
        self.file_name = file_name
        self.intent_column = intent_column
        self.sentence_column = sentence_column
        self.sep = sep
        self.encoding = encoding
        self.__read_knowledge_base()
        self.header = self.__create_request_header()

    def __create_request_header(self):
        """
        Generates the http request header using bot key.
        """

        header = {
            'Content-Type':'application/json',
            'Authorization' :'key ' + self.key
            }
        
        return header

    def __generate_body(self, request_id:str, method:str, uri:str, command_type:str):
        """
        Generates a generic http request body.
        
        Parameters
        ----------
        request_id : str
            Id used to identify the request.
        method : str
            Method used in request. It could be get, post and set.
        uri : str
            Request send a command to uri.
        command_type : str
            Type of command done in BLiP. For more details, see BLiP documentation.
        
        Returns
        -------
        body
            A dict to be used as a generic body in request.   
        """

        body = {
            'id':request_id,
            'to':'postmaster@ai.msging.net',
            'method':method,
            'uri':'/' + uri,
            'type':'application/' + command_type
        }
       
        return body

    

    def __read_knowledge_base(self):
        """
        Read the bot konwledge base from an especific file.
        """

        if type(self.intent_column) == type(self.sentence_column) == str:
            data = pd.read_csv(self.file_path + self.file_name, encoding = self.encoding, sep = self.sep)
            self.knowledge_base = data[[self.sentence_column, self.intent_column]]
        
        elif type(self.intent_column) == type(self.sentence_column) == int:
            data = pd.read_csv(self.file_path + self.file_name, encoding = self.encoding, sep = self.sep)
            sentence = data.iloc[:,self.sentence_column]
            intent = data.iloc[:,self.intent_column]
            self.knowledge_base = pd.DataFrame(data = [sentence, intent])
        
        else:
            print('Error while reading knowledge base!')

    def __get_code(self):
        """
        Creates a code to be used in log file. It's a concatenation of year, month, day, hour, minute and second.

        Returns
        -------
        code
            A string with the concateneted code.
        """

        now = datetime.datetime.now()
        code = str(now.year) + str(now.month) + str(now.day) + \
            str(now.hour) + str(now.minute)+ str(now.second)
        return code

    def __save_log_file(self, file:pd.DataFrame):
        """
        Save the analysis result in a log file.

        Parameters
        ----------
        file : pd.DataFrame
            A DataFrame file with the analysis request result from BLiP.
        """

        full_path = self.log_file_path + '/' + 'log_' + self.__get_code() + '.csv'
        file.to_csv(full_path, sep = self.sep, encoding = self.encoding, index = False)

    def delete_all_intents(self):
        """
        Delete all model intents.
        """
        
        body = self.__generate_body(0, 'get', 'intentions', '')
        del body['type']

        r = requests.post(self.blip_url, json.dumps(body), headers=self.header)
        
        try:
            print('Deleting all model intents...')
            intents = [intent['id'] for intent in r.json()['resource']['items']]
            
            for counter, intent in enumerate(intents): 
                body = self.__generate_body(0,'delete', 'intentions/'+ intent, '')
                del body['type']
                
                r = requests.post(self.blip_url, json.dumps(body), headers=self.header)

            print('All intents were deleted!')
        except:
            print('There is no intent to delete!')

    def create_intents(self, delete_existed_intents:bool=True):
        """
        Create intents in model inside BLiP.
        
        Parameters
        ----------
        delete_existed_intents : bool, optional
            Defines if all the existed intents in a model will be deleted.
        """

        if delete_existed_intents == True:
            self.delete_all_intents()
        
        for counter, intent in enumerate(self.knowledge_base['Intent'].unique()):
            print('Creating intent =', intent)
            body = self.__generate_body(counter, 'set', 'intentions', 'vnd.iris.ai.intention+json')
        
            resource = {
                'name': intent
            }
            body['resource'] = resource

            r = requests.post(self.blip_url, json.dumps(body), headers=self.header)

    def add_intent_examples(self):
        """
        Add examples in existed intents. In order to respect the throwput, the function sleep is used.
        """
        for counter, intent in enumerate(self.knowledge_base['Intent'].unique()):
            print('\nIntent = ', intent)
            
            items = [{'text': example} for example in self.knowledge_base[self.knowledge_base['Intent'] == intent]['Sentence']]

            body = self.__generate_body(counter, 'set', 'intentions/' + intent + '/questions','vnd.lime.collection+json')
            resource = {
                'itemType':'application/vnd.iris.ai.question+json',
                'items': items
            }
            body['resource'] = resource
            r = requests.post(self.blip_url, json.dumps(body), headers=self.header)
            print('Examples Added...')
            sleep(2)

    def train_model(self):
        """
        Train the current model in BLiP.
        """
        print('\nTraining the current model...')
        request_id = 0

        body = self.__generate_body(request_id, 'set', 'models',
                                 'application/vnd.iris.ai.model-training+json')
        resource = dict()
        body['resource'] = resource

        r = requests.post(self.blip_url, json.dumps(body), headers=self.header)
        print('Finished...')
            
    def publish_model(self, publish_model_request_id:str=0):
        """
        Publish the current in model in BLiP.
        """

        print('\nPublishing the current model...')
        body = self.__generate_body('0', 'get', 'models', '')
        del body['type']
        
        r = requests.post(self.blip_url, json.dumps(body), headers=self.header)
        models = r.json()['resource']['items']

        if len(models) > 0:
            current_model = models[0]['id']
            body = self.__generate_body(publish_model_request_id, 'set', 'models',
                                 'vnd.iris.ai.model-publishing+json')
            body['resource'] = {
                'id':current_model
            }
            
            r = requests.post(self.blip_url, json.dumps(body), headers=self.header)
            print(r.json())
            response_status = r.json()['status']
            
            if response_status == 'success':
                print('Model published succefully...')
            elif response_status == 'failure':
                print('Error while publishing the model...')
        else:
            print('There is no model to publish!!!')
        
    def analyse_model(self, test_file_path:str, model_id:str = ''):
        """
        Analyse and calculate evaluation metrics from a model. If parameter model_id is '',
         the current model will be used to analysis.

        Parameters
        ----------
        test_file_path : str
            File path with test file to be used to test the model.
        model_id : str, optional
            Model name in platform.
        """
        
        if model_id == '':
            test_file = pd.read_csv(test_file_path, encoding=self.encoding, sep=self.sep)
            test_file['HttpResult'] = test_file['Sentence'].apply(self.analyse_sentence(0))
            test_file['Predicted'] = test_file['HttpResult'].apply(lambda r: r['name'])
            test_file['Score'] = test_file['HttpResult'].apply(lambda r: float(r['score'])) # fazer casting astype.float -> validar função

            log_file = test_file[['Sentence','Intent','Predicted','Score']]
            self.__save_log_file(log_file)

            y_pred = test_file['Predicted'].values
            y_true = test_file['Intent'].values

            cm = confusion_matrix(y_true, y_pred)
            
            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='macro')
            recall = recall_score(y_true, y_pred, average='macro')
            f1 = f1_score(y_true, y_pred, average='macro')
            mean_confidence = test_file['Score'].mean()
            
            print('\nMODEL METRICS')
            print('Accuracy', accuracy)
            print('Precision', precision)
            print('Recall', recall)
            print('F1-Score', f1)
            print('Mean Confidence', mean_confidence)

        else:
            print('Analyse of selected model is not implemented...')
        

    def analyse_sentence(self, analyse_sentence_request_id:str, message:str):
        """
        Analyse one sentence in the current published model.
        
        Parameters
        ----------
        analyse_sentence_request_id : str
            Id model used in BLiP.
        message : str
            Sentence to be analysed.

        Returns
        -------
        intent
            A dict with the informations of the message analysed.
        """

        body = self.__generate_body(analyse_sentence_request_id, 'set', 'analysis',
                                 'vnd.iris.ai.analysis-request+json')

        body['resource'] = {
                'text': message
                }
        
        r = requests.post(self.blip_url, json.dumps(body), headers=self.header)
        intentions = r.json()['resource']['intentions']
        
        if len(intentions) > 0:
            model_intent = intentions[0]
            print('Classified =', model_intent['name'])
            return intentions[0]
        else:
            print('Error while analysing the sentence...')
            return dict()

     