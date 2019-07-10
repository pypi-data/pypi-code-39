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

import os

import pyworkflow.tests as pwtests
from pyworkflow.tests.em.workflows import TestWorkflow
from pyworkflow.utils import importFromPlugin
import pyworkflow.em as pwem

import sll
import sll.protocols


CPUS = os.environ.get('SCIPION_TEST_CPUS', 4)
GPUS = os.environ.get('SCIPION_TEST_GPUS', 2)


class TestSllFilterClassesCC(TestWorkflow):
    @classmethod
    def setUpClass(cls):
        pwtests.setupTestProject(cls)
        cls.ds = pwtests.DataSet.getDataSet('relion30_tutorial')

    # Validate outputs
    def _checkOutput(self, prot, name, size):
        output = getattr(prot, name, None)
        self.assertIsNotNone(output, "Missing expected output: %s" % name)
        self.assertEqual(output.getSize(), size)

    def _importParticles(self):
        starFn = os.path.join('20190709_scipion_relion30', 'Runs',
                              '001774_ProtRelionClassify2D', 'extra',
                              'relion_it015_data.star')
        protImport = self.newProtocol(
            pwem.ProtImportParticles,
            importFrom=3,  # From Relion
            starFile=self.ds.getFile(starFn),
            samplingRateMode=0,
            samplingRate=3.54,
            magnification=50000,
            scannedPixelSize=7.0,
            voltage=200,
            sphericalAberration=1.4,
        )
        protImport.setObjLabel('import particles from 2D')
        protImport = self.launchProtocol(protImport)

        # Validate outputs
        self._checkOutput(protImport, 'outputParticles', 5552)
        self._checkOutput(protImport, 'outputClasses', 50)
        self._checkOutput(protImport, 'outputMicrographs', 24)

        return protImport

    def _importAverages(self):
        avgsFn = os.path.join('20190709_scipion_relion30', 'Runs',
                              '002060_ProtRelionCenterAverages',
                              'centered_averages.mrcs')
        protAvgs = self.newProtocol(
            pwem.ProtImportAverages,
            importFrom=0,  # From files
            filesPath=self.ds.getFile(avgsFn),
            samplingRateMode=0,
            samplingRate=3.54,
            magnification=50000,
            scannedPixelSize=7.0,
            voltage=200,
            sphericalAberration=1.4,
        )
        protAvgs.setObjLabel('import avgs')
        protAvgs = self.launchProtocol(protAvgs)
        self._checkOutput(protAvgs, 'outputAverages', 14)

        return protAvgs

    def _runFilterClasses(self, protImport, protAvgs):
        protFilter = self.newProtocol(
            sll.protocols.SllProtFilterClassesCC,
            createGoodParts=True,  # Create good particles subset
        )

        protFilter.inputClasses.set(protImport.outputClasses)
        protFilter.inputAverages.set(protAvgs.outputAverages)
        protFilter = self.launchProtocol(protFilter)

        self._checkOutput(protFilter, 'outputGoodAverages', 15)
        self._checkOutput(protFilter, 'outputBadAverages', 35)

    def test_workflow(self):
        protImport = self._importParticles()
        protAvgs = self._importAverages()
        protFilter = self._runFilterClasses(protImport, protAvgs)


if __name__ == '__main__':
    import unittest
    unittest.main()
