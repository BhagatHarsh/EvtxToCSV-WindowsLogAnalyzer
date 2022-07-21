from PySimpleGUI import *
from Analyzer import *
from checkLOG import *
from detailScreen import *
from logScreen import *
from emailScreen import *
from homeScreen import *
flag = 0
b = 0
if is_admin():
    print('Now Admin')
    flag = 1
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def getFilesReady(index, time):
    if(time == ' '):
        if(GenerateCSV(int(index)-1, time)):
            emailscreen("The Daily Report of Errors",
                        "The Major Errors that have occured today are given below:", index+"-data.csv")
            popup("done")
        else:
            popup('Error Occured')
    else:
        if(GenerateCSV(int(index)-1, time)):
            emailscreen("The Daily Report of Errors",
                        "The Major Errors that have occured today are given below:", index+"-"+time+".csv")
            popup("done")
        else:
            popup('Error Occured')
    return


def mains():
    theme('Material2')

    # Heaading
    heading = [Text('Please pick a Log file from the List Below:',
                    font='Sans-Serif 16 bold underline', key="heading", visible=True),
               Text('                                                                                                                                                                                                      '),
               Button('info', font='Sans-Serif 10 bold', key="B5", button_color=('white', '#2fa4e7'), visible=True), ]

    # listBox containing all file names
    listOfAllLogs = [Listbox(values=[(' ' + str(i+1) + ')  ' + allFilePaths[i])
                                     for i in range(len(allFilePaths))], font='Courier 12 bold', select_mode='extended', key='fac', size=(220, 25), visible=True)]

    # to take the number to process upon
    InputBox = [Text('Enter the Log Index :', font='Sans-Serif 14 underline', key="InputBox", visible=True),
                Input(key="LogIndex", visible=True)]

    # yyyy-mm-dd
    dateBox = [Text('Enter the date in format yyyy-mm-dd :', font='Sans-Serif 14 underline', visible=True),
               Input(key="dateBox", visible=True)]

    # to listen to the button
    checkOutButton = [Button('All Logs', font='Sans-Serif 10 bold', key="B1",
                             button_color=('white', '#2fa4e7'), visible=True),
                      Button("Specific Logs", font="Sans-Serif 10 bold", key="B4",
                             button_color=('white', '#2fa4e7'), visible=True),
                      Button('Delete Files', font='Sans-Serif 10 bold', key="B2",
                             button_color=('white', '#2fa4e7'), visible=True),
                      Button('Analyzer', font='Sans-Serif 10 bold', key="B6",
                             button_color=('white', '#2fa4e7'), visible=True),
                      Button('Exit', font='Sans-Serif 10 bold', key="B3",
                             button_color=('white', '#2fa4e7'), visible=True),
                      ]

    layout = [
        heading,
        listOfAllLogs,
        InputBox,
        dateBox,
        checkOutButton,
    ]

    window = Window('Windows Log Analyzer', layout=layout, size=(1300, 625))
    print('window')

    while True:
        event, values = window.read()
        print(values)
        # if event=='-B1-+MOUSE OVER+':
        #     window['-B1-'].update(button_color = ('white','#178acc'))
        # if event=='-B2-+MOUSE AWAY+':
        #     window['-B2-'].update(button_color = ('#FF0000','#FF0000'))
        if event == WIN_CLOSED or event == 'B3':
            break
        try:
            if event == 'B1':
                getFilesReady(values["LogIndex"], ' ')
            if event == 'B4':
                getFilesReady(values["LogIndex"], values['dateBox'])
        except Exception as e:
            popup(e)
        if event == 'B2':
            logScreen()
        if event == 'B5':
            detailScreen()
        if event == 'B6':
            Analyzer()

    window.close()
    return


if(flag == 1):
    homeScreen()
    b = 1
    print('it works')
if(b == 1):
    mains()
