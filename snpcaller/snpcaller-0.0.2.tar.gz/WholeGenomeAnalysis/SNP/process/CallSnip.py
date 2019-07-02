def getSnipPosition(bam,jsondata):
    for sequence in bam:
        if (hasattr(sequence, 'reference_name')):
            print(sequence.reference_name)
            for snp in jsondata['SNP']:
                if(snp['chrom'] == sequence.reference_name):
                    print


    for sequence in bam:
        if (hasattr(sequence, 'reference_name')):
            start=sequence.pos
            end=sequence.pos+len(sequence.seq)
            for snp in data['SNP']:
                if(snp['chrom'] == sequence.reference_name):
                    chromStart=snp['chromStart']
                    chromEnd=snp['chromEnd']
                    if(start < chromStart <  end and start < chromEnd < end):
                        AmpliconName=sequence.query_name.split('#')[2]
                        rawReads = sequence.query_name.split('#')[4]
                        targetPositionStart=chromStart-start
                        targetPositionEnd=chromEnd-start

                        rawbases=sequence.seq[targetPositionStart:targetPositionEnd]
                        print(BlotName+','+SampleName+','+AmpliconName+','+rawReads+','+snp['name']+','+snp['chrom']+','+str(chromStart)+','+str(chromEnd)+','+snp['refNCBI']+','+snp['refUCSC']+','+snp['observed']+','+rawbases)

def CigarCalculation(targetPositionStart, targetPositionEnd, cigar):
    calPositionStart = targetPositionStart
    returnStart = targetPositionStart
    returnEnd = targetPositionEnd

    # Cigar value 0 is mutation, 1 is Insertion , 2 is Deletion.
    for arrCigar in cigar:
        mutationType=arrCigar[0]
        value=arrCigar[1]

        if(value < calPositionStart):
            if(mutationType==0):
                calPositionStart=calPositionStart-value
            elif(mutationType==1):
                returnStart = targetPositionStart + value
                returnEnd = targetPositionEnd + value
                calPositionStart = targetPositionStart + value
            elif(mutationType==2):
                returnStart=targetPositionStart-value
                returnEnd=targetPositionEnd-value
                calPositionStart=targetPositionStart-value
        else:
            return returnStart,returnEnd

    return returnStart, returnEnd
