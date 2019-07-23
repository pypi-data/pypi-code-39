
# coding: utf-8

# In[ ]:

from array import array
import math as math
import collections

'''Contains 1-D and 2-D Lacing algorithms as translated from John Leavy's FORTRAN programs
1-D Lace ( ~jcl/routines/r8adj.f )
2-D Lace ( ~jcl/routines/exact2w.f )

Code Examples:

1-D Lace :

arrayToLace = array('d', [ 400.0, 500.0, 100.0, 1500.0, 3000.14 ])
target = 10000

answers = Lace.Lace1D( target, arrayToLace, 0, 'This is a test', True )
answers = Lace.Lace1D( target, arrayToLace, 0, 'This is a test' )

print(answers)

2-D Lace :

message = 'I''m lacing for County : 12345!'
numIterations = 25
rowTargets    = array('L', [ 107, 107, 107, 107, 107 ])
columnTargets = array('L', [ 107, 107, 107, 107, 107 ])
twoDArray = [\
             [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
             [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
             [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
             [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
             [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
            ]

answers = Lace.Lace2D( numIterations, columnTargets, rowTargets, twoDArray, message, True )
answers = Lace.Lace2D( numIterations, columnTargets, rowTargets, twoDArray, message )

print(answers)

@author: biecheer
'''

class LaceError(Exception):
   '''Exception raised for errors in the input for Lacing.

    Attributes:
        message -- explanation of the error
   '''

   def __init__(self, message):
      self.message = message

