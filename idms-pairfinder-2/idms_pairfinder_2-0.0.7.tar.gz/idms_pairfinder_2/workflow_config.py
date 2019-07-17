# -*- coding: utf-8 -*-
"""
Created on Wed Jul 03 13:42:55 2019

@author: pkiefer
"""
import wtbox
import os
from emzed import gui

def setup_workflow_config(config, project_dir):
    try:
        default_dest= config['destination']
    except:
        default_dest=project_dir
    choices=['manual_parameter_configuration', 'default_nano_lc', 'default_uplc_amino_acids']
    mode_info='IDMS_pairfinder provides 2 default configuration settings ....'
    mode, destination=gui.DialogBuilder('setup paramaters')\
    .addChoice('select configuration mode', choices, default=0, help=mode_info)\
    .addDirectory('select destination for rt alignment plots', help='', default=default_dest)\
    .show()
    if mode==1:
        config = _default_idms_ident_nano_lc(destination)
    elif mode==2:
        config = _config_idms_ident_uplc(destination)
    else:
        config = manual_wf_config(config, project_dir, destination)
    config['project_dir']=project_dir
    return config
    
    


def _default_idms_ident_nano_lc(destination):
    d={}
    d['mztol']=0.002
    d['mzdiff']=0.0009
    d['rttol']=5.0
    d['min_specs']=4
    d['spectral_signal_noise']=6.0
    ff_config=wtbox.feature_extraction.ff.get_default_ff_metabo()
    ff_config['common_chrom_peak_snr']=3.0 # signal to noise of the mass trace
    ff_config['mtd_mass_error_ppm']=20.0
#    ff_config=wtbox.feature_extraction.ff.adapt_ff_metabo_config(config, advanced=True)
    d['ff_config']=ff_config
    d['determine_noise_level']=True
    d['rtalign']={'maxRtDifference': 100.0, 'maxMzDifference': 0.005, 
                'maxMzDifferencePairfinder': 0.003}
    d['group_idms_peaks']={'key2tol': {'mz':None, 'rt': None},  'scaling':3.0, 
                            'diff_col':'area'}
    d['subtract_blank']=d['group_idms_peaks']
    d['feature_regrouper']={'min_abundance': 0.005, 'max_c_gap': 0, 'mz_tolerance': 0.0008, 
                'elements': ('C','H', 'N', 'O', 'S')}
    d['idms_ident']={'db': None, 'binwidth': 0.003, 'abs_tol': 0.003, 'rel_tol':None}
    d['destination']=destination
    d['remove_sholders']=True
    return d
    

def _config_idms_ident_uplc(destination):
    d={}
    d['mztol']=0.002
    d['mzdiff']=0.0009
    d['rttol']=3.0
    d['min_specs']=3
    d['spectral_signal_noise']=6.0
    ff_config=wtbox.feature_extraction.ff.get_default_ff_metabo()
    ff_config['common_noise_threshold_int']= 1000.0
    ff_config['common_chrom_peak_snr']=3.0
    ff_config['common_chrom_fwhm']=5.0
    ff_config['epdet_max_fwhm']= 60.0
    ff_config['epdet_min_fwhm']=1.0
    ff_config['ffm_local_rt_range']=2.0
    ff_config['mtd_min_trace_length']=2.0
    ff_config['mtd_mass_error_ppm']=20.0
    d['ff_config']=ff_config
    d['determine_noise_level']=True
    d['rtalign']=False
    d['group_idms_peaks']={'key2tol': {'mz':None, 'rt': None},  'scaling':3.0, 
                            'diff_col':'area'}
    d['subtract_blank']=d['group_idms_peaks']
    d['feature_regrouper']={'min_abundance': 0.005, 'max_c_gap': 0, 'mz_tolerance': d['mzdiff'], 
                'elements': ('C','H', 'N', 'O', 'S')}
    d['destination']=destination
#    d['idms_ident']={'db': None, 'binwidth': 0.003, 'abs_tol': 0.003, 'rel_tol':None}
    
    d['remove_sholders']=True
    return d




