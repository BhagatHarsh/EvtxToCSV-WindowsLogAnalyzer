from PySimpleGUI import *


detail = '''[Button Details]
1) All Logs - Generates a CSV file containing all the event logs
2) Specific Logs - Generates a CSV file containing all the event logs of that specific date
3) Delete Files - allows the user to deleted unwanted files from the folder
4) Analyzer - counts the errors/types of a Generated CSV file'''

def detailScreen():

    theme('Material2')

    heading = [Text('Info dialog box', font='Sans-Serif 16 bold underline')]
    Details = [Text(detail)]
    exitButton = [Button("Exit")]
    layout = [
        heading,
        Details,
        exitButton,
    ]

    window = Window('Info Window', layout=layout, size=(550, 175))

    while True:
        event, values = window.read()
        print(values)

        if event == WIN_CLOSED or event == 'B2':
            break
        if event == 'Exit':
            break

    window.close()
    return
# detailScreen()