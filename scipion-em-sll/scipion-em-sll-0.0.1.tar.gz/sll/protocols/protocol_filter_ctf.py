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

import pyworkflow.em as pwem
import pyworkflow.protocol.params as params


class SllProtFilterCtf(pwem.ProtCTFMicrographs):
    """ Base class for protocols that will filter micrograph based on
     the CTF estimation parameters. It should classify input micrographs
     in "good/bad" subsets.
     """

    def __init__(self, **kwargs):
        pwem.ProtCTFMicrographs.__init__(self, **kwargs)
        self.stepsExecutionMode = params.STEPS_PARALLEL

    # -------------------------- DEFINE param functions -----------------------
    def _defineParams(self, form):
        form.addSection(label='Input')
        form.addParam('inputCTF', params.PointerParam,
                      pointerClass="SetOfCTF",
                      label='Input CTF',
                      help='Select set of CTF that you want to export.')

    # -------------------------- INSERT steps functions -----------------------
    def _filterCTF(self, ctf):
        """ Return True if we want to keep this micrograph in the output.
        If False, it will go to the rejected set.
        """
        pass

    def createOutputStep(self):
        inputCTF = self.inputCTF.get()
        micSet = inputCTF.getMicrographs()

        def _createCTF(suffix=''):
            ctf = self._createSetOfCTF(suffix)
            ctf.copyInfo(inputCTF)
            mics = self._createSetOfMicrographs(suffix)
            mics.copyInfo(micSet)

            return ctf, mics

        outCTF, outMics = _createCTF()
        rejCTF, rejMics = _createCTF('_rejected')

        for ctf in inputCTF:
            if self._filterCTF(ctf):
                outCTF.append(ctf)
                outMics.append(ctf.getMicrograph())
            else:
                rejCTF.append(ctf)
                rejMics.append(ctf.getMicrograph())

        def _defineOutput(prefix, ctf, mics):
            self._defineOutputs(**{prefix+'Micrographs': mics})
            ctf.setMicrographs(mics)
            self._defineOutputs(**{prefix + 'CTF': ctf})
            self._defineTransformRelation(self.inputCTF, ctf)
            self._defineTransformRelation(micSet, mics)
            self._defineCtfRelation(mics, ctf)

        _defineOutput('output', outCTF, outMics)
        _defineOutput('rejected', rejCTF, rejMics)

    # -------------------------- INFO functions -------------------------------

    def _summary(self):
        summary = []
        return summary

    # -------------------------- UTILS functions ------------------------------