def manual_wf_config(config, project_path, destination):
        if not config:
            ff_config=wtbox.feature_extraction.ff.get_default_ff_metabo()
        else:
            _help=get_key2help()
            ff_config=config['ff_config']
        ff_config=wtbox.feature_extraction.ff.adapt_ff_metabo_config(ff_config, advanced=True)
        d=_get_default_params_dict(config)
        params=gui.DialogBuilder('change idms pairfinder configuration settings')\
        .addFloat('minimal spectral signal to noise', default=d['s2n'], help=_help['s2n'] )\
        .addInt('minimal no of spectra per peak', default= d['min_specs'], help=_help['min_specs'])\
        .addFloat('rttol', default=d['rttol'], help=_help['rttol'])\
        .addFloat('mztol', default=d['mztol'], help=_help['mztol'])\
        .addFloat('C13 isotopes distance tolerance', default=d['mzdiff'], help=_help['mzdiff'])\
        .addFloat('f_regrouper min_abundance', default=d['min_abund'], help=_help['min_abund'])\
        .addFloat('rt align maxMzDifference', default=d['max_mz_diff'], help=_help['max_mz_diff'])\
        .addFloat('rt align maxMzDifferencePairfinder', default=d['max_mz_diff_pair'],
                  help=_help['max_mz_diff_pair'])\
        .addFloat('rt align maxRtDifference', default=d['max_rt_diff'], help=_help['max_rt_diff'])\
        .addDirectory('rt align destination', default=destination, help=_help['destination'])\
        .addBool('perform retention time alignemnt', default = d['rtalign'], help=_help['rtalign'])\
        .addBool('determine noise level', default = d['det_s2n'], help=_help['det_s2n'])\
        .addBool('remove shoulder', default = d['rm_shoulders'], help=_help['rm_shoulders'])\
        .show()
        return _assign_params(ff_config, params, project_path)

def get_key2help():
    d=dict()
    d['s2n']='minimal required signal to noise level at peak maximum to be accepted as peak; '\
            'if noise level is determined from sample spectra'
    d['min_specs']='minimal number of spectra per peak'
    d['rttol']='allowed maximal retention time difference of two LC-MS peaks in different samples'\
                ' to be accepted as coeluting peaks'
    d['mztol']='allowed maximal m/z difference of two lc-ms peaks in different samples '\
                'to be accepted as same m/z'
    d['mzdiff']='allowed maximal m/z difference within an isotopologue pattern of the same sample'\
    ' to be accepted as 13C - 12C isotopologue distance'
    d['min_abund']='minimal abundance relative of an isotopologue relative to the monoisotopic'\
                   ' peak to be accepted as isotopologue'
    d['rtalign']='if True, perform retention time alignment; this is necessary if important rt variations'\
                  ' (rt difference > peak width) between the same metabolites in different samples '\
                  'are observed; in case of most UPLC methods this is not required'  
    d['det_s2n']='if True (default), the minimal required peak intensity is based'\
                ' on spectral signal to noise value of the sample. If False, the ff_metabolo common_noise_threshold_int'\
                ' parameter is used instead'
    d['rm_shoulders']='removes artefact peaks from Orbitrap FTMS data; default is True'
    d['max_mz_diff']='parameter of the emzed rt align module: max allowed difference'\
                       ' in mz values for super imposer'
                       
    d['max_mz_diff_pair']='parameter of the emzed based rt align module: max allowed difference'\
                       ' in mz values for pair finding'
    d['max_rt_diff']='parameter of emzed based rt align module: max allowed difference'\
                       ' in rt values for searching matching features'
    d['destination']='The folder name in which retention time alignment plots will be saved'
    return d

