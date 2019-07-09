import bamnostic as bs
import argparse
import os.path
import json
import csv

from WholeGenomeAnalysis.SNP.model.AutoTypingResult import AutoTypingResult
from WholeGenomeAnalysis.SNP.model.Sample import Sample
from WholeGenomeAnalysis.SNP.model.Amplicon import Amplicon
from WholeGenomeAnalysis.SNP.process import CallSnip as callsnip
from WholeGenomeAnalysis.SNP.process import QualityCalculation as qualityCalculation
from WholeGenomeAnalysis.SNP.reader import reader as reader

parser = argparse.ArgumentParser(description='Input for Snip program')

parser.add_argument("-s", "--snpJsonpath", help='input snp json file path', required=True, dest="snpJsonpath")
parser.add_argument("-j", "--jsonpath", help='input json file path (output json from the sample processor program', required=True, dest="jsonPath")
parser.add_argument("-b", "--bampath", help='input bam file path', required=True, dest="bamPath")
parser.add_argument("-o", "--outfolder",help='output folder location', required=True, dest="outfolder")

args = parser.parse_args()

if (os.path.exists(args.snpJsonpath)):
    print("File exist : " + args.snpJsonpath)
else:
    print("Missing json file : " + args.snpJsonpath)
    exit()

if (os.path.exists(args.bamPath)):
    print("File exist : " + args.bamPath)
else:
    print("Missing bam file : " + args.bamPath)
    exit()

if (os.path.exists(args.jsonPath)):
    print("File exist : " + args.jsonPath)
else:
    print("Missing bam json : " + args.jsonPath)
    exit()

if (os.path.exists(args.outfolder)):
    print("Folder exist : " + args.outfolder)
else:
    print("Created path : " + args.outfolder)
    os.mkdir(args.outfolder)


snpJsonpath = args.snpJsonpath
bamPath = args.bamPath
jsonpath = args.jsonPath

snpData = reader.JsonReader(snpJsonpath)
qualityData = reader.JsonReader(jsonpath)
bam = bs.AlignmentFile(bamPath, 'rb')

# copiedbam = copy.copy(bam)

# for snp in data['SNP']:
#     print('name : ' + snp['name'])

snpVersion = snpData['SNPVERSION']
targetSnpVersion = snpData['VERSION']
experimentID = qualityData['ExperimentID']
experimentName = qualityData['ExperimentName']
plateName = qualityData['PlateName']
sampleId = qualityData['SampleID']


# Create output path

outputpath = args.outfolder+'/'+sampleId+'.csv'
#print("output path : " +outputpath)
#outputfile = writer.csvWriter(outputpath)


# sorted_bam = sorted(bam.head(), key=operator.itemgetter(1), reverse=True)

# for reading in enumerate(bamtmp):
#     print(reading)
# Result = {}
# AmpliconList = {}

# for sequence in copiedbam:
#     if (hasattr(sequence, 'reference_name')):
#         if sequence.query_name.startswith('SNP'):
#             AmpliconName = sequence.query_name.split('#')[2]
#             AmpliconList[AmpliconName] = Amplicon(AmpliconName)

autoResult = AutoTypingResult(snpVersion, targetSnpVersion)
smpl = Sample(experimentID, experimentName, plateName, sampleId)

