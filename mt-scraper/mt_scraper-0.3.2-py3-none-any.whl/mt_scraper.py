import traceback
import threading
import argparse
import os.path
import random
from urllib.request import urlopen, Request
#from urllib.parse import urljoin
from urllib.error import HTTPError, URLError
from datetime import date, datetime
from time import sleep
from json import dump, load
from queue import Queue
from sys import stdout, stderr, exit
import enum

from .dummy_parser import MyDummyHTMLParser

__version__ = '0.3.2'

class ListWithoutDublicates:
    def __init__(self, l=[]):
        self.__obj = {}
        for o in l:
            self.append(o)

    def append(self, obj):
        self.__obj[obj['id']] = obj

    def get_list(self, sorted=True):
        keys_list = [k for k in self.__obj.keys()]

        if sorted:
            keys_list.sort()

        l = [self.__obj[k] for k in keys_list ]

        return l


def default_json(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()

def get_obj_from_file(filename):
        with open(filename) as infile:
            o = load(infile)
        return o

def get_html_from_file(filename):
    with open(filename) as infile:
        html = infile.read()
    return html



class Command():
    pass


class ExitCommand(Command):
    '''СИгнал для выхода потоку-потребителю'''
    pass


class GetCommand(Command):
    def __init__(self, num, obj):
        self.__num = num
        self.__obj = obj

    @property
    def num(self):
        return self.__num

    @property
    def obj(self):
        return self.__obj

    def __str__(self):
        return 'CMD: Get num:{}'.format(self.num)


class Scraper:
    '''Scrapper base class'''
    description = 'Scrapper for http://example.com/'
    filedir = None
    out_filename = 'out.json'
    threads_num = 5
    queue_len = 5
    url_template = '{}'
    url_components_list = [
        'http://example.com/',
        'http://scraper.iamengineer.ru',
        'http://scraper.iamengineer.ru/bad-file.php',
        'http://badlink-for-scarper.ru',
    ]

    #worker_outstring = '{thread_name:10}ID:{num:7}\t{success} {additional_info}'
    worker_outstring = '{thread_name:10}ID:{num:7}\t{success}'

    headers={
        'User-Agent': 'Python Scraper V{}'.format(__version__)
    }
    use_proxy = False

    def parse(self, num, url_component, html):
        '''Необходимо переопределить этот метод
        Должен возвращять словарь или None, если парсинг странички
        невозможен 
        '''
        parser = MyDummyHTMLParser()
        parser.feed(html)
        obj = parser.obj
        obj['url_component'] = url_component
        return parser.obj

    def get_url(self, obj):
        '''Необходимо переопределить этот метод
        если вам нужно особое формирование URL 
        '''
        return self.url_template.format(obj) 

    def get_url_component_list(self):
        '''Необходимо переопределить этот метод
        если вам нужно особое формирование списка
        компонентов URL, например получить его из файла
        из коммандной строки 
        '''
        return self.url_components_list

    def add_arguments(self, parser):
        '''Необходимо переопределить этот метод
        если вам нужно добавить собственные аргументы
        коммандной строки, например особой загрузки списка
        компонентов URL или для формирования
        '''
        pass

    @enum.unique
    class ExitStatus(enum.Enum):
        FILE_NOT_FOUND_ERR = 1000

    def __init__(self):
        self.obj_list = []
        self.proxies = []

        self.queue = Queue(maxsize=self.queue_len)

        self.obj_list_mutex = threading.Lock()
        self.stdout_mutex = threading.Lock()
        if self.filedir is None:
            self.filedir = os.path.dirname(os.path.abspath(__file__))


    # def load_proxy(self, filename):
    #     proxies = []
    #     with open(filename) as infile:
    #         lines = infile.readlines()

    #     for line in lines:
    #         proxies.append(line.strip())

    #     return proxies


    def __get_url_component_list(self):
        if self.args.url_components_file is not None:
            return get_obj_from_file(self.args.url_components_file)
        elif self.args.url_components_list is not None:
            return self.args.url_components_list
        return self.url_components_list

    def get_html(self, url):
        #proxies = {'HTTP': random.choice(proxies)}

        req = Request(url=url, method='GET', headers=self.headers)
        # if use_proxy:
        #     req.set_proxy(random.choice(proxies), 'HTTP')
        f = urlopen(req)
        list_html = f.read().decode('utf-8', errors='ignore')

        return list_html

    def worker(self):
        '''This is worker thread. It gets html and execute parsing function.
        Exit then recive object of ExitCommand class'''
        thread_name = threading.currentThread().getName()

        if not self.args.machine_out:
            with self.stdout_mutex:
                print('Worker started', thread_name)

        out_string_data = {'thread_name':thread_name}

        while True:
            command =  self.queue.get()
            #print('GET COMMAND', command)
            if not isinstance(command, Command):
                raise ValueError('Unknown command')

            if isinstance(command, ExitCommand):
                break

            num = command.num
            out_string_data['num'] = num
            obj = command.obj
            url = self.get_url(obj)
            try:
                if self.args.html_file is None:
                    html = self.get_html(url)
                else:
                    html = get_html_from_file(self.args.html_file)

                obj_out = self.parse(num, obj, html)
                obj_out['id'] = str(obj)
                with self.obj_list_mutex:
                    self.obj_list.append(obj_out)

                out_string_data['success'] = 'OK'
                #out_string_data['additional_info'] = ''


            except HTTPError as e:
                out_string_data['success'] = str(e) 
                #out_string_data['additional_info'] = str(e)

            except URLError as e:
                out_string_data['success'] = 'URL Error: {}'.format(e.reason) 
                #out_string_data['additional_info'] = str(e)

            except FileNotFoundError as e:
                out_string_data['success'] = str(e)

            except Exception as e:
                out_string_data['success'] = str(e) 
                #out_string_data['additional_info'] = str(e)

                with self.stdout_mutex:
                    traceback.print_exc(file=stderr)

            with self.stdout_mutex:
                print(self.worker_outstring.format(**out_string_data))


        if not self.args.machine_out:
            with self.stdout_mutex:
                print('Worker STOPPED', thread_name)


    def __add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file-name', 
            default=self.out_filename, 
            help="Filename for input and output data. '\
            'May be stdout for console output"
        )
        parser.add_argument(
            '-t',
            '--threads',
            type=int,
            default=self.threads_num, 
            help="Number of threads"
        )
        parser.add_argument(
            '-q',
            '--queue-len', 
            default=self.queue_len, 
            help="Length of queue for requests"
        )
        # parser.add_argument(
        #     '-p',
        #     '--use-proxy',
        #     const=use_proxy,
        #     default=not use_proxy,
        #     action='store_const',
        #     help="Please use proxy servers from list"
        # )
        parser.add_argument(
            '-m', 
            '--machine-out', 
            action='store_true',
            help='Prohibit the printing of unnecessary information in std. '\
            'This flag is used to output information to standard output '\
            'instead of a file.'
        )
        parser.add_argument(
            '-u', 
            '--url-components-file', 
            default=None,
            help='Filename to load url_component_list'
        )
        parser.add_argument(
            '-l', 
            '--url-components-list', 
            nargs='*',
            default=None,
            help='Filename to load url_component_list'
        )
        parser.add_argument(
            #'-i',
            '--html-file', 
            default=None, 
            help="Filename for input html data if you want to work without "\
            "internet connection"
        )

        self.add_arguments(parser)

    def __parse_args(self, cmd_args):
        parser = argparse.ArgumentParser(description=self.description)
        self.__add_arguments(parser)
        self.args = parser.parse_args(args=cmd_args)

    def run(self, cmd_args=None):
        self.__parse_args(cmd_args=cmd_args)
        # proxies = load_proxy(os.path.join(filedir, 'proxy.txt'))
        #print(proxies)
        #print(args)
        #raise KeyboardInterrupt

        out_filename = self.args.file_name
        threads_num = self.args.threads
        queue_len = self.args.queue_len
        # use_proxy = args.use_proxy

        try:
            self.obj_list = ListWithoutDublicates(get_obj_from_file(out_filename))
        except FileNotFoundError:
            self.obj_list = ListWithoutDublicates()
        try:
            url_components_list = self.__get_url_component_list()
        except FileNotFoundError as e:
            print("Error {}".format(e), file=stderr)
            exit(self.ExitStatus.FILE_NOT_FOUND_ERR)

        obj_iter = iter(enumerate(url_components_list))

        start_time = datetime.now()    

        if not self.args.machine_out:
            print('start working with:', self.description)
            print('Work with {} threads at {}'.format(threads_num, start_time))
            print('Push Ctrl+C for exit')

        threads = []

        for i in range(threads_num):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)
        try:
            while True:
                (num, obj, ) = next(obj_iter)
                self.queue.put(GetCommand(num, obj))

        except StopIteration:

            if not self.args.machine_out:
                 with self.stdout_mutex:
                    print('End of operation')

        except KeyboardInterrupt:
            if not self.args.machine_out:
                with self.stdout_mutex:
                    print('Operation canceled by keyboard')

        #New line for stdout parsing
        print()
           
        for i in range(threads_num):
            self.queue.put(ExitCommand())

        for thread in threads:
            thread.join(timeout=60)

        zths = []
        for th in threads:
            if th.is_alive():
                zths.append(th)

        stop_time = datetime.now()
        if not self.args.machine_out:
            print('Zombies:')
            print(zths)
            print('Processed in', stop_time - start_time)
        
        try:
            if out_filename == 'stdout':
                outfile = stdout
            else:
                outfile = open(out_filename, 'w')

            dump(
                self.obj_list.get_list(), 
                outfile,
                indent=4,
                default=default_json,
                sort_keys=True
            )
        finally:
            if out_filename != 'stdout':
                outfile.close()

        if not self.args.machine_out:
            print('Saved at', out_filename, datetime.now())

def main():
    print('Hello World!')
    scraper = Scraper()
    scraper.run()

if __name__ == '__main__':
    main()