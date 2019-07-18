import boto3

class SQS(object):
    def __init__(self, queuename):
        self.sqs = boto3.resource('sqs')
        self.queuename = queuename
        self.queue = None

        
    def get_queue(self):
        if(self.queue is not None):
            return self.queue
        self.queue = self.queue = self.sqs.create_queue(
            QueueName=self.queuename
        )
        return self.queue


    def make_message(self, body, id, attributes = None):
        body = {"MessageBody" : body,
                "Id": id
        }
        if(attributes is not None):
            body['attributes'] = attributes
        return body

    
    def send_message(self, body, attributes=None):
        queue = self.get_queue()
        msg = self.make_message(body, attributes)
        del(msg['Id'])
        return queue.send_message(**msg)

    
    def send_messages(self, msgs):
        self.get_queue().send_messages(Entries = msgs)

        
    def receive_message(self, wait_time_seconds = 20,
                        visibility_timeout = 120):
        return self.get_queue().receive_messages(
            WaitTimeSeconds=20,
            VisibilityTimeout=120,
            MaxNumberOfMessages=10
        )

    
    def delete_queue(self):
        val = self.get_queue().delete()
        if(val['HTTPStatusCode']==200):
            return True
        else:
            return val
        
