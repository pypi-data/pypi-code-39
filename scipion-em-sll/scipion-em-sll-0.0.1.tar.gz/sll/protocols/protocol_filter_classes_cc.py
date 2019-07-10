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

import numpy as np
import json
from collections import OrderedDict

import pyworkflow as pw
import pyworkflow.protocol.params as params

from .protocol_filter_classes import SllProtFilterClasses


class SllProtFilterClassesCC(SllProtFilterClasses):
    """
    Simple protocol to filter classes based on cross-correlation and
    the number of particles assigned to each class. Usually, "good" classes
    contains most of the particles. So, first a group of possible good classes
    are selected and then we check how good they correlate among then.

    Alternatively, input reference can be provided. In that case, it will
    be take for the cross-correlation checks.
    """

    _label = 'filter classes cc'

    # -------------------------- DEFINE param functions -----------------------
    def _defineParams(self, form):
        SllProtFilterClasses._defineParams(self, form)
        form.addParam('inputAverages', params.PointerParam,
                      pointerClass="SetOfAverages",
                      allowsNull=True,
                      label='Input references',
                      help='If you provide some 2D averages as references, '
                           'it will be used for the cross-correlation check'
                           'if what are "good" classes from the input. ')

    # -------------------------- INSERT steps functions -----------------------
    def filterStep(self):
        if self.inputAverages.get() is None:
            goodClsIds = self._filter()
        else:
            goodClsIds = self._filterWithReferences()

        json.dump(goodClsIds, open(self._getExtraPath('good.json'), 'w'))

    def _filterWithReferences(self):
        ih = pw.em.ImageHandler()
        inputClasses = self.inputClasses.get()
        inputParts = inputClasses.getImages()
        inputAvgs = self.inputAverages.get()
        n = 1. / inputParts.getSize()

        goodCount = 0
        badCount = 0
        goodFn = self._getExtraPath('good.mrcs')
        badFn = self._getExtraPath('bad.mrcs')

        avgsList = [ih.read(img) for img in inputAvgs]
        goodClsIds = []

        for cls in inputClasses:
            percent = cls.getSize() * n
            if percent < 0.01:
                continue
            m = self.computeCorrelation([ih.read(cls.getRepresentative())],
                                        avgsList)
            if np.max(m) > 0.95:
                goodCount += 1
                loc = (goodCount, goodFn)
                goodClsIds.append(cls.getObjId())
            else:
                badCount += 1
                loc = (badCount, badFn)
            ih.write(ih.read(cls.getRepresentative()), loc)

        return goodClsIds

    def _filter(self):
        inputClasses = self.inputClasses.get()
        inputParts = inputClasses.getImages()

        ih = pw.em.ImageHandler()
        n = 1. / inputParts.getSize()
        # Initially, let's make to groups, where a class is considered
        # "bad" if it contains less that 1% of the data
        clsList = OrderedDict()

        for cls in inputClasses:
            percent = cls.getSize() * n
            if percent > 0.01:  # Only consider classes with at least 1%
                clsList[cls.getObjId()] = {
                    'size': cls.getSize(),
                    'percent': percent,
                    'image': ih.read(cls.getRepresentative())
                }
        corrMat = self.computeSelfCorrelation([d['image'] for d in clsList.values()])
        goodIndexes = []
        badIndexes = []

        for i, clsDict in enumerate(clsList.values()):
            s = np.sort(corrMat[i])
            m = s[-1]
            self.info("max: %0.4f,   %s"
                      % (m, ['%0.4f' % v for v in s]))
            if m < 0.94 and clsDict['size'] < 100:  # rule of thumb here
                badIndexes.append(i)
            else:
                goodIndexes.append(i)

        self.info("Second round to rescue 'bad'")
        goodIndexes2 = []
        for i, b in enumerate(badIndexes):
            bCorr = corrMat[b]
            s = np.sort([bCorr[g] for g in goodIndexes])
            m = s[-1]
            clsDict = clsList.values()[b]
            p = clsDict['percent']
            # Let's rescue some classes from the "bad" group
            # taking into account the correlation with the averages
            # of the "good" group and also the percentage of data
            self.info("max: %0.4f, percent: %0.4f,  %s"
                      % (m, p, ['%0.4f' % v for v in s]))
            if m > 0.9 or (m > 0.85 and p > 0.02):
                goodIndexes2.append(b)
            ih.write(clsDict['image'], (i, self._getExtraPath('rescue.mrcs')))

        goodIndexes.extend(goodIndexes2)
        for i, clsDict in enumerate(clsList.values()):
            clsDict['good'] = i in goodIndexes

        goodCount = 0
        badCount = 0
        goodFn = self._getExtraPath('good.mrcs')
        badFn = self._getExtraPath('bad.mrcs')
        goodClsIds = []

        for cls in inputClasses:
            clsId = cls.getObjId()

            if clsId in clsList and clsList[clsId]['good']:
                goodCount += 1
                loc = (goodCount, goodFn)
                goodClsIds.append(cls.getObjId())
            else:
                badCount += 1
                loc = (badCount, badFn)
            ih.write(ih.read(cls.getRepresentative()), loc)

        return goodClsIds

    # -------------------------- INFO functions -------------------------------

    def _summary(self):
        summary = []
        return summary

    # -------------------------- UTILS functions ------------------------------
    def _correlate(self, img1, img2):
        import xmippLib  # FIXME: Remove dependency
        imgAligned = xmippLib.image_align(img1, img2)
        return img1.correlation(imgAligned)

    def computeSelfCorrelation(self, imgList):
        """ Compute the correlation matrix among all classes in imgPath. """
        n = len(imgList)
        corrMat = np.zeros((n, n))

        for i, img in enumerate(imgList):
            for j, img2 in enumerate(imgList):
                if j < i:
                    corrMat[i, j] = corrMat[j, i]
                elif j > i:
                    corrMat[i, j] = self._correlate(img, imgList[j])
        return corrMat

    def computeCorrelation(self, imgList1, imgList2):
        n = len(imgList1)
        m = len(imgList2)
        corrMat = np.zeros((n, m))

        for i, img1 in enumerate(imgList1):
            for j, img2 in enumerate(imgList2):
                corrMat[i, j] = self._correlate(img1, img2)

        return corrMat
