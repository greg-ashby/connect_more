import game_logic as gl
from bottle import route, run, static_file

#this is kinda bad using a global like this, BUT...
# 1) I didn't want to make this complicated and get into authentication & sessions
# 2) It's just a toy and meant to run stand alone as a local web app... it'd
#      need some work to make it suitable to run on an actual web server with
#      multiple clients
# so this is sufficient for the current purpose
game = None

@route('/')
def index():
    return static_file("game.html", root="./web")

@route('/static/<file_name>')
def static(file_name):
    return static_file(file_name, root="./web")

# NOTE: I could in theory serve the images from the above static route as well
# by using /static/<file_name:path> and refering to /static/images/ in the
# browser, but since adding the 'path' filter allows the 'file_name' input to
# contain '/', I wasn't sure how Bottle would handle file_names with '../'
# and didn't want to get into security issues like ensuring you can't traverse
# folders via the web app. Not sure if it would be an issue, but wanted to keep
# it simple and only except file names with no '/'s
@route('/images/<file_name>')
def images(file_name):
    return static_file(file_name, root="./web/images")

# will always reset the current game with a new game, which is fine in this case
@route('/create/<num_players:int>')
def create_game(num_players):
    global game
    game = gl.ConnectMore(num_players)
    return game.to_json()


@route('/play/<col_num:int>')
def play(col_num):
    global game
    try:
        #don't need to error check here since both the UI and Game Logic will
        game.play(col_num)
        return game.to_json()
    except gl.FullColumnError:
        return '{"error": "Column is full, please select another"}'
    except gl.GameOverError:
        return '{"error": "Game is already over"}'
    except:
        return '{"error": "Unknown error occured. Sorry about that."}'

print("PLEASE OPEN YOUR BROWSER TO THE PROVIDED URL TO PLAY!!!")