def _get_default_params_dict(config):
    d={}
    d['s2n']=10.0
    d['min_specs']=10
    d['rttol']=3.0
    d['mztol']=3.0
    d['mzdiff']=0.0009
    d['min_abund']=0.005
    d['rtalign']=True
    d['det_s2n']=True
    d['rm_shoulders']=True
    d['max_mz_diff']=0.005
    d['max_mz_diff_pair']=0.003
    d['max_rt_diff']=60.0
    if isinstance(config, dict):
        d['s2n']=config['spectral_signal_noise']
        d['min_specs']=config['min_specs']
        d['rttol']=config['rttol']
        d['mztol']=config['mztol']
        d['mzdiff']=config['mzdiff']
        d['min_abund']=config['feature_regrouper']['min_abundance']
        if isinstance(config['rtalign'], bool):
            d['rtalign']=config['rtalign']
        else:
            d['rtalign']=True
            d['max_mz_diff']=config['rtalign']['maxMzDifference']
            d['max_mz_diff_pair']=config['rtalign']['maxMzDifferencePairfinder']
            d['max_rt_diff']=config['rtalign']['maxRtDifference']
        d['det_s2n']=config['determine_noise_level']
        d['rm_shoulders']=config['remove_sholders']
    return d
    
        


def _assign_params(ff_config, params, project_path):
    # decompose params
    s2n, min_specs, rttol, mztol, mzdiff, min_abund=params[:6]
    max_mz_diff, max_mz_diff_pair, max_rt_diff, dest, rtalign, det_s2n, rm_sh=params[6:]
    d={}
    d['ff_config']=ff_config
    d['group_idms_peaks']={'key2tol': {'mz':None, 'rt': None},  'scaling':3.0, 
                            'diff_col':'area'}
    d['subtract_blank']=d['group_idms_peaks']
    d['feature_regrouper']={'elements': ('C','H', 'N', 'O', 'S'), 'max_c_gap': 0, 
                            'min_abundance': min_abund, 'mz_tolerance': mzdiff}
    d['determine_noise_level']=det_s2n
    d['mztol']=mztol
    d['mzdiff']=mzdiff
    d['rttol']=rttol
    d['min_specs']=min_specs
    d['rtalign']=rtalign
    if rtalign:
        align={'maxMzDifference': max_mz_diff,
             'maxMzDifferencePairfinder': max_mz_diff_pair,
             'maxRtDifference': max_rt_diff},
        d['rtalign']=align
    d['spectral_signal_noise']=s2n
    d['destination']=dest
    d['remove_sholders']=rm_sh
    d['project_path']=project_path
    return d
    
    

#################################################################################################
# config management

def get_config(config, project_dir, filename='idms_pairfinder_config.json'):
    if not config:
        config=load_config(project_dir)
    if not config:
        config=setup_workflow_config(config, project_dir)
    save_config(config, project_dir, filename)
    return config

def load_config(project_dir, filename='idms_pairfinder_config.json'):
    path=os.path.join(project_dir, filename)
    if os.path.exists(path):
        config=wtbox.in_out.load_dict(path)
        return config
    

def save_config(config, project_path, filename='idms_pairfinder_config.json'):
    path=os.path.join(project_path, filename)
    wtbox.in_out.save_dict(config, path, True)


def _make_dir(dir_):
    if not os.path.exists(dir_):
        os.mkdir(dir_)

def convert_config_to_relative_path(config, project_dir):
    """ replaces all absolute pathes by relative ones (relative to project directory)
    """
    project=config['project_dir']
    ids=config['batch_ids']
    keys=['batch2samples', 'batch2result']
    #1) replace current_result
    if config['current_result']:
        rel_path=get_relative_path(config['current_result'], project)
        _path_exists(rel_path, project_dir)
        config['current_result']=rel_path
    # 2) adapt result pathes
    for key in keys:
        _update_config_pathes(config, key, ids, project_dir)
    config['project_dir']=project_dir


def _path_exists(rel_path, project):
    path=os.path.join(project, rel_path)
    assert os.path.exists(path), '%s is not existing!' %path



