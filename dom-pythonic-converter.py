import sys
import xml.etree.ElementTree as ET
import csv
import json
from lxml import etree
from io import StringIO
def indent(elem, level=0):  #for pretty writing to xml file
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
def csvToxml(file1, file2):
    root = ET.Element("departments") #root of tree
    rowNum = 0
    oldUni = ""
    newUni = ""
    with open(file1,'rt') as f: #read csv file
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if rowNum == 0 : #skip first row couse of tag row
                tags = row
            else:
                element = row #for ecah row, put is to element array
                newUni = element[1]
                if (newUni != oldUni):
                    node = ET.SubElement(root, "university", {"name":element[1],"uType":element[0]}) #start to work with subelements and its attributes
                    node2 = ET.SubElement(node, "item", {"id":element[3],"faculty":element[2]})
                else:
                    node2 = ET.SubElement(node, "item", {"id":element[3],"faculty":element[2]})
                node3 = ET.SubElement(node2, "name", {"lang":element[5],"second":element[6]})
                node3.text = element[4] #text of elements 
                node9 = ET.SubElement(node2, "scolarship")
                node9.text = element[7]
                node4 = ET.SubElement(node2, "period",)
                node4.text = element[8]
                node5 = ET.SubElement(node2, "quota", {"spec":element[11]})
                node5.text = element[10]
                node6 = ET.SubElement(node2, "field")
                node6.text = element[9]
                node7 = ET.SubElement(node2, "last_min_scoreorder")
                node7.text = element[12]
                node8 = ET.SubElement(node2, "grant")
                node8.text = element[13]
            oldUni = newUni
            rowNum = rowNum + 1 #to count row
    indent(root) #to print tree beautifully
    data = ET.tostring(root, encoding='utf8', method='xml')
    f2 = open(file2, "w") #open xml file
    f2.write(data.decode("utf-8")) #writo to xml file the data
    f2.close # close xml file
def xmlTocsv(file1, file2):  
    parser = ET.XMLParser(encoding="utf-8") #parse the tree
    tree = ET.parse(file1, parser=parser) 
    root = tree.getroot() #get root of tree
    tags = [ "university_type","university_name","faculty","id","faculty_name", "lang", "second","scolarship" ,"period","field","quota","spec","last_min_scoreorder","grant"]
    csvFile = open(file2,'w')#open csv file
    csvWrite = csv.writer(csvFile,delimiter=';')
    csvHead = [] #for tags, I work with specific file so, I don't use the array, but if ı would not use specific file then I should have used them for element names
    count = 0
    for uni in root.findall('university'):
        university = [] #for each university create an array
        if(count==0):
            csvWrite.writerow(tags) #write tags to the first row
        else:#get elements of tree and send them to the array
            for elem in uni.findall('item'):
                uType = uni.get('uType')
                university.append(uType)
                name = uni.get('name')
                university.append(name)
                faculty = uni.find('item').get('faculty')
                university.append(faculty)
                id1 = uni.find('item').get('id')
                university.append(id1)
                facultyname = elem.find('name').text
                university.append(facultyname)
                lang = elem.find('name').get('lang')
                university.append(lang)
                second = elem.find('name').get('second')
                university.append(second)
                scolarship = elem.find('scolarship').text
                university.append(scolarship)
                period = elem.find('period').text
                university.append(period)
                field = elem.find('field').text
                university.append(field)
                quota = elem.find('quota').text
                university.append(quota)
                spec = elem.find('quota').get('spec')
                university.append(spec)
                last_min_scoreorder = elem.find('last_min_scoreorder').text
                university.append(last_min_scoreorder)
                grant = elem.find('grant').text
                university.append(grant)      
                csvWrite.writerow(university)#write each row the each universities specific elements
                university = [] #for each university create an array
        count = count + 1
    csvFile.close()#close the csv file
