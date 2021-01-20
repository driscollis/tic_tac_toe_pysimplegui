import io

import PySimpleGUI as sg
from PIL import Image


def check_if_won(ways_to_win):
    """
    Check if anyone has won yet
    """
    won = False
    tied = False
    winner = "Tie Game!"
    for btn_one, btn_two, btn_three in ways_to_win:
        meta = [btn_one.metadata, btn_two.metadata, btn_three.metadata]
        if None in meta:
            continue
        if meta.count(meta[0]) == len(meta):
            winner = f'{meta[0]} won!'
            mark_win([btn_one, btn_two, btn_three])
            won = True
            
    # Check if tied game
    data = []
    for row in ways_to_win:
        for button in row:
            data.append(button.metadata)
    if None not in data:
        tied = True
        
    if won or tied:
        restart = play_again(winner)
        if restart == 'quit':
            # Quit game
            return 'quit'
        else:
            # Restart game
            return True
    # Keep playing
    return False


def get_ways_to_win(buttons):
    """
    Returns a list of methods to win the game
    """
    horizontal_ways_to_win = [[buttons[0][0], buttons[1][0], buttons[2][0]],
                              [buttons[0][1], buttons[1][1], buttons[2][1]],
                              [buttons[0][2], buttons[1][2], buttons[2][2]]
                              ]
    vertical_ways_to_win = [[buttons[0][0], buttons[0][1], buttons[0][2]],
                            [buttons[1][0], buttons[1][1], buttons[1][2]],
                            [buttons[2][0], buttons[2][1], buttons[2][2]]
                            ]
    diagonal_ways_to_win = [[buttons[0][0], buttons[1][1], buttons[2][2]],
                            [buttons[0][2], buttons[1][1], buttons[2][0]]
                            ]
    return horizontal_ways_to_win + vertical_ways_to_win + diagonal_ways_to_win


def mark_win(buttons):
    """
    Mark the winning buttons with a different background color
    """
    for button in buttons:
        button.update(button_color=['green', 'green'])


def play_again(player):
    """
    Ask the user if they want to play again or quit
    """
    layout = [
        [sg.Text(f"{player} Do you want to play again or Quit?")],
        [sg.Button("Restart", key="restart"),
         sg.Button("Quit", key="quit")]]
    window = sg.Window("Play Again?", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event:
            choice = event
            break
    window.close()
    return choice


def reset_game(buttons):
    """
    Reset the game to play again
    """
    bio = io.BytesIO()
    image = Image.open("blank.png")
    image.save(bio, format='PNG') 
    for row in buttons:
        for button in row:
            button.update(image_data=bio.getvalue(),
                          button_color=['white', 'white'])
            button.metadata = None


def update_game(button, player):
    """
    Update the game
    """
    original_player = player
    if player == 'X':
        filename = "X.jpg"
        player = "O"
    else:
        filename = "O.jpg"
        player = "X"
    
    bio = io.BytesIO()
    image = Image.open(filename)
    image.save(bio, format='PNG') 
    
    if not button.metadata:
        button.update(text=player, image_data=bio.getvalue())
        button.metadata = original_player
        return player
    # If the user clicks on a location that has already been played
    # don't change players
    button.metadata = player
    return original_player


def main():
    """
    Create GUI and manage UI events
    """
    buttons = [[sg.Button(size=(7, 5), button_text=f'({row} {col})', key=(row, col), 
                          button_color=("white", "white"), 
                         image_filename="BLANK.png") for row in range(3)]
               for col in range(3)]
    window = sg.Window("Tic-Tac-Toe", buttons)
    ways_to_win = get_ways_to_win(buttons)
    
    player = 'X'
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        print(event)
        if isinstance(event, tuple):
            player = update_game(window[event], player)
            restart = check_if_won(ways_to_win)
            if restart == True:
                print("Restarting")
                player = 'X'
                reset_game(buttons)
            elif restart == "quit":
                break
    
    window.close()


if __name__ == "__main__":
    main()