def main():
    fileName = "Sample_Table_Structure.sql"
    lineList = list()
    fieldsList = list()

    tableStarted = False
    lineList.append("[")
    with open(fileName) as f:
        for line in f:
            line = line.rstrip('\n')
            line = line.lstrip()
            line = line.rstrip()
            line = line.rstrip(',')
            line = line.replace('\t', ' ')

            tmpStr = line.split(" ")
            if tmpStr[0] == ")" or tmpStr[0] == "UNIQUE":
                tmpItem = fieldsList[len(fieldsList)-1]
                tmpItem = tmpItem.rstrip(',')
                fieldsList[len(fieldsList)-1] = tmpItem
                lineList.append(fieldsList)
                tableStarted = False
                if tmpStr[0] == ")":
                    print("*****************")
                    print("Table Completed")
                    print("*****************")
                    lineList.append("]")

                continue

            #print(tmpStr)
            if line.startswith("CREATE TABLE "):
                print("*****************")
                print("New Table Started: " + tmpStr[2])
                print("*****************")

                lineList.append('{"TableName": "' + tmpStr[2] + '",')
                lineList.append('"Fields": [')
                fieldsList.clear()
                tableStarted = True
                continue
            
            if tableStarted:
                fieldsList.append('{')
                fieldsList.append('"FieldName": "' + tmpStr[0] + '",')
                if tmpStr[1] == "CHARACTER":
                    charLen = tmpStr[2].replace("VARYING(", "")
                    charLen = charLen.replace(")", "")
                    fieldsList.append('"DataType": ' + '"VARCHAR"' + ',')
                    fieldsList.append('"DataLen": ' + charLen + ',')
                    fieldsList.append('"DataScale": 0')
                    fieldsList.append('},')
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
                            dataLen = numbreak[0]
                            dataScale = numbreak[1]
                            dataType = "DECIMAL(" + str(dataLen) + "," + str(dataScale) + ")"
                        
                        fieldsList.append('"DataType": "' + dataType + '"')
                        fieldsList.append('"DataLen": ' + str(dataLen) + ',')
                        fieldsList.append('"DataScale": ' + str(dataScale))
                    else:
                        if tmpStr[1] == "TIMESTAMP":
                            fieldsList.append('"DataType": "' + tmpStr[1] + '"')
                            fieldsList.append('"DataLen": 6,')
                            fieldsList.append('"DataScale": 0')
                        if tmpStr[1] == "INTEGER":
                            fieldsList.append('"DataType": "' + tmpStr[1] + '"')
                            fieldsList.append('"DataLen": 999999999,')
                            fieldsList.append('"DataScale": 0')
                        if tmpStr[1] == "SMALLINT":
                            fieldsList.append('"DataType": "' + tmpStr[1] + '"')
                            fieldsList.append('"DataLen": 9999,')
                            fieldsList.append('"DataScale": 0')
                        if tmpStr[1] == "TINYINT":
                            fieldsList.append('"DataType": "' + tmpStr[1] + '"')
                            fieldsList.append('"DataLen": 99,')
                            fieldsList.append('"DataScale": 0')
                        if tmpStr[1] == "BYTEINT":
                            fieldsList.append('"DataType": "TINYINT"')
                            fieldsList.append('"DataLen": 9,')
                            fieldsList.append('"DataScale": 0')


                    fieldsList.append('},')
    lineList.append("]")
    for s in lineList:
        if isinstance(s, list):
            for x in s:
                print("\t" + x)
        else:
            print(s)

if __name__ == "__main__":
    main()