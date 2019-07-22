import csv, sys
from qualifyr.quality_file import QualityFile
from qualifyr.utility import string_to_num, get_logger

class BactinspectorFile(QualityFile):
    logger = get_logger(__file__)
    file_type = 'bactinspector'

    def validate(self):
        # method to check file looks like what it says it is
        '''Returns valid rows from file. An empty list if invalid'''
        with open(self.file_path) as fh:
            reader = csv.DictReader(fh, delimiter='\t')
            rows = list(reader)
            if reader.fieldnames[0] == 'file' and reader.fieldnames[-1] == 'result' and  len(rows) == 1:
                return reader.fieldnames, rows[0]
            else:
                return {}, []
    

    def parse(self):
        # read in file and make a dict:
        fields, data = self.validate()
        if len(data) == 0:
            self.logger.error('{0} file invalid'.format(self.file_type))
            raise(Exception)

        else:
            for field in fields:
                self.metrics[field] = string_to_num(data[field])