class Lace(object):

   failedLace2DMatrix = None

   '''
   This method is used to lace a one dimensional array of doubles to a target number.
   This was originally written by John Leavy in the UE group in FORTRAN and then
   re-written by Pete Rzonca as a VB module that is utilized in excel. Now I have
   translated that VB code into java code.  And now I'm writing it in Python 3.5.

   ~jcl/routines/r8adj.1.f

   This method also puts out a lot of information in table form to the log file
   at the FINEST level this is done for checking purposes.

   inputs:
      theTarget
      arrayToLace
      numDecimalPlaces
      message
      printInfo
   '''
   @staticmethod
   def Lace1D(theTarget, arrayToLace, numDecimalPlaces, message='', printInfo=False):

      decimalPlaces = math.pow(10, numDecimalPlaces)
      target = math.floor(theTarget * decimalPlaces)

      factor = 1.0

      sumOfSource = math.fsum(arrayToLace)

      if sumOfSource > 0:
         factor = target / sumOfSource
      else:
         print('Error -> The sum of the source data to be laced is zero.')
         return array('d')

      sourceNotRounded  = [ math.floor(element * factor) for element in arrayToLace ]
      sourceNotRounded2 = [ math.floor(element * factor) for element in arrayToLace ]
      sourceRounded = [ math.floor(element * factor + (0.5 * decimalPlaces)) for element in arrayToLace ]
      errors = [ ((element1 * factor) - element2) for element1, element2 in zip( arrayToLace, sourceNotRounded) ]

      sumOfSourceNotRounded = math.fsum(sourceNotRounded)
      sumOfSourceRounded = math.fsum(sourceRounded)

      lacedValues = array('d')
      if sumOfSourceRounded == target:
         lacedValues = [ element / decimalPlaces for element in sourceRounded ]
         if printInfo:
            print('%s' % Lace.build1DLogMessage(message, theTarget, factor / decimalPlaces, numDecimalPlaces,\
                         arrayToLace, sourceRounded, sourceNotRounded, errors, lacedValues, []))
         return lacedValues
      else:
         numberToAdjust = math.floor(target - sumOfSourceNotRounded)
         intPositions = Lace.getNLargestErrors(errors, numberToAdjust)

         for index in intPositions:
            sourceNotRounded2[index] = sourceNotRounded2[index] + 1

         sumOfSourceNotRounded2 = math.fsum( sourceNotRounded2 )
         lacedValues = [ element / decimalPlaces for element in sourceNotRounded2 ]

         if printInfo:
            print('%s' % Lace.build1DLogMessage(message, theTarget, factor / decimalPlaces, numDecimalPlaces,\
                         arrayToLace, sourceRounded, sourceNotRounded, errors, lacedValues, intPositions))

         if sumOfSourceNotRounded2 == target:
            return lacedValues;
         else:
            print('Error -> Can\'t lace this.')
            return array('d')

   '''
      Builds the 1-D Lace log message that will be printed if the printInfo is True
   '''
   @staticmethod
   def build1DLogMessage(message, target, factor, decimalPlaces, arrayToLace, sourceRounded, sourceNotRounded, errors, lacedValues, intPositions):
      s = '\n1-D LACING INFORMATION\n'
      s = s + '\n   ' + message + '\n'
      s = s + '   Target = {0:,} Factor = {1} Decimal Places {2}\n\n'.format(target, factor, decimalPlaces)
      s = s + '                   Source              Source               Source Not\n'
      s = s + '   * Index         Array               Rounded               Rounded             Error               Returning\n'
      s = s + '   - ----- -------------------- -------------------- -------------------- -------------------- --------------------\n'

      for index in range(len(arrayToLace)):
         s = s + '   {0:1} {1:5} {2:20,} {3:20,} {4:20,} {5:20} {6:20,}\n'\
         .format('*' if index in intPositions else ' ', index, arrayToLace[index],\
         sourceRounded[index], sourceNotRounded[index], errors[index], lacedValues[index])

      if len(intPositions) > 0:
         s = s + '\n   * - Indicates the value that had the most error and was rounded.\n\n'
      else:
         s = s + '\n\n'
      return s

   '''
     This method goes through and determines which of the array elements
     to round by checking for the max error.  When found, the position
     in the array is saved and that element will be rounded.

     This is used for the Lace1D routine
   '''
   @staticmethod
   def getNLargestErrors(errors, numberToAdjust):
      members = [0] * len(errors)
      intPositions = [0] * numberToAdjust

      for i in range(numberToAdjust):
         maxError = 0.0
         maxPosition = 0

         for j in range(len(errors)):
            if errors[j] >= 0 and members[j] == 0:
               if errors[j] >= maxError:
                  maxError = errors[j]
                  maxPosition = j

         members[maxPosition] = 1
         intPositions[i] = maxPosition

      return intPositions

   '''
     This method is used to lace a two dimensional (n x m) array of doubles to a
     vector of row targets and column targets  Where n, m &gt;= 2.

     This was originally written by John Leavy in the UE group in FORTRAN.
     The routine uses only a number of iterations to lace not tolerances.

     It laces first to the desired column totals then to the desired row
     totals.  This constitutes one iteration.

     On the last iteration, it laces to the desired row totals by using the
     r8adj.1.f (Lace1D) routine to get an exact, integer-rounded set of
     estimates.  Then it checks the column totals and if they do not sum
     exactly, it tries again starting with the last unrounded laced matrix.
     if the columns are still not exact, the differences are added to the
     largest row to produce the final, exact laced output.

     ORIGINAL SOURCE : ~jcl/routines/exact2w.f

     SIMPLE PSEUDOCODE :

     check for QA stuff on incoming arguments
     firstTime = .true.

     for each iteration
        simpleColumnLace
        if ( .not. lastIteration ) then
           simpleRowLace
        else
           Lace1D ( ~jcl/routines/r8adj.1.f ) on each of the Rows

           add up columns and check for 100% matches
             ( store the column indices and differences where they don't match )

           if( doesn't add up ) then
             if( firstTime ) then
                firstTime = .false.
                numberOfIterations++
                currentIteration = 0
                continue

             else

                ONE LAST DITCH EFFORT TO FORCE THE LACING OF THIS 2D MATRIX

                Rank the row indices in descending order according to the RowTargets.
                ex&gt; if    rowTargets = { 22510, 14210, 16920, 22030, 12570, 20160 };
                    then  rankedRowTargetIndecies = { 0, 3, 5, 2, 1, 4 };
                    this becomes the order of how the program will try to
                    force lace the 2D matrix.

                find the largest ranked row such that for each off column
                the elements in that row when subtracting the difference
                wont produce values &lt; 0.0

                if( row found ) then
                   modify those columns within that row that was previously determined to have
                   the column sum != column target.

                   if( prior value == 0.0 )  print a message to the user

                   for each element in the matrix check to see if all elements are positive

                   if( true ) then
                      return laced matrix
                   else
                      print a message saying that there was a value in the 2D matrix that
                      is negative.
                      2D MATRIX NOT LACED
                   end if
                else
                   print a message saying that the program could not Force lace the matrix
                   since all rows would contain negative values.
                   2D MATRIX NOT LACED
                end if
             end if
           else
             return Laced 2D Array
           end if
        end if
     end for

     @param numberOfIterations
     @param columnTargets
     @param rowTargets
     @param twoDArrayToLace
     @param message
     @return laced2DArray
   '''
   @staticmethod
   def Lace2D( numberOfIterations, columnTargets, rowTargets, twoDArrayToLace, message = '', printInfo = False ):
      Lace.failedLace2DMatrix = None
      logMessage = ''

      Lace.check2DLaceArgs( numberOfIterations, columnTargets, rowTargets, twoDArrayToLace )

      numColumns = len(columnTargets)
      numRows = len(rowTargets)

      firstTime = True
      currentIteration = 1

      # Copy the original 2D Array into a working copy and an empty copy
      prior2DArray =  [ [ 0.0 ] * numColumns for _ in range(numRows) ]
      current2DArray = [ [ twoDArrayToLace[row][col] for col in range(0, numColumns) ] for row in range(0, numRows) ]

      rowFactors = array('d', [0.0] * numRows)
      columnFactors = array('d', [0.0] * numColumns)

      if printInfo:
         logMessage = '\n\n2-D LACING INFORMATION\n'
         logMessage = logMessage + '\t' + message + '\n\n'
         logMessage = Lace.logMatrix( logMessage, 0, firstTime, rowTargets, columnTargets, rowFactors, columnFactors, current2DArray )

      #for currentIteration in range(numberOfIterations):
      while currentIteration <= numberOfIterations:
         Lace.simpleColumnLace( numRows, numColumns, columnTargets, prior2DArray, current2DArray, columnFactors )

         if currentIteration != numberOfIterations:
            Lace.simpleRowLace(numRows, numColumns, rowTargets, current2DArray, rowFactors)

         else:   # On the last iterations
            for row in range(len(current2DArray)):
               newRow = Lace.Lace1D( rowTargets[row], current2DArray[row], 0 )
               for col in range(len(current2DArray[row])):
                  current2DArray[row][col] = newRow[col]

            if printInfo:
               logMessage = Lace.logMatrix( logMessage, currentIteration, firstTime, rowTargets, columnTargets, rowFactors, columnFactors, current2DArray )

            columnSums = [0.0] * numColumns
            differences = dict()
            numberOfColumnsOff = Lace.checkColumnTotals( numColumns, numRows, columnTargets, current2DArray, differences, columnSums )

            if numberOfColumnsOff > 0:

               indexes = list(differences.keys())
               if firstTime:

                  if printInfo:
                     logMessage = logMessage + '\nFIRST TIME :: There were {0} non-0 differences for Columns. They are : \n'.format(len(indexes))
                     for index in range(len(indexes)):
                        logMessage = logMessage + 'Column #{0:02d} Column Sum = {1:15.3f} Target = {2:15d} Diff = {3:5.1f}\n'.\
                        format(indexes[index] + 1, columnSums[indexes[index]], columnTargets[indexes[index]], differences[indexes[index]])

                  firstTime = False

                  #Set the matrix back to the previous iteration before the 1DLace (R8ADJ.f)
                  for row in range(numRows):
                     for col in range(numColumns):
                        current2DArray[row][col] = prior2DArray[row][col]

                  numberOfIterations = numberOfIterations + 1
                  currentIteration = 0 # Set the currentIteration back to zero
                  # Continue on with another loop of n+1 iterations
               else:
                  if printInfo:
                     logMessage = logMessage + '\nSECOND TIME :: There were {0} non-0 differences for Columns. They are : \n'.format(len(indexes))
                     for index in range(len(indexes)):
                        logMessage = logMessage + 'Column #{0:02d} Column Sum = {1:15.3f} Target = {2:15d} Diff = {3:5.1f}\n'.\
                        format(indexes[index] + 1, columnSums[indexes[index]], columnTargets[indexes[index]], differences[indexes[index]])

                  rankRowTargetIndexes = Lace.rankRowTargets(rowTargets)

                  for row in range(numRows):
                     changeRowIndex = rankRowTargetIndexes[row]
                     for currCollOff in range(numberOfColumnsOff):
                        diff = current2DArray[changeRowIndex][indexes[currCollOff]] - differences[indexes[currCollOff]]

                        if diff < 0.0:
                           changeRowIndex = -1
                           break

                     if changeRowIndex != -1:   # Make the forced adjustment
                        for currCollOff in range(numberOfColumnsOff):
                           if current2DArray[changeRowIndex][currCollOff] == 0.0 and printInfo:
                              logMessage = logMessage + '\nCAUTION COLUMN MATRIX[{0:02d}][{1:02d}] WAS PREVIOUSLY ZERIO!!'.format(changeRowIndex + 1, currCollOff + 1)

                           current2DArray[changeRowIndex][indexes[currCollOff]] = current2DArray[changeRowIndex][indexes[currCollOff]] - differences[indexes[currCollOff]]

                        if printInfo:
                           logMessage = logMessage + '\n\nADJUSTMENT MADE IN ROW {0:02d}\n\n'.format(changeRowIndex + 1)

                        # One last check to make sure all values in the matrix are positive!!
                        error = False
                        for row in range(numRows):
                           for col in range(numColumns):
                              if current2DArray[row][col] < 0.0:
                                 if printInfo:
                                    logMessage = logMessage + '\n***** ATTENTION - EMERGENCY NEGATIVE VALUE IN MATRIX FOUND ******\n'
                                    logMessage = logMessage + '\tmatrix[{0:02d][1:02d] = {2}'.format(row+1, col+1, current2DArray[row][col])
                                 error = True

                        if error:
                           if printInfo:
                              print(logMessage)

                           Lace.failedLace2DMatrix = current2DArray
                           if not printInfo:
                              raise LaceError('ERROR: Can''t lace this 2D Array.  Rerun with printInfo = True!')
                           else:
                              raise LaceError('ERROR: Can''t lace this 2D Array.')
                           #raise Exception("ERROR: Rerun with printInfo = True!")

                        if printInfo:
                           logMessage = logMessage + '\n\nFINAL ANSWER!!!!!\n\n'
                           logMessage = Lace.logMatrix( logMessage, currentIteration, firstTime, rowTargets, columnTargets, rowFactors, columnFactors, current2DArray )
                           print(logMessage)

                        return current2DArray

                  if printInfo:
                     logMessage = logMessage + '\n\n***** ATTENTION - NO FINAL COLUMN ADJUSTMENT WAS DONE!'
                     logMessage = logMessage + '\n***** COLUMNS DON''T ADD UP!!\n***** EVERY ROW WOULD GENERATE A NEGATIVE VALUE!'
                     print(logMessage)

                  Lace.failedLace2DMatrix = current2DArray;

                  if not printInfo:
                     raise LaceError('ERROR: Can''t lace this 2D Array.  Rerun with printInfo = True!')
                  else:
                     raise LaceError('ERROR: Can''t lace this 2D Array.')

            else:
               if printInfo:
                  logMessage = logMessage + '\n\nFINAL ANSWER!!!!!\n\n'
                  logMessage = Lace.logMatrix( logMessage, currentIteration, firstTime, rowTargets, columnTargets, rowFactors, columnFactors, current2DArray )
                  print(logMessage)

               return current2DArray

         currentIteration = currentIteration + 1

      if printInfo:
         logMessage = logMessage + '\n\nFINAL ANSWER!!!!!\n\n'
         logMessage = Lace.logMatrix( logMessage, currentIteration, firstTime, rowTargets, columnTargets, rowFactors, columnFactors, current2DArray )
         print(logMessage)

      return current2DArray

   '''
      Builds the 2-D Lace log message that will be printed if the printInfo is True
   '''
   @staticmethod
   def logMatrix( logMessage, currentIteration, firstTime, rowTargets, columnTargets, rowFactors, columnFactors, current2DArray ):

      rowSums = [ math.fsum(current2DArray[row]) for row in range(len(rowTargets)) ]
      colSums = [0] * len(columnTargets)

      for col in range(len(columnFactors)):
         for row in range(len(rowFactors)):
            colSums[ col ] = colSums[ col ] + current2DArray[ row ][ col ]

      totalTarget = sum(rowTargets)

      logMessage = '{0}\nIteration: {1:02} Loop: {2}\n\n'.format( logMessage, currentIteration, 'first' if firstTime else 'second' )
      logMessage = logMessage + '               '

      for col in range(1, len(columnFactors) + 1):
         logMessage = logMessage + '  Column  {0:02}    '.format(col)

      logMessage = logMessage + '    Row Sums      Row Targets      Row Ratios'

      logMessage = logMessage + '\n               '
      for col in range(len(columnFactors) + 3):
         logMessage = logMessage + '--------------- '

      logMessage = logMessage + '\n'

      for row in range(len(rowFactors)):
         logMessage = logMessage + 'Row {0:04}      |'.format(row + 1)
         for col in range(len(columnFactors)):
            logMessage = logMessage + '{0:15.3f} '.format(current2DArray[row][col])
            #if col == len(columnFactors) - 1:
            #   logMessage = logMessage + '   '

         logMessage = logMessage + '{0:15.3f} {1:15d} {2:15.3f}\n'.format(rowSums[row], rowTargets[row], rowFactors[row])

      logMessage = logMessage + '\nCol Sums      |'
      for col in range(len(columnFactors)):
         logMessage = logMessage + '{0:15.3f} '.format(colSums[col])

      logMessage = logMessage + '\nCol Targets   |'
      for col in range(len(columnFactors)):
         logMessage = logMessage + '{0:15d} '.format(columnTargets[col])

      logMessage = logMessage + '{0:31d} '.format(totalTarget)

      logMessage = logMessage + '\nCol Ratios    |'
      for col in range(len(columnFactors)):
         logMessage = logMessage + '{0:15.3f} '.format(columnFactors[col])

      logMessage = logMessage + '\n'
      return logMessage
      #print(logMessage)

   '''
     Method used by the 2DLace to rank the rows in descending order by
     the rowTargets in magnitude.  This will be the order the method
     uses to try to force the matrix to be laced.
   '''
   @staticmethod
   def rankRowTargets( rowTargets ):
      rankedRowTargets = [0] * len(rowTargets)
      d = dict()
      for row in range(len(rowTargets)):
         if rowTargets[row] in d:
            d[rowTargets[row]] = d.get(rowTargets[row], 0) + [row]
         else:
            d[rowTargets[row]] = [row]

      # Sort the dictionary by key in reverse order
      od = collections.OrderedDict(sorted(d.items(), reverse=True))

      r_index = 0
      for value in od.values():
         for num in sorted(value, reverse=True):
            rankedRowTargets[r_index] = num
            r_index = r_index + 1

      return rankedRowTargets




   '''
     Checks the 2D matrix's columns to make sure that they come back to the desired column
     totals.  If not the columns indices, differences and number of columns off is stored
     so that the program and make a one last ditch effort to lace this 2D matrix.
   '''
   @staticmethod
   def checkColumnTotals( numColumns, numRows, columnTargets, current2DArray, differences, columnSums ):

      numberOfColumnsOff = 0
      for col in range(numColumns):
         for row in range(numRows):
            columnSums[ col ] = columnSums[ col ] + current2DArray[ row ][ col ]

         if abs(columnSums[ col ] - columnTargets[ col ]) >= 1.0:
            numberOfColumnsOff = numberOfColumnsOff + 1
            differences[col] = columnSums[ col ] - columnTargets[ col ]

      return numberOfColumnsOff

   '''
     A method used by the 2DLace.

     Simple 1DLace of each row.

     for each row
        sum up current row
        current row factor = current row Target / current row sum
        for each element within this row
           apply the current row factor to the element
        end for
     end for
   '''
   @staticmethod
   def simpleRowLace( numRows, numColumns, rowTargets, current2DArray, rowFactors ):
      rowSums = [0] * numRows

      for row in range(numRows):
         for col in range(numColumns):
            rowSums[row] = rowSums[row] + current2DArray[row][col]

         if rowSums[row] > 0:
            rowFactors[row] = rowTargets[row] / rowSums[row]
            #rowFactors.append( rowTargets[row] / rowSums[row] )
         else:
            rowFactors.append( 0.0 )

         for col in range(numColumns):
            current2DArray[row][col] = current2DArray[row][col] * rowFactors[row]

   '''
     A method used by the 2DLace.  This method also sets the prior 2D Array
     so on the 1st iteration of the 2nd try the program can use the values
     from the 2D matrix prior to the r8adj.1.f ( Lace1D ) routine.

     Simple 1DLace of each column.

     for each column
        sum up current column
        current column factor = current column Target / current column sum
        for each element within this column
           apply the factor
        end for
     end for
   '''
   @staticmethod
   def simpleColumnLace( numRows, numColumns, columnTargets, prior2DArray, current2DArray, columnFactors ):
      columnSums = [0] * numColumns
      #columnFactors = [0.0] * numColumns

      for col in range(numColumns):
         for row in range(numRows):
            columnSums[col] = columnSums[col] + current2DArray[row][col]
            prior2DArray[row][col] = current2DArray[row][col]

         if columnSums[col] > 0:
            columnFactors[col] = columnTargets[col] / columnSums[col]
            #columnFactors.append( columnTargets[col] / columnSums[col] )
         else:
            columnFactors[col] = 0.0
            #columnFactors.append( 0.0 )

         for row in range(numRows):
            current2DArray[row][col] = current2DArray[row][col] * columnFactors[col]

   '''
     This method is a helper method to check the incoming Lace2D arguments.
     A QA thing.
   '''
   @staticmethod
   def check2DLaceArgs( numberOfIterations, columnTargets, rowTargets, twoDArrayToLace ):
      s = ''
      try:
         if numberOfIterations <= 0:
            s = 'Error the number of iterations must be > 0'
            raise

         if len(rowTargets) != len(twoDArrayToLace):
            s = 'Lace2D Error -> The number of rows in the 2D array must be : ' + str(len(rowTargets)) + '!'
            raise

         for row in range(len(twoDArrayToLace)):
            if len(columnTargets) != len(twoDArrayToLace[row]):
               s = 'Lace2D Error -> Each row of the 2-D array must have ' + str(len(columnTargets)) + ' columns in it!'
               raise

         rowSum = sum(rowTargets)
         colSum = sum(columnTargets)
         if rowSum != colSum:
            s = '\nLace2D Error -> The sum of Row Targets: {0:,} must equal to the sum of Column Targets : {1:,}\n'.format(rowSum, colSum)
            raise

      except:
         s = s + '\n   Num Iterations: ' + str(numberOfIterations) + '\n'
         s = s + '   Row Targets   : ' + str(rowTargets) + '\n'
         s = s + '   Col Targets   : ' + str(columnTargets) + '\n'
         s = s + '   To Be Laced   :\n'
         for row in range(len(twoDArrayToLace)):
            s = s + '     ' + str(twoDArrayToLace[row]) + '\n'

         raise Exception(s)

