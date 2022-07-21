from PySimpleGUI import *

from checkLOG import SendEmail


def emailscreen(subject, msgstr, fileName):
    theme('Material2')

    heading = [Text('Email dialog box', font='Sans-Serif 16 bold underline')]

    InputBox = [Text('Enter your Email:- '),
                Input(key='EmailIndex')]
    Emailbutton = [Button("Send Mail", key='SM')]
    layout = [
        heading,
        InputBox,
        Emailbutton,
    ]

    window = Window('Email Window', layout=layout, size=(450, 100))

    while True:
        event, values = window.read()
        print(values)

        if event == WIN_CLOSED or event == 'B2':
            break
        if event == 'SM':
            try:
                SendEmail(values['EmailIndex'], subject, msgstr, fileName)
            except Exception as e:
                popup(e)

    window.close()
    return
