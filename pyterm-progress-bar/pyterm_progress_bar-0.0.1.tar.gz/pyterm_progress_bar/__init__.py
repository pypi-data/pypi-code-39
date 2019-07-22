import sys


class ProgressBar:
    def __init__(self, name="Progress", char='#'):
        self.name = name
        self.char = char

    def set_progress(self, progress):
        self.progress = progress
        width_done = int(self.width * progress)
        self.done_str = self.char * width_done
        self.to_do_str = ' ' * (self.width - width_done)

    def update(self, progress=None):
        if progress != None:
            self.set_progress(progress)
        percent = str(int(self.progress * 100))
        ret = sys.stdout.write(f'\r{self.name}: [{self.done_str}{self.to_do_str}] {percent}%')

    def start(self):
        # TODO: Read terminal width
        # TODO: Move width reading into update method
        self.width = 60
        self.update(progress=0)


class Loop():
    """
    Pass __init__ a function that will be executed.
    The first parameter passed to your function will be the counter, from 0 to 'iterations'.
    You may specify ONE additional parameter, which will be passed as the second parameter.
    """
    def __init__(self, code_block, number_of_iterations=1, param=None, progress_bar_name=None, progress_bar_char=None):
        self.code_block = code_block
        self.iterations = number_of_iterations
        self.function_param = param
        if progress_bar_name:
            self.progress_bar_name = progress_bar_name
        else:
            self.progress_bar_name = f'Running {code_block.__name__}'
        if progress_bar_char:
            self.progress_bar = ProgressBar(name = self.progress_bar_name, char=progress_bar_char)
        else:
            self.progress_bar = ProgressBar(name=self.progress_bar_name)

    def execute(self):
        self.progress_bar.start()
        for i in range(0, self.iterations):
            if self.function_param != None:
                self.code_block(i, self.function_param)
            else:
                self.code_block(i)
            self.progress_bar.update((i+1)/self.iterations)
