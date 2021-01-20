import PySimpleGUI as sg


def main():
    layout = [[sg.Button(size=(10, 6), key=(row, col), button_color=("white", "white"), 
                         image_filename="BLANK.png") for row in range(3)]
               for col in range(3)]
    window = sg.Window("Tic-Tac-Toe", layout)
    
    player = 'X'
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
    window.close()


if __name__ == "__main__":
    main()