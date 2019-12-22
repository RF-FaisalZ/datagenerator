import json
import ast
import string
import random
import time
from random import seed
from random import randint
from secrets import choice
from datetime import datetime

def genDDL(tableNames, lineList):
    obj = ""
    tabObj = ""

    for s in lineList:
        obj = obj + s

    for s in tableNames:
        tabObj = tabObj + s

    #Convert the Table Columns String to JSON
    jsonObj = json.loads(obj)

    #Convert the Table Names String to JSON
    tabJsonObj = json.loads(tabObj)

    for x in jsonObj:
        print("=======================================")
        print(x['TableName'])
        print("=======================================")
        print("CREATE TABLE " + x['TableName'] + "(")
        #Generate Parent's Data
        #genParentData(x['TableName'], x['Fields'], 10000000)
        f = open(x['TableName'],"w+", 100000)
        for y in x['Fields']:
            if str(y['DataType']).startswith("INTEGER") or str(y['DataType']).startswith("BIGINT") or str(y['DataType']).startswith("TINYINT") or str(y['DataType']).startswith("MEDIUMINT") or str(y['DataType']).startswith("SMALLINT"):
                f.write(y['FieldName'] + " " + str(y['DataType']) + " NOT NULL,\n")
            if str(y['DataType']).startswith("TIMESTAMP"):
                f.write(y['FieldName'] + " " + str(y['DataType']) + "(6) NOT NULL,\n")
            if str(y['DataType']).startswith("VARCHAR"):
                f.write(y['FieldName'] + " " + y['DataType'] + "(" + str(y['DataLen']) + ") NOT NULL,\n")
            if str(y['DataType']).startswith("DECIMAL"):
                f.write(y['FieldName'] + " " + str(y['DataType']) + " NOT NULL,\n")
        f.close()

        print("---------- Table Completed ------------")
        print("")

def readList(tableNames, lineList):
    obj = ""
    tabObj = ""

    for s in lineList:
        obj = obj + s

    for s in tableNames:
        tabObj = tabObj + s

    #Convert the Table Columns String to JSON
    jsonObj = json.loads(obj)

    #Convert the Table Names String to JSON
    tabJsonObj = json.loads(tabObj)

    for x in jsonObj:
        print("=======================================")
        print(x['TableName'])
        print("=======================================")
        
        if tabJsonObj[x['TableName']]["TableType"] == "Parent":
            #Generate Parent's Data
            #genParentData(x['TableName'], x['Fields'], 10000000)
            f = open(x['TableName'],"w+", 100000)
            for y in x['Fields']:
                f.write(y['FieldName'] + " " + y['DataType'] + " NOT NULL,\n")
            f.close()            
        else:
            #Generate Child's Data
            genChildData(x['TableName'], x['Fields'], 1000000)

        print("---------- Table Completed ------------")
        print("")

#Bad Performance
def genParentData_Slow(tabName, rowObj, rowCount):
    #https://www.geeksforgeeks.org/execute-string-code-python/
    strRow = ""
    print("Generating data for " + tabName + "\n")
    f = open(tabName,"w+")
    i=0
    for rows in range(rowCount):
        i = i + 1
        printProgressBar(i, rowCount, prefix = 'Progress:', suffix = 'Complete', length = 100)
        #print ("Rows Generated: " + str(i), end = "\r")
        strRow = str(rows) + ","
        for y in rowObj:
            strRow = strRow + genData(y) + ","
        strRow = strRow.rstrip(',')
        f.write(strRow + "\n")
        strRow = ""
    f.close()

def genParentData(tabName, rowObj, rowCount): 
    strRow = ""
    retVal = ""
    for y in rowObj:
        if y["TypeID"] == "N":
            retVal = 'str(1024)'
        if y["TypeID"] == "S":
            retVal = "'Data ' + str(i)"
        if y["TypeID"] == "T":
            retVal = 'str(datetime.now())'
        strRow = strRow + retVal + "+','+"

    strRow = strRow.rstrip("+','+")
    scriptTxt = """ 
def genMasterData(): 
    print("Generating data for """ + tabName + """")
    print()
    f = open('""" + tabName + """',"w+")
    i=0
    printProgressBar(i, """ + str(rowCount) + """, prefix = 'Progress:', suffix = 'Complete', length = 100)
    generatedRow = ''
    for rows in range(""" + str(rowCount) + """):
        generatedRow = str(i) + ',' + """ + strRow + """
        f.write(generatedRow + '\\n')
        i = i + 1
        printProgressBar(i, """ + str(rowCount) + """, prefix = 'Progress:', suffix = 'Complete', length = 100)
    generatedRow = ""
    f.close()

#genMasterData()
"""
    print(scriptTxt)
#    exec(scriptTxt) 

def genChildData(tabName, rows, rowCount):
    strRow = ""


def genData(obj):
    #{'HASH_ATTRIBUTE', 'DataType': 'BIGINT', 'DataLen': 999999999999999999, 'DataScale': 0}
    retVal = ''
    if obj["TypeID"] == "N":
        retVal = str(randint(0, obj["DataLen"]))
    if obj["TypeID"] == "S":
        retVal = '"' + rndStr(obj["DataLen"]) + '"'
    if obj["TypeID"] == "T":
        retVal = random_datetime()

    return retVal

def rndStr(strLen):
    #Generates Random String witn ALPHA/NUMERIC and then adds spaces at random places
    return (''.join([choice(string.ascii_uppercase + string.digits) for _ in range(strLen)]).replace(str(randint(0,9)), ' ').replace(chr(randint(65,65+27)), ' '))

