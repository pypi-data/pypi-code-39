
import matplotlib.pyplot as plt

from workspace_jam.plotting.requirements import parallel_x2_requirements
from workspace_jam.plotting.requirements import parallel_x3_requirements
from workspace_jam.plotting.requirements import serial_x2_requirements
from workspace_jam.plotting.requirements import serial_x3_requirements

import os

# Setup the path to the workspace, using a relative directory name.
workspace_path = '{}/../../'.format(os.path.dirname(os.path.realpath(__file__)))
plot_path = '{}/plotting/requirements/plots/'.format(workspace_path)
output_path = workspace_path + '../../outputs/PyAutoCTI/'

ci_resolutions = ['low_resolution', 'mid_resolution', 'high_resolution']

requirement_means_parallel_x2, requirement_errors_parallel_x2 = \
    parallel_x2_requirements.parallel_x2_requirements_of_resolutions(ci_resolutions=ci_resolutions)

requirement_means_serial_x2, requirement_errors_serial_x2 = \
    serial_x2_requirements.serial_x2_requirements_of_resolutions(ci_resolutions=ci_resolutions)

requirement_means_parallel_x3, requirement_errors_parallel_x3 = \
    parallel_x3_requirements.parallel_x3_requirements_of_resolutions(ci_resolutions=ci_resolutions)

requirement_means_serial_x3, requirement_errors_serial_x3 = \
    serial_x3_requirements.serial_x3_requirements_of_resolutions(ci_resolutions=ci_resolutions)

columns = [517, 1034, 2068]#, 4136]

jitters = [-30.0, -10.0, 10.0, 30.0]

plt.figure(figsize=(20, 15))
plt.suptitle('Requirements for CTI Models', fontsize=40)
plt.tick_params(labelsize=16)

columns_plot = list(map(lambda column : column + jitters[0], columns))

eb0 = plt.errorbar(x=columns_plot, y=requirement_means_parallel_x2,
                  yerr=[requirement_errors_parallel_x2, requirement_errors_parallel_x2],
                  capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
eb0[-1][0].set_linestyle(':')

columns_plot = list(map(lambda column : column + jitters[1], columns))

eb1 = plt.errorbar(x=columns_plot, y=requirement_means_serial_x2,
                  yerr=[requirement_errors_serial_x2, requirement_errors_serial_x2],
                capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
eb1[-1][0].set_linestyle(':')

columns_plot = list(map(lambda column : column + jitters[2], columns))

eb2 = plt.errorbar(x=columns_plot, y=requirement_means_parallel_x3,
                  yerr=[requirement_errors_parallel_x3, requirement_errors_parallel_x3],
                  capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
eb2[-1][0].set_linestyle(':')

columns_plot = [min(columns) + jitters[3], 1034]# , 2068]  # , 4136]

columns_plot = list(map(lambda column : column + jitters[3], columns))

eb3 = plt.errorbar(x=columns_plot, y=requirement_means_serial_x3,
                  yerr=[requirement_errors_serial_x3, requirement_errors_serial_x3],
                  capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
eb3[-1][0].set_linestyle(':')

columns = [517-30, 1034, 2068+30]#, 4136]

plt.plot(columns, len(columns) * [1.1e-4], linestyle='-', color='r')
plt.plot(columns, len(columns) * [-1.1e-4], linestyle='-', color='r')

plt.legend(handles=[eb0, eb1, eb2, eb3], labels=['Parallel x2', 'Serial x2', 'Parallel x3', 'Serial x3'], loc='northeast', fontsize=25)
plt.xlabel('Number of columns / rows', fontsize=18)
plt.ylabel(r'$\Delta e_{\rm 1}$', fontsize=18)

plt.savefig(plot_path + '/requirements.png')
plt.show()