def _update_config_pathes(config, key, ids, project):
    
    for id_ in ids:
        if key=='batch2result':
            rel_path=get_relative_path(config[key][id_], config['project_dir'])
            _path_exists(rel_path, project)
            config[key][id_]=rel_path
        elif key=='batch2samples':
            # samples are not stored within the project. We therefore check whether the current
            # sample pathes do exist
            pathes=config[key][id_]
            # 1) get relative pathes
            try:
                try_relative_pathes(config, key, id_, pathes, config['project_dir'])
            except:
                abs_pathes=_get_sample_folder(pathes, project)
                try_relative_pathes(config, key, id_, abs_pathes, project)


def try_relative_pathes(config, key, id_, pathes, project):
    rel_pathes=[get_relative_path(path, config['project_dir']) for path  in pathes]
    assert all([p!=None for p in pathes])    
    abs_pathes=[os.path.join(project, rel_p) for rel_p in rel_pathes]
    if all([os.path.exists(p) for p in abs_pathes]):
        config[key][id_]=rel_pathes
    else:
        config[key][id_]=pathes


def _get_sample_folder(pathes, project):
    sample_names=[os.path.basename(path) for path in pathes]
    names='\n'.join(sample_names)
    gui.showWarning('Pathes of peakmaps got lost! Please select'\
                        'folder containing peakmaps:\n %s' %names)
    m=0
    while True:
        dir_=gui.DialogBuilder('select project sample folder')\
        .addDirectory('select sample folder', default=project)\
        .show()
        new_pathes=[os.path.join(dir_, s) for s in sample_names]
        
        if all([os.path.exists(p) for p in new_pathes]):
            return new_pathes
        m+=1
        if m>3:
            print names
            assert False, 'samples seem to be hard to find. Check your data folders manually!! '



def get_relative_path(path, project_dir):
    if os.path.isabs(path):
        path=os.path.normpath(path)
        project_dir=os.path.normpath(project_dir)
        try:
            if os.path.commonprefix([path, project_dir])==project_dir:
                return os.path.relpath(path, project_dir)
        except:
            pass
    return path


####################################################################################
def _show_help():
    text=""" RUNNIG THE IDMS_PAIRFINDER APP  \n
GENERAL: An emzed2 application for LC-MS data acquired with Orbitrap high mass resolution instruments.\n
The application allows untargeted extraction of metabolites based on isotope dilution 
mass spectrometry (IDMS) method. For each metabolite a pair of an natural labeled [12C] and an 
uniformly 13C labeled [13C] isotopologue is present in the same sample, since the sample is a 
mixture of respective cell extracts. 
As unlabeled and labeled isotopologues have the same physicochemical properties, the corresponding 
LC-MS peaks will co-elute and the m/z difference equals \n
n* (mz.C13 - mz.C12)*z \n 
where n corresponds to the number of the metabolite carbon atoms,
mz.c12 is the m/z of the 12C isotope, mz.C13 equals the m/z of the correpsonding 13C isotope, 
and z is the charge state of the ions. 
In addition, untargeted metabolite extraction is not only based on analysis of an IDMS sample, 
but also on individual LC-MS measurements of the corresponding [12C] and the [13C] extracts, 
respectively. Separate analysis allows direct assignment of isotopologue identity ([12C], [13C]) 
in the IDMS sample. 
Overall, this approach significantly reduces the number of false positive metabolites 
and enhances metabolite annotation as the number carbon atoms can be determined from the 
isotopologue mass distances.

PROJECT FOLDER: You have to select a project folder where app results will be saved. 
Ideally, the folder has also a subfolder containing the LC-MS data.\n
SAMPLES: The approach requires samples from two individual cultivations carried out on a 
natural labeled (n. l.) carbon source and on a uniformly 13C ([U-13C]) labeled carbon source, 
respectively.
LC-MS analysis is performed with 1) the natural labeled sample, 2) the [U-13C] sample, and
a 50 : 50 mixture of both samples (IDMS). \n
PARAMETER CONFIGURATION: The app provides two default configurations for LC-MS methods routinely used in our lab. In addition, there is the possibility to setup individual configurations. For each parameter a short help is provided in the GUI, which pops up after a few seconds shown when pointing with the mouse to the parameter.

"""
    gui.showInformation(text)