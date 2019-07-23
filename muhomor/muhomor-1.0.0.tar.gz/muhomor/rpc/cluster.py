import multiprocessing as mp
from multiprocessing import Value, Queue
from typing import Dict, List, Union, Any
import os
import time
import queue
from .config import Config, configure, get_config
from .worker import RpcServer
from .entry_points import _is_entrypoint
from ..exceptions import NotEnoughWorkers
import threading
import inspect
from logging import getLogger
from ..utils.filesystem import load_config_section, decorator_containers_from_module
import sys


logger = getLogger(__name__)


class Cluster:

    def __init__(self, service, workers_num, restart_dead_workers=True):
        self.workers_num = workers_num
        self.service_name = service.name
        self.service_class = service
        self.start_queue = Queue(maxsize=1)
        self.workers = {}
        self.worker_stop_sig: Dict[int, Value] = {}
        self.restart_dead_workers = restart_dead_workers
        self.last_health_report = time.time()
        self.loop_interval = 1
        self._processes_counter = 0

    def run(self):
        logger.info(f'Starting cluster `{self.service_name}`; process id: {os.getpid()}')
        try:
            for _ in range(self.workers_num):
                self.worker_process()
            logger.info(f'Cluster `{self.service_name}` started with {len(self.workers)} workers')
            if len(self.workers) < self.workers_num:
                logger.info(f'Not enough workers. Stopping cluster `{self.service_name}`...')
                raise NotEnoughWorkers
            self.loop(interval=self.loop_interval)
        except KeyboardInterrupt:
            logger.info(f'Stopping cluster `{self.service_name}`')
        except NotEnoughWorkers:
            pass
        finally:
            if not len(self.workers):
                logger.info(f'Cluster `{self.service_name}` stopped because workers pool is empty')
            else:
                for c in self.worker_stop_sig.values():
                    c.value = 1
                for pid in self.workers:
                    self.workers[pid].join()
                logger.info(f'Cluster `{self.service_name}` stopped because all workers completed jobs')

    def start_worker(self, start_queue: Queue, process_stopper: Value, **kwargs):
        try:
            worker = RpcServer(**kwargs)
            worker.setup_provider(self.service_class)
            worker.set_process_stopper(process_stopper)
            start_queue.put(worker.worker_id, block=True, timeout=10)
            worker.run()
        except BaseException as e:
            logger.error(f'Worker creation in cluster `{self.service_name}` failed: {e}')
            start_queue.put(False, block=True, timeout=10)

    def worker_process(self):
        stopper = Value('i', 0)
        self._processes_counter += 1
        proc_name = f'{self.service_name:15s} {self._processes_counter:5d}'
        p = mp.Process(target=self.start_worker,
                       name=f'{proc_name}',
                       daemon=True,
                       args=(self.start_queue, stopper,),
                       kwargs={'name': self.service_name})
        p.start()
        started = False
        try:
            started = self.start_queue.get(block=True, timeout=10)
        except queue.Empty:
            logger.warning(f'Worker start queue is empty in cluster `{self.service_name}`...')
            pass
        if started:
            logger.info(f'{RpcServer.alias(self.service_name, started)} started')
            self.worker_stop_sig[p.pid] = stopper
            self.workers[p.pid] = p
        else:
            p.terminate()

    def loop(self, interval=1):
        while True and len(self.workers) > 0:
            time.sleep(interval)
            dead_workers = list()
            for pid in self.workers:
                if not self.workers[pid].is_alive():
                    dead_workers.append(pid)
            if len(dead_workers) > 0:
                for pid in dead_workers:
                    exitcode = self.workers[pid].exitcode
                    del self.workers[pid]
                    if exitcode != 0:
                        logger.error(f'{RpcServer.alias(self.service_name, pid)} died, code: {exitcode}')
                        if self.restart_dead_workers:
                            logger.info(f'Attempting to start new worker in cluster `{self.service_name}`...')
                            self.worker_process()
                    else:
                        logger.info(f'{RpcServer.alias(self.service_name, pid)} exited.')
            if time.time() - self.last_health_report > 5:
                self.last_health_report = time.time()
                if self.workers_num != len(self.workers):
                    logger.debug(f'Alive workers in cluster `{self.service_name}`: {len(self.workers)}')


def _verify_rpc_provider_class(obj):
    config = get_config()
    if hasattr(obj, 'name'):
        if len(obj.name) > config.max_service_name_len:
            logger.warning(f'Name of RPC provider `{obj.__name__}` exceeds '
                           f'{config.max_service_name_len} chars.')
        else:
            return True
    else:
        logger.warning(f'Class `{obj.__name__}` contains RPC entry points, '
                       'but has no `name` attribute. If you want it to be registered as service, '
                       'include `name` attribute outside of __init__ scope.')
    return False


def rpc_entrypoint_container_extractor(module):
    containers = list()
    for _, maybe_container in inspect.getmembers(module, lambda obj: isinstance(obj, type)):
        if inspect.getmembers(maybe_container, _is_entrypoint):
            if _verify_rpc_provider_class(maybe_container):
                containers.append(maybe_container)
    return containers


def _run_one(service):
    config = get_config()
    cluster = Cluster(service=service,
                      workers_num=config.workers if config.workers > 0 else config.default_workers_cpu_based,
                      restart_dead_workers=config.restart_dead_workers)
    cluster.run()


def _run_multi(services):
    threads = []
    for service in services:
        t = threading.Thread(target=_run_one, daemon=True, args=(service,))
        t.start()
        threads.append(t)
    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            time.sleep(5)
            break


def run_cluster(service_or_services: Union[str, List[type], type], conf: Dict[str, Any] = None):
    """
    Starting cluster of services with multiple workers per service.
    Each cluster runs in separate thread. And every of those threads creates separate process for each service worker.
    If you run cluster on MacOS it is possible that you will face fork problem. Details are here:
    http://sealiesoftware.com/blog/archive/2017/6/5/Objective-C_and_fork_in_macOS_1013.html
    To fix it, add following to .bash_profile:
    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
    """
    if type(service_or_services) is str and \
            (service_or_services.__contains__('.') or service_or_services.__contains__(':')):
        services = decorator_containers_from_module(service_or_services, rpc_entrypoint_container_extractor)
        if services and len(services):
            return run_cluster(services, conf)
        else:
            logger.critical('Running cluster failed. No RPC providers found.')
            return
    services = [service_or_services] if isinstance(service_or_services, type) else service_or_services
    if conf is not None:
        configure(**conf)
    if len(services) > 1:
        _run_multi(services)
    else:
        _run_one(services[0])


def main(args):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

    if not args.path or not len(args.path):
        logger.critical(f'Critical error! Wrong services path: `{args.path}`')
        return

    run_cluster(args.path,
                load_config_section(args.config, Config.external_conf_file_section_name) if args.config else None)
