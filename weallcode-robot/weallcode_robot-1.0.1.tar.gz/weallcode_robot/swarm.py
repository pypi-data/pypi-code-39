from multiprocessing import Process
from .robot import Robot


class Swarm:
  def __init__(self, *names):
    self.robots = [Robot(name) for name in names]
    self.robots_len = len(self.robots)

    for method_name in dir(Robot):
      if callable(getattr(Robot, method_name)) and not method_name.startswith("__"):
        setattr(self, method_name, self.make_method(method_name))

  def make_method(self, method_name):
    return lambda *args : self.run_on_all(method_name, *args)

  def run_on_all(self, method_name, *args):
    processes = []

    for idx, robot in enumerate(self.robots):
      p = Process(target=getattr(robot, method_name), args=args)
      processes.append(p)

    [x.start() for x in processes]
