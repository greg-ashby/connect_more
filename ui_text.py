import game_logic as gl

def run():
    """
    runs a simple text interface version of Connect More
    """

    num_players = 0
    while not (2 <= num_players <= 6):
        try:
            prompt = "\nPlease enter the number of players (2 - 6)"
            num_players = int(input(prompt))
        except:
            print("Invalid Input!")

    game = gl.ConnectMore(num_players)

    while(game.empty_squares > 0):
        print(game)

        try:
            prompt = "\nPlayer #" + str(game.current_player) + \
                " - please enter the column number to play in: "
            col = int(input(prompt))

            if 1 <= col <= game.width:
                game.play(col)
            else:
                print("invalid column #")

        except gl.FullColumnError:
            print("Column Full - please choose another!")
        except Exception as e:
            print("invalid input!")

    winners = game.get_leaders()
    print(game)
    if(len(winners) > 1):
        print("TIE GAME! Players:", ', '.join([str(x) for x in winners]), "all win!!!")
    else:
        print("Player " + str(winners[0]) + " wins!!!")