def random_datetime():
    from_date = datetime(year = 1947, month = 1, day = 1, hour = 0, minute = 0, second = 0)
    to_date = datetime.now()
    delta = to_date - from_date
    rand = random.random()
    return str(from_date + rand * delta)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line after completion
    if iteration == total: 
        print("\n")

def main():
    fileName = "Sample_Table_Structure.sql"
    lineList = list()
    tableNames = list()

    tableStarted = False
    lineList.append("[")
    tableNames.append("{")

    with open(fileName) as f:
        for line in f:
            line = line.rstrip('\n')
            line = line.lstrip()
            line = line.rstrip()
            line = line.rstrip(',')
            line = line.replace('\t', ' ')

            tmpStr = line.split(" ")
            if tmpStr[0] == ")" or tmpStr[0] == "UNIQUE":
                tmpItem = lineList[len(lineList)-1]
                tmpItem = tmpItem.rstrip(',')
                lineList[len(lineList)-1] = tmpItem
                tableStarted = False
                if tmpStr[0] == ")":
                    print("*****************")
                    print("Table Completed")
                    print("*****************")
                    lineList.append("]},")
                continue

            if line.startswith("CREATE TABLE "):
                print("*****************")
                print("New Table Started: " + tmpStr[2])
                print("*****************")

                lineList.append('{"TableName": "' + tmpStr[2] + '",')
                tableNames.append('"' + tmpStr[2] + '": ')
                tableNames.append('{"TableType": "Parent"},')
                lineList.append('"Fields": [')
                tableStarted = True
                continue
            
            if tableStarted:
                #if str(tmpStr[0]).startswith("PK_"):
                #    continue

                lineList.append('{')
                lineList.append('"FieldName": "' + tmpStr[0] + '",')
                #Set the previous Table as the Child
                if str(tmpStr[0]).startswith("FK_"):
                    tableNames[len(tableNames)-1] = ('{"TableType": "Child"},')

                if tmpStr[1] == "CHARACTER":
                    charLen = tmpStr[2].replace("VARYING(", "")
                    charLen = charLen.replace(")", "")
                    lineList.append('"DataType": ' + '"VARCHAR"' + ',')
                    lineList.append('"DataLen": ' + charLen + ',')
                    lineList.append('"DataScale": 0,')
                    lineList.append('"TypeID": "S"')
                    lineList.append('},')
                else:
                    if tmpStr[1].startswith("NUMERIC"):
                        numbreak = tmpStr[1].split(",")
                        numbreak[0] = numbreak[0].replace("NUMERIC(", "")
                        numbreak[1] = numbreak[1].replace(")", "")

                        if int(numbreak[1]) == 0:
                            dataScale = 0
                            if int(numbreak[0]) <= 2:
                                dataType = "TINYINT"
                                dataLen = 99
                            if int(numbreak[0]) > 2 and int(numbreak[0]) <= 4:
                                dataType = "SMALLINT"
                                dataLen = 9999
                            if int(numbreak[0]) > 4 and int(numbreak[0]) <= 6:
                                dataType = "MEDIUMINT"
                                dataLen = 999999
                            if int(numbreak[0]) > 6 and int(numbreak[0]) <= 9:
                                dataType = "INTEGER"
                                dataLen = 999999999
                            if int(numbreak[0]) > 9:
                                dataType = "BIGINT"
                                dataLen = 999999999999999999
                        else:
                            dataLen = ast.literal_eval(''.rjust(int(numbreak[0]), '9'))
                            dataScale = ast.literal_eval(''.rjust(int(numbreak[1]), '9'))
                            dataType = "DECIMAL(" + str(numbreak[0]) + "," + str(numbreak[1]) + "),"
                        
                        lineList.append('"DataType": "' + dataType + '",')
                        lineList.append('"DataLen": ' + str(dataLen) + ',')
                        lineList.append('"DataScale": ' + str(dataScale) + ',')
                        lineList.append('"TypeID": "N"')
                    else:
                        if tmpStr[1] == "TIMESTAMP":
                            lineList.append('"DataType": "' + tmpStr[1] + '",')
                            lineList.append('"DataLen": 6,')
                            lineList.append('"DataScale": 0,')
                            lineList.append('"TypeID": "T"')
                        if tmpStr[1] == "INTEGER":
                            lineList.append('"DataType": "' + tmpStr[1] + '",')
                            lineList.append('"DataLen": 999999999,')
                            lineList.append('"DataScale": 0,')
                            lineList.append('"TypeID": "N"')
                        if tmpStr[1] == "SMALLINT":
                            lineList.append('"DataType": "' + tmpStr[1] + '",')
                            lineList.append('"DataLen": 9999,')
                            lineList.append('"DataScale": 0,')
                            lineList.append('"TypeID": "N"')
                        if tmpStr[1] == "TINYINT":
                            lineList.append('"DataType": "' + tmpStr[1] + '",')
                            lineList.append('"DataLen": 99,')
                            lineList.append('"DataScale": 0,')
                            lineList.append('"TypeID": "N"')
                        if tmpStr[1] == "BYTEINT":
                            lineList.append('"DataType": "TINYINT",')
                            lineList.append('"DataLen": 9,')
                            lineList.append('"DataScale": 0,')
                            lineList.append('"TypeID": "N"')

                    lineList.append('},')
    
    tmpItem = lineList[len(lineList)-1]
    tmpItem = tmpItem.rstrip(',')
    lineList[len(lineList)-1] = tmpItem
    lineList.append("]")

    tmpItem = tableNames[len(tableNames)-1]
    tmpItem = tmpItem.rstrip(',')
    tableNames[len(tableNames)-1] = tmpItem
    tableNames.append("}")

    #for x in lineList:
    #    print(x)

    #readList(tableNames, lineList)
    genDDL(tableNames, lineList)

if __name__ == "__main__":
    main()
    