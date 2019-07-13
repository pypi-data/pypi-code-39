# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os
import pyworkflow.em
from pyworkflow import Config
from pyworkflow.utils import Environ

_logo = "salk_logo.jpg"
_references = ['tan2017']

NYSBC_3DFSC_HOME = 'NYSBC_3DFSC_HOME'
NYSBC_3DFSC_ACTIVATION_CMD = "NYSBC_3DFSC_ACTIVATION_CMD"


class Plugin(pyworkflow.em.Plugin):
    _homeVar = NYSBC_3DFSC_HOME
    _pathVars = [NYSBC_3DFSC_HOME]
    _supportedVersions = ['2.5', '3.0']

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(NYSBC_3DFSC_HOME, 'nysbc3DFSC-2.5')
        cls._defineVar(NYSBC_3DFSC_ACTIVATION_CMD, 'conda activate fsc')

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch 3DFSC. """
        environ = Environ(os.environ)
        environ.update({'PATH': cls.getHome('ThreeDFSC')},
                       position=Environ.BEGIN)

        return environ

    @classmethod
    def getProgram(cls):
        """ Return the program binary that will be used. """
        cmd = cls.getHome('ThreeDFSC', 'ThreeDFSC_Start.py')
        return str(cmd)

    @classmethod
    def getCondaActivationCmd(cls):

        condaActivationCmd = os.environ.get('CONDA_ACTIVATION_CMD', "")
        if not condaActivationCmd:
            print("WARNING!!: CONDA_ACTIVATION_CMD variable not defined. "
                   "Relying on conda being in the PATH")
        elif condaActivationCmd[-1] != ";":
            condaActivationCmd += ";"
        return condaActivationCmd

    @classmethod
    def getNYSBCACtivationCmd(cls):
        cmd = cls.getVar(NYSBC_3DFSC_ACTIVATION_CMD) + ";"
        # If variable comes from the config, scipion appends the scipion home, we should removr it
        cmd = cmd.replace(Config.SCIPION_HOME+"/", "")
        return cmd

    @classmethod
    def defineBinaries(cls, env):
        # try to get CONDA activation command
        condaActivationCmd = cls.getCondaActivationCmd()
        neededProgs = []
        if not condaActivationCmd:
            neededProgs = ['conda']

        fsc_commands = [(condaActivationCmd + './install.sh',
                         'IS_INSTALLED')]

        envPath = os.environ.get('PATH', "")  # keep path since conda likely in there
        installEnvVars = {'PATH': envPath} if envPath else None
        env.addPackage('nysbc3DFSC', version='2.5',
                       tar='nysbc3DFSC-2.5.tgz',
                       commands=fsc_commands,
                       neededProgs=neededProgs,
                       default=True,
                       vars=installEnvVars)

        env.addPackage('nysbc3DFSC', version='3.0',
                       tar='nysbc3DFSC-3.0.tgz',
                       commands=fsc_commands,
                       neededProgs=neededProgs,
                       vars=installEnvVars)


pyworkflow.em.Domain.registerPlugin(__name__)
