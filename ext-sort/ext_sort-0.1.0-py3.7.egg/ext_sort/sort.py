import abc
import contextlib
import heapq
import logging
import multiprocessing as mp
import tempfile

logger = logging.getLogger(__package__)


class Serializer(abc.ABC):
    """
    Abstract data serializer.
    Custom serializers should be inherited from it.
    """

    def __init__(self, writer):
        self._writer = writer

    @abc.abstractmethod
    def write(self, item):
        """
        Serializes an item and writes it to the writer.

        :param item: item to be serialized
        """


class Deserializer(abc.ABC):
    """
    Abstract data serializer.
    Custom deserializers should be inherited from it.
    """

    def __init__(self, reader):
        self._reader = reader

    @abc.abstractmethod
    def read(self):
        """
        Reads an item from the reader and deserializes it.

        :return: deserialized item
        """

    def __iter__(self):
        return self

    def __next__(self):
        item = self.read()
        if not item:
            raise StopIteration

        return item


class ByteLineDeserializer(Deserializer):
    """
    Byte line deserializer. Deserializes
    """

    def read(self):
        return self._reader.readline().rstrip()


class ByteLineSerializer(Serializer):
    """
    Byte line serializer. Serializes
    """

    def write(self, item):
        self._writer.write(item + b'\n')


def sort(
    reader, writer,
    butch_size, butch_mem=None, total_mem=None,
    Serializer=ByteLineSerializer,
    Deserializer=ByteLineDeserializer,
    workers_cnt=None,
    tmp_dir=None,
):
    """
    Sorts a file using external sort algorithm.
    """

    workers_cnt = workers_cnt or mp.cpu_count()

    logger.debug(f"sorting file using {workers_cnt} workers (butch_size: {butch_size})")

    with tempfile.TemporaryDirectory(dir=tmp_dir) as tmp_dir:
        logger.debug(f"using '{tmp_dir}' as temporary directory")

        with mp.Pool(workers_cnt) as pool:
            deserializer = Deserializer(reader)
            async_results = []

            butch = []
            for item in deserializer:
                butch.append(item)
                if len(butch) == butch_size:
                    butch_filename = _flush_butch_to_tmp_file(butch, tmp_dir, Serializer)
                    async_results.append(pool.apply_async(_sort_file, kwds=dict(
                        filename=butch_filename,
                        Serializer=Serializer,
                        Deserializer=Deserializer,
                    )))

            if len(butch):
                butch_filename = _flush_butch_to_tmp_file(butch, tmp_dir, Serializer)
                async_results.append(pool.apply_async(_sort_file, kwds=dict(
                    filename=butch_filename,
                    Serializer=Serializer,
                    Deserializer=Deserializer,
                )))

            tmp_filenames = [res.get() for res in async_results]

        _merge_files(tmp_filenames, writer, Serializer, Deserializer)


def _sort_file(filename, Serializer, Deserializer):
    logger.debug(f"[{mp.current_process().name}] sorting file '{filename}'...")

    with open(filename, 'rb') as reader:
        data = [item for item in Deserializer(reader)]

    data = sorted(data)

    result_filename = f"{filename}.sorted"
    with open(result_filename, 'wb') as writer:
        serializer = Serializer(writer)

        for item in data:
            serializer.write(item)

    return result_filename


def _flush_butch_to_tmp_file(butch, tmp_dir, Serializer, filename_prefix='butch-'):
    tmp_fd, tmp_filename = tempfile.mkstemp(prefix=filename_prefix, dir=tmp_dir)

    logger.debug(f"creating butch file '{tmp_filename}'...")

    with open(tmp_fd, mode='wb') as writer:
        serializer = Serializer(writer)

        for item in butch:
            serializer.write(item)

    butch.clear()

    return tmp_filename


def _merge_files(filenames, writer, Serializer, Deserializer):
    logger.debug(f"merging result...")

    with contextlib.ExitStack() as stack:
        tmp_files = [Deserializer(stack.enter_context(open(filename, mode='rb'))) for filename in filenames]

        serializer = Serializer(writer)
        for item in heapq.merge(*tmp_files):
            serializer.write(item)
