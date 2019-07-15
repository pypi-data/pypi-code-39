from database import connection_pool
import xml.etree.ElementTree as ET 
import re
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
connection = connection_pool.getconn()

# Fetching Data From Database
def fetchdata():
    with connection.cursor() as cursor:
        cursor.execute("select content from xml.t_parties where publication_id in (select publication_id from xml.t_patent_document_values where country = 'US' order by family_id desc limit 100000)")
        result = cursor.fetchall()
        with open('finaldata.xml','w') as fp:
            fp.write('\n'.join('{}'.format(row[0]) for row in result))
        # for row in result:
        #     tree = ET.fromstring(row[0])
        #     print("++++++++++Applicants+++++++++++++++")
        #     for applicant in tree.iter('applicant'):
        #         for name in applicant.iter('name'):
        #             print(name.attrib,name.text)
        #         for country in applicant.iter('country'):
        #             print(country.attrib,country.text)
        #     print("++++++++++++Inventors+++++++++++++")
        #     for inventor in tree.iter('inventor'):
        #         for name in inventor.iter('name'):
        #             print(name.attrib,name.text)
        #         for country in inventor.iter('country'):
        #             print(country.attrib,country.text)

    connection.commit()

# Parsing Fetched XML data from database.
def mainlist(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    detail = []
    for parties in root.iter('parties'):
        partieslist = []
        for applicant in parties.iter('inventor'):
            seqno = applicant.attrib['sequence']
            fullname = ''
            cityad = ''
            countryad =''
            statead = ''
            for name in applicant.iter('name'):
                fullname = name.text
            for fname in applicant.iter('first-name'):
                fullname = fname.text
            for lname in applicant.iter('last-name'):
                fullname = fullname + lname.text
            for city in applicant.iter('city'):
                cityad = city.text
            for country in applicant.iter('country'):
                countryad = country.text
            for state in applicant.iter('state'):
                statead= state.text
            if fullname != '':
                namelist = [seqno,fullname,cityad,statead,countryad]
                partieslist.append(namelist)
            
        detail.append(partieslist)
    return detail

# Creating the Master Record consisting seq no, name , city, state ,country
def MasterRecord(allist):
    partiesmaster = []
    for parties in allist:
        applicantlist = []
        x = pd.DataFrame(parties)
        y = x.groupby(0).apply(lambda z: list(z.values))
        goal = [[list(z) for z in y[idx]] for idx in y.index]
        
    
        for seq in goal:
            seqno=0
            namelist = []
            citylist = []
            statelist=[]
            countrylist = []
            for i in seq:
                seqno = i[0]
                namelist.append(i[1])
                if i[2] != '':
                    citylist.append(i[2])
                if i[3] !='':
                    statelist.append(i[3])
                if i[4] != '':
                    countrylist.append(i[4])
            seqlist = [seqno,namelist,citylist,statelist,countrylist]
            applicantlist.append(seqlist)
        partiesmaster.append(applicantlist)
    return partiesmaster

# Calculating the similarity score of each name wrt the seq 1 name  
def SimilScore(masterlist):
    totalscore = []
    for parties in masterlist:
        allnames = []
        testname =''
        for sequence in parties:
            seq = []
            sqno = sequence[0]
            names = sequence[1]
            for i in names:
                names1 = [sqno,i]
                allnames.append(names1)
                # seq.append(names1)
            if sqno == '1':
                for namestest in sequence[1]:
                    if len(testname)<len(namestest):
                        testname=namestest
            # allnames.append(seq)
        for names in allnames:
            testname = ' '.join(testname.split(',')[::-1])
            newname = ' '.join(names[1].split(',')[::-1])
            namerev = ''.join(newname.split(' ')[::-1]) 
            # newname = re.findall('[A-Z][^a-z]+', newname)
            # seperator = ' '
            # newname =seperator.join(newname)
            # testname = re.findall('[A-Z][^a-z]+', testname)
            # seperator = ' '
            # testname =seperator.join(testname)
            score1 =fuzz.token_set_ratio(testname.lower(),newname.lower())
            scorerev = fuzz.token_set_ratio(testname.lower(),namerev.lower())
            if score1 > scorerev:
                score =score1
            else:
                score = scorerev
            finallist = [names[0],names[1],score,testname]
            # seqscore.append(finallist)
            totalscore.append(finallist)
        # score = process.extract(testname,allnames)
        # totalscore.append(score)
    with open('score.csv','w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for i in totalscore:
            csv_writer.writerow(i)
    # print(totalscore)
    return totalscore
            
def parsxml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    parties = []

    for item in root.findall('./parties'):
        detail = []
        for child in item:
            detail.append(child)
        parties.append(detail)  
    return parties 

# classify each applicant name in yes and no category (seq no 1 is yes category) 
def classify(scores):
    dataset = []
    for assigne in scores:
        if assigne[0] == '1':
            asgncls = 'yes'
            name = assigne[1]
            score = assigne[2]
            ref = assigne[3]
            asgnlist = [asgncls,score,name,ref]
            dataset.append(asgnlist)

        else:
            asgncls = 'no'
            name = assigne[1]
            score = assigne[2]
            ref = assigne[3]
            asgnlist=[asgncls,score,name,ref]
            dataset.append(asgnlist)
        # dataset.append(seqdataset)
    # print(dataset)
    with open('dataset.csv','w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for i in dataset:
            csv_writer.writerow(i)
    findthresh(dataset)


# Calculating threshold for similarity score 

def findthresh(dataset):
    threshold = 50
    bestthreshold = 0
    best = 0
    results= []
    wronglist = []
    correctlist = []
    while threshold <= 100:
        trueP = 0
        trueN = 0
        falseP = 0
        falseN = 0
        for i in dataset:
            if i[0] == 'yes':
                if i[1] >= threshold:
                    trueP = trueP+1
                elif i[1]< threshold:
                    falseN = falseN+1
            else:
                if i[1]>= threshold:
                    falseP = falseP+1
                elif i[1] < threshold:
                    trueN = trueN+1
        precision = (trueP/(trueP+falseP))*100
        recall = (trueP/(trueP+falseN))*100
        accuracy = ((trueP+trueN)/(trueN+trueP+falseN+falseP))*100
        if accuracy > best:
            best = accuracy
            bestthreshold = threshold
        reslist = [threshold,precision,recall,accuracy]
        results.append(reslist)
        print("\n>>>>>>>Result for Threshold {} <<<<<<<<<<<\n".format(threshold))
        print("\n Precision: {} recall: {} Accuracy: {} ".format(precision,recall,accuracy))
        threshold = threshold+1
    # referencename = seq[0][2]
    print("\n>>>>>>>>>>><<<<<<<<<<<<<<\n")
    print("Best Threshold is {} \n".format(bestthreshold))
    # Finding the wrong classification with best threshold 
    wrongentries = 0
    for i in dataset:
        if i[0] == 'yes':
            if i[1]< bestthreshold:
                clss= i[0]
                score = i[1]
                name= i[2]
                ref = i[3]
                # ref = referencename
                lst = [clss,score,name,ref]
                wronglist.append(lst)
                wrongentries = wrongentries +1
            else:
                clss= i[0]
                score = i[1]
                name= i[2]
                ref = i[3]
                lst = [ref,name,clss,score]
                correctlist.append(lst)
        else:
            if i[1]>= bestthreshold:
                clss= i[0]
                score = i[1]
                name= i[2]
                ref = i[3]
                # ref = referencename
                lst = [clss,score,name,ref]
                wronglist.append(lst)
                wrongentries = wrongentries +1
            else:
                clss= i[0]
                score = i[1]
                name= i[2]
                ref = i[3]
                lst=[ref,name,clss,score]
                correctlist.append(lst)
    with open('CSV_FOLDER/wrong.csv','w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for i in wronglist:
            csv_writer.writerow(i)
    with open('CSV_FOLDER/correct.csv','w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for i in correctlist:
            csv_writer.writerow(i)
    print("no of wrong entries : {}".format(wrongentries))

    
    with open('results.csv','w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for i in results:
            csv_writer.writerow(i)




def main():
    # data = parsxml('sampledata.xml')
    # fetchdata()
    detailist = mainlist('finaldata.xml')
    master = MasterRecord(detailist)
    with open('masterfile.csv','w') as csv_file:
        csv_writer = csv.writer(csv_file,delimiter=',')
        for parties in master:
            csv_writer.writerow(parties) 
    scores = SimilScore(master)
    classify(scores)
if __name__ == "__main__": 
    main()


