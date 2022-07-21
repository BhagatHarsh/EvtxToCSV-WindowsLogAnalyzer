from PySimpleGUI import *

from checkLOG import deleteIT


def logScreen():
    theme('Material2')
    current_files = [i for i in os.listdir(
        os.getcwd()) if not i.endswith(('.py','.jpeg','.png'))]
    heading = [Text('Contents of the Current Folder are given below :')]
    listoffiles = [Listbox(values=[(' ' + str(i+1) + ')  ') + current_files[i]
                           for i in range(len(current_files))], size=(150, 5), key='list')]

    InputBox = [Text('Enter the index'),
                Input()]
    deletebutton = [Button("Delete", key='Input')]
    layout = [
        heading,
        listoffiles,
        InputBox,
        deletebutton,
    ]

    window = Window('Log Window', layout=layout, size=(700, 200))

    while True:
        event, values = window.read()
        print(values)

        if event == WIN_CLOSED or event == 'B2':
            break
        if event == "Input":
            try:
                deleteIT(os.path.join(
                    os.getcwd(), current_files[int(values[0])-1]))
                current_files.remove(current_files[int(values[0])-1])
                window["list"].update(values=[(' ' + str(i+1) + ')  ') +
                                              current_files[i] for i in range(len(current_files))])
            except Exception as e:
                popup(e)
    window.close()
    return

# logScreen()