def xmlTojson(file1, file2):
    parser = ET.XMLParser(encoding="utf-8")#parse the tree
    tree = ET.parse(file1, parser=parser)
    root = tree.getroot()#get the root 
    jsonString = '['#while converting to string "[" will be at the beginning
    with open(file2, 'w', encoding='utf-8') as json_file: #open json file
        for uni in root.findall('university'): 
            data_dict = dict() #the is is a dict to put all xml data to csv
            
            for elem in uni.findall('item'):
                uType = uni.get('uType')
                data_dict['uType'] = uType
                name = uni.get('name')
                data_dict['name'] = name
                faculty = uni.find('item').get('faculty')
                id1 = uni.find('item').get('id')
                facultyname = elem.find('name').text
                lang = elem.find('name').get('lang')
                second = elem.find('name').get('second')
                scolarship = elem.find('scolarship').text
                period = elem.find('period').text
                field = elem.find('field').text
                quota = elem.find('quota').text
                spec = elem.find('quota').get('spec')
                last_min_scoreorder = elem.find('last_min_scoreorder').text
                grant = elem.find('grant').text
                departments = {"id":id1,"facultyname":facultyname,"lang":lang,"second":second,"scolarship":scolarship,"period":period,"field":field,"quota":quota,"spec":spec,"last_min_scoreorder":last_min_scoreorder,"grant":grant}
                items = {"faculty":faculty,"department":[departments] } 
                data_dict['items'] = [items] #departments and items are the subelement of university that is why they are dict by own 
                newString = json.dumps(data_dict, indent = 4, sort_keys=True, ensure_ascii=False) #convert dict to json string to put comma between each university
                jsonString = jsonString + newString + ','
        jsonString = jsonString[:-1]#on last line ther will be a comma because of upper code, so i deleted the last comma
        jsonString = jsonString + ']' #close tag of json string
        finaldict = json.loads(jsonString)#convert jsonString to dict again
        json.dump(finaldict, json_file, indent = 4, sort_keys=True, ensure_ascii=False)#finally put dict to json file 
def jsonToxml(file1, file2):
    with open(file1,'r') as json_file:#open json file
        jsonData = json.load(json_file)
    root = ET.Element("departments")#create xml root
    oldUni = ""
    newUni = ""
    for eachDict in jsonData:#for each dict read all the data
        newUni = eachDict['name']

        for itemsElement in eachDict['items']:
            for deparmentElement in itemsElement['department']:
                
                if (newUni != oldUni):
                    node1 = ET.SubElement(root,"university")
                    node1.set('name',eachDict['name'])
                    node1.set('uType',eachDict['uType'])    
                    node2 = ET.SubElement(node1,"item")                    
                    node2.set('faculty',itemsElement['faculty'])
                    node2.set('id',deparmentElement['id'])
                else:
                    node2 = ET.SubElement(node1,"item")                    
                    node2.set('faculty',itemsElement['faculty'])
                    node2.set('id',deparmentElement['id'])

                node3 = ET.SubElement(node2,"name")
                node3.set('lang',deparmentElement['lang'])
                node3.set('second',deparmentElement['second'])
                node3.text = deparmentElement['facultyname']
                node4 = ET.SubElement(node2,"scolarship")
                node4.text = deparmentElement['scolarship']
                node5 = ET.SubElement(node2,"period")
                node5.text = deparmentElement['period']
                node6 = ET.SubElement(node2,"quota")
                node6.text = deparmentElement['quota']
                node6.set('spec',deparmentElement['spec'])
                node7 = ET.SubElement(node2,"field")
                node7.text = deparmentElement['field']
                node8 = ET.SubElement(node2,"last_min_scoreorder")
                node8.text = deparmentElement['last_min_scoreorder']
                node9 = ET.SubElement(node2,"grant")
                node9.text = deparmentElement['grant']
                oldUni = newUni

    indent(root)#xml beautiful writing
    data = ET.tostring(root, encoding='utf8', method='xml')
    f2 = open(file2, "w")
    f2.write(data.decode("utf-8")) #writo to xml file the data
    f2.close
