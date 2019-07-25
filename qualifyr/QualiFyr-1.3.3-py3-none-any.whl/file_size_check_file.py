import csv, sys
from qualifyr.quality_file import QualityFile
from qualifyr.utility import string_to_num, get_logger

class FileSizeCheckFile(QualityFile):
    logger = get_logger(__file__)
    file_type = 'file_size_check'

    def validate(self):
        # method to check file looks like what it says it is
        '''Returns valid rows from file. An empty list if invalid'''
        with open(self.file_path) as fh:
            reader = csv.reader(fh, delimiter='\t')
            rows = list(reader)
            if rows[0][0] == 'file' and rows[0][-1] == 'size' and  len(rows) == 2:
                return rows
            else:
                return []
    

    def parse(self):
        # read in file and make a dict:
        rows = self.validate()
        if len(rows) == 0:
            self.logger.error('{0} file invalid'.format(self.file_type))
            raise(Exception)

        else:
            fields = rows[0]
            for index, field in enumerate(fields):
                self.metrics[field] = string_to_num(rows[1][index])




