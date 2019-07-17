import logging
import os
import unittest
import csv
from .context import drcompare
from drcompare import drcompare_main


class TestDrCompare(unittest.TestCase):
    def setUp(self):
        currentDir = os.getcwd()
        self.inputDirPath = currentDir + '/images/'
        self.inputTestFileMap = {
            'WITH_VAILD_PATHS':'images.csv', 
            'WITH_INVAILD_PATHS':'images.csveee', 
            'WITH_SAME_IMAGES':'images_same.csv',
            'WITH_COMPLETELY_DIFFERENT_IMAGES':'images_different.csv',
            'WITH_SIMILAR_IMAGES':'images_similar.csv',
            'WITH_MISSING_PATHS':'images_missing_path.csv', 
            'WITH_NON_UNIFORM_IMAGE_SIZES':'images_uneven_size.csv',
            'WITH_NON_IMAGE_PATHS':'images_with_txt_paths.csv'}
        self.outputFilePath = self.inputDirPath + '/output.csv'

    
    def test_numberOfRowsinInputAndOutputfiles(self):
        inputFileName = self.inputDirPath + self.inputTestFileMap["WITH_VAILD_PATHS"]
        drcompare_main(inputFileName, self.inputDirPath)
        self.assertEqual(self.countRows(inputFileName), self.countRows(self.outputFilePath), 
        "The number of rows in output file are different from inputfile.")
    
    def test_invalidInputfileShouldHandleGracefully(self):
        inputFileName = self.inputDirPath + self.inputTestFileMap["WITH_INVAILD_PATHS"]
        ret = drcompare_main(inputFileName, self.inputDirPath)
        self.assertEqual(ret, None)

    def test_sameImagesShouldReturnValidOutputFile(self):
        inputFileName = self.inputDirPath + self.inputTestFileMap["WITH_SAME_IMAGES"]
        drcompare_main(inputFileName, self.inputDirPath)
        rows = self.readRows(self.outputFilePath)
        self.assertTrue(rows, "should contain non-empty result in output file") # non-empty result
        self.assertEqual(rows[0]['similar'], '0')
        self.assertTrue(rows[0]['elapsed'])

    def test_differentImagesShouldReturnValidOutputFile(self):
        inputFileName = self.inputDirPath + self.inputTestFileMap["WITH_COMPLETELY_DIFFERENT_IMAGES"]
        drcompare_main(inputFileName, self.inputDirPath)
        rows = self.readRows(self.outputFilePath)
        self.assertTrue(rows, "should contain non-empty result in output file") # non-empty result
        self.assertGreater(float(rows[0]['similar']), 0)
        self.assertTrue(rows[0]['elapsed'])
    
    def test_similarImagesShouldReturnValidOutputFile(self):
        inputFileName = self.inputDirPath + self.inputTestFileMap["WITH_SIMILAR_IMAGES"]
        drcompare_main(inputFileName, self.inputDirPath)
        rows = self.readRows(self.outputFilePath)
        self.assertTrue(rows, "should contain non-empty result in output file") # non-empty result
        self.assertNotEqual(float(rows[0]['similar']), 0)
        self.assertTrue(rows[0]['elapsed'])
    
    def test_missingImagesPathShouldReturnValidOutputFile(self):
        inputFileName = self.inputDirPath + self.inputTestFileMap["WITH_MISSING_PATHS"]
        drcompare_main(inputFileName, self.inputDirPath)
        rows = self.readRows(self.outputFilePath)
        self.assertTrue(rows, "should contain non-empty result in output file") # non-empty result
        self.assertEqual(float(rows[0]['similar']), -1.0)
        self.assertTrue(rows[0]['elapsed'])
    
    def test_differentSizedImagesShouldReturnValidOutputFile(self):
        inputFileName = self.inputDirPath + self.inputTestFileMap["WITH_NON_UNIFORM_IMAGE_SIZES"]
        drcompare_main(inputFileName, self.inputDirPath)
        rows = self.readRows(self.outputFilePath)
        self.assertTrue(rows, "should contain non-empty result in output file") # non-empty result
        self.assertEqual(float(rows[0]['similar']), 1.0)
        self.assertTrue(rows[0]['elapsed'])
    
    def test_nonImagesPathShouldReturnValidOutputFile(self):
        inputFileName = self.inputDirPath + self.inputTestFileMap["WITH_NON_IMAGE_PATHS"]
        drcompare_main(inputFileName, self.inputDirPath)
        rows = self.readRows(self.outputFilePath)
        self.assertTrue(rows, "should contain non-empty result in output file") # non-empty result
        self.assertEqual(float(rows[0]['similar']), -1.0)
        self.assertTrue(rows[0]['elapsed'])

    # Helper methods
    def countRows(self,filename):
        with open(filename) as f:
            return sum(1 for line in f)
    
    def readRows(self,filename):
        rows = []
        with open(filename) as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader]
        return rows
