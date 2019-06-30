from pathlib import Path
import os
import shutil
import numpy as np

import spikeextractors as se
from ..basesorter import BaseSorter
from ..sorter_tools import _run_command_and_print_output

try:
    import circus
    HAVE_SC = True
except ImportError:
    HAVE_SC = False


class SpykingcircusSorter(BaseSorter):
    """
    """

    sorter_name = 'spykingcircus'
    installed = HAVE_SC

    _default_params = {
        'probe_file': None,
        'detect_sign': -1,  # -1 - 1 - 0
        'adjacency_radius': 200,  # Channel neighborhood adjacency radius corresponding to geom file
        'detect_threshold': 6,  # Threshold for detection
        'template_width_ms': 3,  # Spyking circus parameter
        'filter': True,
        'merge_spikes': True,
        'auto_merge': 0.5,
        'num_workers': None,
        'electrode_dimensions': None,
        'whitening_max_elts': 1000,  # I believe it relates to subsampling and affects compute time
        'clustering_max_elts': 10000,  # I believe it relates to subsampling and affects compute time
        }

    installation_mesg = """
        >>> pip install spyking-circus

        Need MPICH working, for ubuntu do:
            sudo apt install libmpich-dev

        More information on Spyking-Circus at: 
            https://spyking-circus.readthedocs.io/en/latest/
    """

    def __init__(self, **kargs):
        BaseSorter.__init__(self, **kargs)

    def _setup_recording(self, recording, output_folder):
        p = self.params
        source_dir = Path(__file__).parent

        # save prb file:
        if p['probe_file'] is None:
            p['probe_file'] = output_folder / 'probe.prb'
            se.save_probe_file(recording, p['probe_file'], format='spyking_circus',
                               radius=p['adjacency_radius'], dimensions=p['electrode_dimensions'])

        # save binary file
        file_name = 'recording'
        np.save(str(output_folder / file_name), recording.get_traces().astype('float32'))

        if p['detect_sign'] < 0:
            detect_sign = 'negative'
        elif p['detect_sign'] > 0:
            detect_sign = 'positive'
        else:
            detect_sign = 'both'

        sample_rate = float(recording.get_sampling_frequency())

        # set up spykingcircus config file
        with (source_dir / 'config_default.params').open('r') as f:
            circus_config = f.readlines()
        if p['merge_spikes']:
            auto = p['auto_merge']
        else:
            auto = 0
        circus_config = ''.join(circus_config).format(sample_rate, p['probe_file'], p['template_width_ms'],
                    p['detect_threshold'], detect_sign, p['filter'], p['whitening_max_elts'],
                    p['clustering_max_elts'], auto)
        with (output_folder / (file_name + '.params')).open('w') as f:
            f.writelines(circus_config)

        if p['num_workers'] is None:
            p['num_workers'] = np.maximum(1, int(os.cpu_count()))

    def _run(self,  recording, output_folder):
        num_workers = self.params['num_workers']
        cmd = 'spyking-circus {} -c {} '.format(output_folder / 'recording.npy', num_workers)

        if self.debug:
            print(cmd)
        retcode = _run_command_and_print_output(cmd)
        if retcode != 0:
            raise Exception('Spyking circus returned a non-zero exit code')

    @staticmethod
    def get_result_from_folder(output_folder):
        sorting = se.SpykingCircusSortingExtractor(Path(output_folder) / 'recording')
        return sorting