def csvTojson(file1, file2):
    json_file = open(file2,'w', encoding='utf-8')#open json file
    jsonString = '['#while converting to string "[" will be at the beginning
    rowNum = 0
    with open(file1,'rt') as f: #read csv file
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if rowNum == 0 : #skip first row couse of tag row
                tags = row
            else:
                element = row 
                data_dict = dict() 
                data_dict['uType'] = element[0] 
                data_dict['name'] = element[1] 
                departments = {"id":element[3],"facultyname":element[2],"lang":element[5],"second":element[6],"scolarship":element[7],"period":element[8],"field":element[9],"quota":element[10],"spec":element[11],"last_min_scoreorder":element[12],"grant":element[13]}
                items = {"faculty":element[4],"department":[departments]} 
                data_dict['items'] = [items] #departments and items are the subelement of university that is why they are dict by own 
                newString = json.dumps(data_dict, indent = 4, sort_keys=True, ensure_ascii=False) #convert dict to json string to put comma between each university
                jsonString = jsonString + newString + ','
            rowNum = rowNum + 1 #to count row
    jsonString = jsonString[:-1]#on last line ther will be a comma because of upper code, so i deleted the last comma
    jsonString = jsonString + ']' #close tag of json string
    finaldict = json.loads(jsonString)#convert jsonString to dict again
    json.dump(finaldict, json_file, indent = 4, sort_keys=True, ensure_ascii=False)#finally put dict to json file 
    json_file.close()     #close the json file                 
def jsonTocsv(file1, file2):
    with open(file1,'r') as json_file:#open json file
        jsonData = json.load(json_file)
    tags = [ "university_type","university_name","faculty","id","faculty_name", "lang", "second","scolarship" ,"period","field","quota","spec","last_min_scoreorder","grant"]
    with open(file2,'w') as csvFile: #read csv file
        csvWrite = csv.writer(csvFile,delimiter=';')
        csvWrite.writerow(tags)#write first row
        for eachDict in jsonData:#for each dict read all the data
            row = [] #for each university create an array
            row.append(eachDict['uType'])
            row.append(eachDict['name'])
            for itemsElement in eachDict['items']:
                row.append(itemsElement['faculty'])
                for deparmentElement in itemsElement['department']:
                    row.append(deparmentElement['id'])
                    row.append(deparmentElement['facultyname'])
                    row.append(deparmentElement['lang'])
                    row.append(deparmentElement['second'])
                    row.append(deparmentElement['scolarship'])
                    row.append(deparmentElement['period'])
                    row.append(deparmentElement['field'])
                    row.append(deparmentElement['quota'])
                    row.append(deparmentElement['spec'])
                    row.append(deparmentElement['last_min_scoreorder'])
                    row.append(deparmentElement['grant'])
            csvWrite.writerow(row)#write each row the each universities specific elements     
def xmlValidatesWithxsd(file1, file2):
    doc = etree.parse(file1)
    root = doc.getroot()
    xmlschema_doc = etree.parse(file2)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(etree.tostring(root))
    validation_result = xmlschema.validate(doc)
    print(validation_result)
    xmlschema.assert_(doc)
    
def main():
    if (len(sys.argv)!=4):
        print("Wrong command line argument.")
    else:
        if(sys.argv[3]=="1"):
            csvToxml(sys.argv[1],sys.argv[2])
        if(sys.argv[3]=="2"):
            xmlTocsv(sys.argv[1],sys.argv[2])
        if(sys.argv[3]=="3"):
            xmlTojson(sys.argv[1],sys.argv[2])
        if(sys.argv[3]=="4"):
            jsonToxml(sys.argv[1],sys.argv[2])
        if(sys.argv[3]=="5"):
            csvTojson(sys.argv[1],sys.argv[2])
        if(sys.argv[3]=="6"):
            jsonTocsv(sys.argv[1],sys.argv[2])
        if(sys.argv[3]=="7"):
            xmlValidatesWithxsd(sys.argv[1],sys.argv[2])         
if __name__ == "__main__":
    main()