with open(outputpath, mode='w', newline='') as csv_file:
    fieldnames = ['experimentName', 'sampleId', 'seqName', 'rawReads', 'snpName', 'chrom', 'chromStart', 'chromEnd',
                  'refNCBI', 'refUCSC', 'targeted', 'observed', 'minBaseOcurrances', 'minBasePercentages',
                  'minBaseQualityPercentage']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for sequence in bam:
        if (hasattr(sequence, 'reference_name')):
            if sequence.query_name.startswith('SNP'):
                start = sequence.pos
                end = sequence.pos + len(sequence.seq)
                isTargeted = False
                # print("1. reference_name: " + sequence.reference_name + " | 1. sequence.query_name: " + sequence.query_name)
                # print("1. sequence.read_name: " + sequence.read_name)
                # dt = {}
                print("Name : " + sequence.query_name)
                AmpliconName = sequence.query_name.split('#')[2]
                amp = Amplicon(AmpliconName)

                for snip in snpData['SNP']:
                    if (snip['chrom'] == sequence.reference_name):

                        # print("2. reference_name: " + sequence.reference_name)v
                        # print("2. sequence.query_name: " + sequence.query_name)

                        chromStart = snip['chromStart']
                        chromEnd = snip['chromEnd']

                        if (start < chromStart < end and start < chromEnd < end):
                            # print("1. reference_name: " + sequence.reference_name + " | 1. sequence.query_name: " + sequence.query_name)

                            # AmpliconName = sequence.query_name.split('#')[2]
                            rawReads = sequence.query_name.split('#')[4]
                            targetPositionStart = chromStart - start
                            targetPositionEnd = chromEnd - start
                            print("targetPositionStart : " + str(targetPositionStart) + " | targetPositionEnd: " + str(targetPositionEnd))
                            calStart, calend = callsnip.CigarCalculation(targetPositionStart, targetPositionEnd, sequence.cigar)
                            print("start : " + str(calStart) + " | end: " + str(calend))
                            rawbases = sequence.seq[calStart:calend]

                            if(calStart==calend and rawbases==''):
                                rawbases='-'

                            minBaseOcurrances, minBasePercentages, minBaseQualityPercentage = qualityCalculation.getQuality(qualityData, rawbases, calStart, calend, sequence.query_name)
                            #rawbases = sequence.seq[targetPositionStart:targetPositionEnd]

                            #snps = Snp(1, sequence.query_name, rawReads, snip['name'], snip['chrom'], chromStart, chromEnd,
                            #           snip['refNCBI'], snip['refUCSC'], snip['observed'], rawbases, minBaseOcurrances, minBasePercentages, minBaseQualityPercentage, sequence)

                            # dt.update(vars(snps))
                            # dt = json.dumps(dt)

                            #amp.add(snps)
                            writer.writerow({'experimentName': experimentName, 'sampleId': sampleId, 'seqName': sequence.query_name, 'rawReads': rawReads, 'snpName': snip['name'], 'chrom': snip['chrom'], 'chromStart': str(chromStart), 'chromEnd': str(chromEnd), 'refNCBI': snip['refNCBI'], 'refUCSC': snip['refUCSC'], 'targeted': snip['observed'], 'observed': rawbases, 'minBaseOcurrances': str(minBaseOcurrances), 'minBasePercentages': str(minBasePercentages), 'minBaseQualityPercentage': str(minBaseQualityPercentage)})

                            print(experimentName + ',' + sampleId + ',' + sequence.query_name + ',' + rawReads + ',' + snip[
                                'name'] + ',' + snip['chrom'] + ',' + str(chromStart) + ',' + str(chromEnd) + ',' + snip[
                                      'refNCBI'] + ',' + snip['refUCSC'] + ',' + snip['observed'] + ',' + rawbases  + ',' + str(minBaseOcurrances) + ',' + str(minBasePercentages) + ',' + str(minBaseQualityPercentage))
                            isTargeted = True
                            break

                # AmpliconName = sequence.query_name.split('#')[2]
                # amp = Amplicon(AmpliconName)

                # if AmpliconName in AmpliconList:
                #     amp = AmpliconList[AmpliconName] # Get Amplicon object by AmpliconName
                #     amp.add(dt)

                #if isTargeted == True:
                #    smpl.add(amp)
                #else:
                #    print("None Target List: " + sequence.query_name)

autoResult.add(smpl)

autoResult.autoTyping_dic = {}
autoResult.autoTyping_dic["snpVersion"] = autoResult.snpVersion
autoResult.autoTyping_dic["targetSnpVersion"] = autoResult.targetSnpVersion
autoResult.autoTyping_dic["sample"] = autoResult.sample_list

Convert_Json = {
    "autoTypingResult": autoResult.autoTyping_dic
}

jsonFormat = json.dumps(Convert_Json, indent=4)
print(jsonFormat)

