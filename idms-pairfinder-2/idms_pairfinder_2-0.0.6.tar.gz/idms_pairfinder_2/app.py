
from emzed import gui, io
import wtbox
import os

here = os.path.dirname(os.path.abspath(__file__))
import workflow_config as wfc
from main_pair_finder import main_pair_finder

def config2text(d):
    blocks=[]
    for key, value in d.items():
        blocks.append(_build_line(key, value))
    return '\n'.join(blocks)

def _build_line(key, value):
    lines=[]
    if isinstance(value, dict):
        lines.append(key)
        for sub, val in value.items():
            sub_line=(_build_line(sub, val))
            lines.append('\t'.join(['', sub_line]))
    else:
        lines.append(':\t'.join([str(key), str(value)]))
    return '\n'.join(lines)
    
    
            

class WorkflowGui(gui.WorkflowFrontend):
    """
    """
    samples=gui.WorkflowFrontend().set_defaults()
    project_path=gui.DirectoryItem('project path', default=here, 
                                   help='enter main project folder path.')
    _help=gui.RunJobButton('show help', method_name='show_help')
    config=gui.RunJobButton('setup config', method_name='change_config_settings')
    __=gui.RunJobButton('show current config', method_name='show_config')
    run_pipeline=gui.RunJobButton('run analysis', method_name='start_analysis') 
    
    def show_help(self):
        wfc._show_help()
    
    
    
    def change_config_settings(self):
        if not self.config:
            self.handle_config()
        self.config=wfc.setup_workflow_config(self.config, self.project_path)
            
    
    def load_samples(self):
        formats=['mzML', 'mzXML']
        help12c='please select the mz(X)ML file of the natural labeled sample'
        help13c='please select the mz(X)ML file of the uniformly 13C labeled sample'
        helpidms='please select the mz(X)ML file of the natural labeled U13C labeled mixture sample'
        
        pathes=gui.DialogBuilder('select samples')\
        .addFileOpen('natural labeled sample', basedir=self.project_path, formats=formats,
                     help=help12c)\
        .addFileOpen('U13C labeled sample', basedir=self.project_path, formats=formats,
                     help=help13c)\
        .addFileOpen('IDMS sample', basedir=self.project_path, formats=formats,
                     help=helpidms)\
        .show()
        self.samples=wtbox.in_out.load_peakmaps(pathes)
        assert len(self.samples)==3
    

    def start_analysis(self):
        if not self.config:
            self.handle_config()
        if not self.samples:
            self.load_samples()
        self.result=main_pair_finder(self.samples, self.config)
        self.save_results()


    
    def handle_config(self):
        self.config=wfc.get_config(self.config, self.project_path)
        
        
        
    def show_config(self):
        if not self.config:
            self.handle_config()
        gui.showInformation(config2text(self.config))
    

    
    def save_results(self):
        path= self._get_result_path()
        path=gui.askForSave(startAt=path, extensions=['table'])
        io.storeTable(self.result, path, forceOverwrite=True)
    
    
    def _get_result_path(self, data):
        path=os.path.join(self.project_path, 'RESULTS')
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    
        
def run():
    WorkflowGui().show()    
    
if __name__ == '__main__':
    run()    