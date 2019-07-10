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
import json

import pyworkflow.em as pwem
import pyworkflow.protocol.params as params


class SllProtFilterClasses(pwem.EMProtocol):
    """
    Base class to filter 2D classes and to create "good" and "bad" subsets.
    It can be subclasses to provide specific implementations about how
    the filter is done. This base protocol requires that a good.json file
    is written with the IDs of the good classes and the output will be
    created from there.
     """
    # -------------------------- DEFINE param functions -----------------------
    def _defineParams(self, form):

        form.addSection(label='Input')

        form.addParam('inputClasses', params.PointerParam,
                      pointerClass="SetOfClasses2D",
                      label='Input classes',
                      help='Input classes to filter ')

        form.addParam('createGoodParts', params.BooleanParam,
                      default=False,
                      label='Create subset of good particles?',
                      help='If *Yes*, a subset of particles belonging to the '
                           'classes marked as "good" will be created. ')

    # -------------------------- INSERT steps functions -----------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('convertInputStep')
        self._insertFunctionStep('filterStep')
        self._insertFunctionStep('createOutputStep')

    def convertInputStep(self):
        """ Implement this in subclasses if you need to do some conversion. """
        pass

    def filterStep(self):
        """ Implement this function to filter the input classes and generate
        the good.json file with the IDs of good classes. """
        pass

    def createOutputStep(self):
        goodFn = self._getExtraPath('good.json')

        if not os.path.exists(goodFn):
            raise Exception("File %s was not generated from the 'filterStep'. "
                            "Please check that its ran properly or if its  "
                            "implementation is correct.")

        goodClsIds = json.load(open(goodFn))
        inputClasses = self.inputClasses.get()
        inputParts = inputClasses.getImages()
        outputGoodAvgs = self._createSetOfAverages('_good')
        outputGoodAvgs.copyInfo(inputParts)
        outputBadAvgs = self._createSetOfAverages('_bad')
        outputBadAvgs.copyInfo(inputParts)

        if self.createGoodParts:
            outputParts = self._createSetOfParticles('_good')
            outputParts.copyInfo(inputClasses.getFirstItem())

        for cls in inputClasses:
            classId = cls.getObjId()
            if classId in goodClsIds:
                avgs = outputGoodAvgs
                if self.createGoodParts:
                    outputParts.appendFromImages(cls)
            else:
                avgs = outputBadAvgs
            avgOut = avgs.ITEM_TYPE()
            avgOut.setObjId(classId)
            avgOut.setLocation(cls.getRepresentative().getLocation())
            avgs.append(avgOut)

        self._defineOutputs(outputGoodAverages=outputGoodAvgs)
        self._defineTransformRelation(inputClasses, outputGoodAvgs)
        self._defineOutputs(outputBadAverages=outputBadAvgs)
        self._defineTransformRelation(inputClasses, outputGoodAvgs)
        if self.createGoodParts:
            self._defineOutputs(outputGoodParticles=outputParts)
            self._defineTransformRelation(inputParts, outputParts)
            self._defineTransformRelation(inputClasses, outputParts)

    # -------------------------- INFO functions -------------------------------
    def _summary(self):
        summary = []
        return summary

