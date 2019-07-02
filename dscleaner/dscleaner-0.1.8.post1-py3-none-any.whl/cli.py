'''from dscleaner.ifileinfo import IFileInfo
from dscleaner.fileinfo import FileInfo
from dscleaner.fileutil import FileUtil
from dscleaner.filewriter import FileWriter
from dscleaner.csvfileinfo import CsvFileInfo
from dscleaner.merger import Merger'''
import fileinfo
import fileutil
import filewriter
import utils as u
import click
@click.command()
@click.argument(
    'input',
    type=click.Path(exists=True,resolve_path=True),
)
@click.argument(
    'output',
    type=click.Path(exists=False,file_okay=False,dir_okay=False,resolve_path=True),
)
@click.option(
    '--resample',
    '-r',
    help='Value the dataset must be resampled to',
)
@click.option(
    '--fix_duration',
    '-f',
    help='Duration every dataset file should have.',
)
def cli(resample,fix_duration,input,output):
    #it also should normalize but in order to do that it must accept an array of values...
    import os
    if(os.path.isdir(input)):
        print(">pasta")
        pass
    else:
        print(">ficheiro")
        pass
    
    if(resample is not None):
        if(not u.is_number(resample)):
            print("Invalid resample value!")
            return
        resample= float(resample)
        print("Resampled to:", resample)

    if(fix_duration is not None):
        if(not u.is_number(fix_duration)):
            print("Invalid fix_duration value!")
        fix_duration = float(fix_duration)
        print("New duration:", fix_duration)

    with fileinfo.FileInfo(input) as file:
        with fileutil.FileUtil(file) as futil:
            if(fix_duration):
                futil.fix_duration(fix_duration)
            if(resample):
                futil.resample(resample)
        with filewriter.FileWriter(file) as fw:
            fw.create_file(output)
    
cli()