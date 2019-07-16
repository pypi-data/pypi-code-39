from threading import Thread


def parallelize_pyspark_scheduling(transformations, arguments=()):
    """

    Args:
        transformations: Iterable of transformation function.
        arguments (tuple): This is passed to each transformation.

    """

    thread_generator = [
        _MyThread(target=transformation, args=arguments)
        for transformation in transformations
    ]

    _execute_threads(thread_generator)


class _MyThread(Thread):
    def run(self):
        """Catch exception and make it available."""
        try:
            super().run()
        except Exception as err:
            self.err = err
        else:
            self.err = None


def _execute_threads(threads):
    """
    Start all threads and raise at least 1 exception they caught.

    Args:
        threads (list): list of :class:`optel.datalake.utils._MyThread`

    """
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    for t in threads:
        if t.err:
            raise t.err