'''
   Used to initially test this code.
'''
if __name__ == "__main__":

   try:
      print('\n------------- Lace 2D Example -------------\n')
      rowTargets    = array('L', [ 107, 107, 107, 107, 107 ])
      #rowTargets    = array('L', [ 107, 107, 107, 107, 106 ])
      #columnTargets = array('L', [ 107, 107, 107, 107 ])
      columnTargets = array('L', [ 107, 107, 107, 107, 107 ])
      #rowTargets    = array('L', [ 107, 107, 107, 107 ])
      #columnTargets = array('L', [ 107, 107, 107, 107 ])
      twoDArray = [\
                   [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
                   [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
                   [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
                   [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
                   [ 10.0, 10.0, 10.0, 10.0, 10.0 ],\
                  ]

      lacedArray = Lace.Lace2D( 25, columnTargets, rowTargets, twoDArray, 'This is a test', False )

      print( 'FINAL MATRIX...')
      for row in range(len(lacedArray)):
         print (lacedArray[row])

      exit()


      rowTargets     = [ 1518, 6018, 456, 450, 733, 391, 332, 4664, 373, 984, 1803, 469, 860, 888, 356, 406, 263, 383, 739, 225, 297, 392 ]
      columnTargets  = [ 152, 57, 0, 9, 6733, 8483, 2758, 1847, 62, 19, 0, 0, 2880 ]
      twoDArray  = [
                    [  266.11, 116.28, 0,        0,  3909.91,  5854.17, 2395.10, 1186.47,   53.89,  46.00, 0, 0, 1352.69 ],\
                    [  963.48, 408.62, 0,    25.28, 18655.20, 30488.99, 2478.21, 1021.86,       0,      0, 0, 0, 6108.87 ],\
                    [       0, 114.09, 0,        0,   677.11,  1012.96,  828.96,  764.71,       0,      0, 0, 0, 1075.98 ],\
                    [   38.88,      0, 0,        0,   606.96,   526.05, 1452.74,  669.73,  159.70,      0, 0, 0, 1046.07 ],\
                    [   47.50,      0, 0,        0,  1122.15,  1644.71, 1958.14, 1307.89,  208.17,      0, 0, 0, 1041.59 ],\
                    [       0,  37.93, 0,        0,   657.39,  1211.87,  551.47,  770.66,  140.92,      0, 0, 0,  540.13 ],\
                    [       0,      0, 0,        0,   379.68,   506.50,  969.97,  285.42,       0,      0, 0, 0, 1178.70 ],\
                    [  764.90, 569.47, 0,        0, 12206.62, 24061.11, 3011.08, 1743.40,   55.97,  70.89, 0, 0, 4157.96 ],\
                    [  134.84,  53.23, 0,        0,   403.03,   794.45,  673.04, 1068.42,   78.26,  50.95, 0, 0,  474.12 ],\
                    [  309.37,  104.4, 0,        0,  1338.24,  2065.12, 1741.88, 1719.64,  313.01,  81.38, 0, 0, 2168.05 ],\
                    [  146.58,      0, 0,     36.6,  3850.67,  7700.25, 1975.01, 1763.87,  172.19, 158.48, 0, 0, 2227.07 ],\
                    [       0,  80.53, 0,        0,   738.39,  1748.95,  474.25,  908.83,  105.81,  63.97, 0, 0,  569.41 ],\
                    [   58.05,  39.04, 0,        0,   707.44,  1510.68, 2338.77, 1710.45,  121.60, 118.94, 0, 0, 1995.54 ],\
                    [  346.14,      0, 0,        0,  2911.31,  1443.62, 1305.89, 1317.88,  128.05,  27.35, 0, 0, 1399.93 ],\
                    [  221.79,      0, 0,        0,   952.44,  1565.23,  325.28,   62.26,       0,      0, 0, 0,  433.43 ],\
                    [       0,      0, 0,        0,   257.53,  1528.18,  785.37, 1170.05,       0,      0, 0, 0,  319.12 ],\
                    [  102.49,      0, 0,        0,       46,   599.72, 1184.58,  555.09,       0,      0, 0, 0,  141.97 ],\
                    [       0,      0, 0,        0,   647.73,   294.91, 1572.37,  435.51,  171.09,      0, 0, 0,  708.40 ],\
                    [  402.98,  90.53, 0,        0,  1560.03,  1634.22, 1464.18, 1086.63,  121.12,      0, 0, 0, 1030.54 ],\
                    [  135.52,      0, 0,        0,        0,   623.72,  480.67,  702.94,       0,      0, 0, 0,  307.42 ],\
                    [       0,  49.06, 0,        0,   369.47,   349.06,  778.91,  502.97,       0,      0, 0, 0,  920.82 ],\
                    [  139.98,      0, 0,        0,  1098.54,   987.25,  697.80,  658.72,   64.80,      0, 0, 0,  273.18 ]\
                   ]

      lacedArray = Lace.Lace2D( 25, columnTargets, rowTargets, twoDArray, 'Unit Test: 5', True )

      print( 'FINAL MATRIX...')
      for row in range(len(lacedArray)):
         print (lacedArray[row])
   except LaceError as ex1:
      print(ex1)
      badArray = Lace.failedLace2DMatrix
      print( 'FINAL BAD MATRIX 1...')
      for row in range(len(badArray)):
         print (badArray[row])
   except Exception as ex2:
      print(ex2)
      print( 'FINAL BAD MATRIX 2...')
      badArray = Lace.failedLace2DMatrix
      for row in range(len(badArray)):
         print (badArray[row])

   exit()