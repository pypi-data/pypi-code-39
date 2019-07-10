# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *
# * [1] SciLifeLab, Stockholm University
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

import pyworkflow.protocol.params as params

from .protocol_filter_ctf import SllProtFilterCtf


class SllProtFilterCtfThreshold(SllProtFilterCtf):
    """
    Select "good/bad" micrographs based on the input CTF parameters.
    """
    _label = 'filter ctf'

    def _defineParams(self, form):
        SllProtFilterCtf._defineParams(self, form)

        form.addParam('useDefocus', params.BooleanParam, default=True,
                      label='Use Defocus for selection',
                      help='Use this button to decide if carry out the '
                           'selection taking into account or not the defocus '
                           'values.')

        line = form.addLine('Defocus (A)', condition="useDefocus",
                            help='Minimum and maximum values for defocus in '
                                 'Angstroms')
        line.addParam('minDefocus', params.FloatParam, default=4000,
                      label='Min')
        line.addParam('maxDefocus', params.FloatParam,
                      default=40000, label='Max')

        form.addParam('maxAstigmatism', params.FloatParam, default=0,
                      label='Max astigmatism (A)',
                      help='Maximum value allowed for astigmatism '
                           '(abs(defocusU - defocusV) in Angstroms)'
                           'If a given CTF does not fulfill '
                           'this requirement, it will be discarded. \n\n'
                           '*Note:* Use *0* to not check astigmatism. ')
        form.addParam('minResolution', params.FloatParam, default=0,
                      label='Min resolution (A)',
                      help='Minimum value for resolution in Angstroms. '
                           'If the evaluated CTF does not fulfill this '
                           'requirement, it will be discarded.\n\n'
                           '*Note:* Use *0* to not check astigmatism. ')

        form.addParallelSection(threads=1, mpi=1)

    # --------------------------- INSERT steps functions ----------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('createOutputStep')

    def _filterCTF(self, ctf):
        """ Return True if we want to keep this micrograph in the output.
        If False, it will go to the rejected set.
        """
        if self.useDefocus:
            minD = self.minDefocus.get()
            maxD = self.maxDefocus.get()
            dU, dV, _ = ctf.getDefocus()
            self.info("Using defocus: min: %f, max %f, values: dU %f dV %f" % (minD, maxD, dU, dV))
            if not (minD <= dU <= maxD and minD <= dV <= maxD):
                return False

        minResolution = self.minResolution.get()
        if minResolution > 0 and ctf.getResolution() > minResolution:
            return False

        return True

    def _stepsCheck(self):
        pass
