from PySimpleGUI import *
import pandas as pd


indexWhereErrorWasFound = []
errorCount = 0
errorTypes = ""
Levels = set()

levelTypeDict = {
    # No level filtering is done on the event. When used as a level filter for enabling events, for example in EventListener.EnableEvents(), events of all levels will be included.
    0: "LogAlways",
    # This level corresponds to a critical error, which is a serious error that has caused a major failure.
    1: "Critical",
    # This level adds standard errors that signify a problem.
    2: "Error",
    # This level adds warning events (for example, events that are published because a disk is nearing full capacity).
    3: "Warning",
    # This level adds informational events or messages that are not errors. These events can help trace the progress or state of an application.
    4: "Informational",
    # This level adds lengthy events or messages. It causes all events to be logged.
    5: "Verbose",
}
defineTypeDict = {
    "LogAlways": "No level filtering is done on the event. When used as a level filter for enabling events, for example in EventListener.EnableEvents(), events of all levels will be included.",
    "Critical": "This level corresponds to a critical error, which is a serious error that has caused a major failure.",
    "Error": "This level adds standard errors that signify a problem.",
    "Warning": "This level adds warning events (for example, events that are published because a disk is nearing full capacity).",
    "Informational": "This level adds informational events or messages that are not errors. These events can help trace the progress or state of an application.",
    "Verbose": "This level adds lengthy events or messages. It causes all events to be logged.",
}

NumberOfIndividualErrors = {}


def preProcessDataframe(name):
    print('preprocessing')
    global data, rows, cols
    data = pd.read_csv(name, index_col=False)
    rows = len(data.axes[0])
    cols = len(data.axes[1])


def processLevels(name):
    print('Levels')
    preProcessDataframe(name)
    for i in range(1, rows):
        errorTypes = int(data.iat[i, 5])
        Levels.add(levelTypeDict[errorTypes])
        try:
            NumberOfIndividualErrors[errorTypes] += 1
        except:
            NumberOfIndividualErrors[errorTypes] = 1
    print(NumberOfIndividualErrors)
    return


def writeAndPrintErrors(name):
    processLevels(name)
    file = open(name + " TypesOfErrors", "w")
    file.write("Types of Erros that have occured in your laptop:\n\n")

    for i in Levels:
        print(i)
        file.write(i+' ('+defineTypeDict[i]+')' + '\n')
    file.close()
    return


def writeAndPrintErrorCount(name):
    processLevels(name)
    file = open(name+" AllErrorCount", "w")
    file.write("All the Errors that have occured and how many times:\n\n")

    for i, j in NumberOfIndividualErrors.items():
        print("{:<8} {:<10}\n".format(levelTypeDict[i], ': ' + str(j)))
        file.write("{:<8} {:<10}\n".format(levelTypeDict[i], ':  ' + str(j)))
    file.close()
    return


def Analyzer():
    theme('Material2')
    current_files = [i for i in os.listdir(
        os.getcwd()) if i.endswith('.csv')]
    heading = [Text('Contents of the Current Folder are given below :')]
    listoffiles = [Listbox(values=[(' ' + str(i+1) + ')  ') + current_files[i]
                           for i in range(len(current_files))], size=(150, 5), key='list')]

    InputBox = [Text('Enter the index'),
                Input()]
    Analyzerbutton = [Button("Analyze error types", key='B1'),
                      Button("Analyze error count", key='B3')]
    layout = [
        heading,
        listoffiles,
        InputBox,
        Analyzerbutton,
    ]

    window = Window('Analysis Window', layout=layout, size=(700, 200))

    while True:
        event, values = window.read()
        print(values)

        if event == WIN_CLOSED or event == 'B2':
            break
        if event == "B1":
            try:
                file = os.path.join(
                    os.getcwd(), current_files[int(values[0])-1])
                writeAndPrintErrors(file)
                popup(file + ' TypesOfErrors.txt' +
                      ' has been created for you')
            except Exception as e:
                popup(e)
        if event == "B3":
            try:
                file = os.path.join(
                    os.getcwd(), current_files[int(values[0])-1])
                writeAndPrintErrorCount(file)
                popup(file + ' AllErrorCount.txt' +
                      ' has been created for you')
            except Exception as e:
                popup(e)
    window.close()
    return


# Analyzer()
