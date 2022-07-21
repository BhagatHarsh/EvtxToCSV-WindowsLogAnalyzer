# imports
import os
import pandas as pd
from typing import OrderedDict
from evtx import PyEvtxParser
import ctypes
import json
import xmltodict
import pandas as pd
import json
from os import listdir
from os.path import isfile, join
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from PySimpleGUI import popup



today = str(datetime.today())[0:10]  # YYYY-MM-DD
logPath = r"C:\Windows\System32\winevt\Logs"
allFilePaths = [join(logPath, f)
                for f in listdir(logPath) if isfile(join(logPath, f))]



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# def getFile():
#     _counter = 1
#     for name in os.listdir(path=logPath):
#         print(str(_counter) + ')  ' + name)
#         _counter += 1
#     index = int(
#         input("\nEnter the Index of File you want to Analyze : "))
#     return allFilePaths[index-1]


def deleteIT(folder_path):
    try:
        if(os.path.isdir(folder_path)):
            if os.path.exists(folder_path):
                # checking whether the folder is empty or not
                if len(os.listdir(folder_path)) == 0:
                    # removing the file using the os.remove() method
                    os.rmdir(folder_path)
                    popup("Removed the Folder")
                else:
                    for file in os.listdir(folder_path):
                        os.remove(os.path.join(folder_path, file))
                    os.rmdir(folder_path)
                    popup("Removed the Folder")
            else:
                # file not found message
                popup("File not found in the directory")
        else:
            os.remove(folder_path)
            popup("Removed the file")
    except Exception as e:
        popup(e)


def createFolders():
    global xml_path, json_path
    try:
        xml_path = join(os.path.abspath(os.getcwd()), "allXmlFiles")
        json_path = join(os.path.abspath(os.getcwd()), "allJsonFiles")
        os.mkdir(xml_path)
        print("Created a new folder at: " + xml_path)
        os.mkdir(json_path)
        print("Created a new folder at: " + json_path)
    except:
        return


try:

    def GenerateCSV(ind, date):
        global df
        # Code of your program here
        evtx_path = allFilePaths[ind]
        os.path.normpath(evtx_path)
        print("Accessing the File at: " + evtx_path)
        _flag = 0
        createFolders()
        parser = PyEvtxParser(evtx_path)
        print(date)
        if(date != ' '):
            for record in parser.records():
                # print(record['timestamp'][0:10] , date)
                if(record['timestamp'][0:10] == date):
                    recordID = str(record["event_record_id"])
                    file = open(os.path.join(
                        xml_path, recordID+".xml"), "w")
                    # file.write(f'Event Record ID: {record["event_record_id"]}\n')
                    # file.write(f'Event Timestamp: {record["timestamp"]}\n')
                    file.write(record['data'])
                    file.close()
                    xmlToJson(recordID)
                    with open(os.path.join(json_path, recordID+".json")) as f:
                        data = json.loads(f.read())
                    if(_flag == 0):
                        df = pd.json_normalize(data)
                    else:
                        df = pd.concat([pd.json_normalize(data), df])
                    _flag = 1
                    # file.write('---------------------------------------\n')
            if(_flag == 1):
                df.to_csv(str(ind+1)+"-"+today+".csv", index=False)
                return True
            else:
                popup('Invalid File')
                return False
        else:
            for record in parser.records():
                recordID = str(record["event_record_id"])
                file = open(os.path.join(xml_path, recordID+".xml"), "w")
                # file.write(f'Event Record ID: {record["event_record_id"]}\n')
                # file.write(f'Event Timestamp: {record["timestamp"]}\n')
                file.write(record['data'])
                file.close()
                xmlToJson(recordID)
                with open(os.path.join(json_path, recordID+".json")) as f:
                    data = json.loads(f.read())
                if(_flag == 0):
                    df = pd.json_normalize(data)
                else:
                    df = pd.concat([pd.json_normalize(data), df])
                _flag = 1
                # file.write('---------------------------------------\n')
            if(_flag == 1):
                df.to_csv(str(ind+1)+"-data.csv", index=False)
                return True
            else:
                popup('Invalid File')
                return False
        

    def xmlToJson(recordID):

        # open the input xml file and read
        # data in form of python dictionary
        # using xmltodict module
        data_dict = OrderedDict()
        with open(os.path.join(xml_path, recordID+".xml")) as xml_file:

            data_dict = xmltodict.parse(xml_file.read())
            xml_file.close()

            # generate the object using json.dumps()
            # corresponding to json data

            json_data = json.dumps(data_dict)

            # Write the json data to output
            # json file
            with open(os.path.join(json_path, recordID+".json"), "w") as json_file:
                json_file.write(json_data + '\n')
                json_file.close()

except Exception as e:
    print(e)

# recived data and formed a df



try:
    # This function is called to send a secure email to the user about TranactionHistory,OTP,Updates etc.
    def SendEmail(Email, subject, msgstr, fileName):
        print("Emailing")
        # Emailing the user his ID and password
        # message to be sent
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = "pythonemailtestservice@gmail.com"
        msg['To'] = Email
        # msg.attach(MIMEText(msgstr, 'plain'))
        # The subject line
        # The body and the attachments for the mail
        attach_file = open(fileName, 'rb')  # Open the file as binary mode
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        payload.add_header('Content-Decomposition',
                        'attachment; filename={}'.format(fileName))
        msg.attach(payload)
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # checking connections
        # s.ehlo()
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("pythonemailtestservice@gmail.com", "tzleaaknhfstkngz")
        # sending the mail
        s.sendmail("pythonemailtestservice@gmail.com", Email, msg.as_string())
        # terminating the session
        s.quit()
        print("Done Email")
        return
except:
    popup("Email Error try again")

# SendEmail('harsh.b2@ahduni.edu.in','qsdasd','asdasd','Analyzer.py')
