#Connect More
A multiplayer spin on "Connect Four"!

Allows for 2 to 6 players, and *chains* (a string of 3 or more tokens) score more points the longer they get!

##Usage
Requires at least Python 3. (only tested on 3.5). All dependencies needed are included in the main folder. Run:

>python runme.py

then enter either *text* (for a simple text interface), or *web* (for a prettier web UI).

##Implementation Notes
This is my first app in quite a few years, and first Python app since some simple "data structures" assignments in my Comp. Sci. university days. Please be kind :P.

All code written from scratch, with the exception of bottle.py, which I chose to serve the main web page and handle the simple web requests because it's contained within a single file (and the usage is pretty intuitive... basically just maps some URLs to my functions). I probably should have just written the entire application in html/javascript, but I'd been playing around with Python for an online course (https://www.udacity.com/course/artificial-intelligence-for-robotics--cs373), which reminded me how much I had liked Python when we first met, so I wanted to get some more practice with it.

Oh, and I use jQuery in the web interface too.

###Possible issue running Web UI...
The web UI uses relative paths to the static files, which Bottle warns may be an issue as the 'current folder' may not always be the same as the project folder. It works for me on Windows 10 when run from the main project folder, but I haven't tested on other platforms. If it fails for you, try running from the main project folder and if it still doesn't work, you can change the "root" parameters in the ui_web.py files to work in your environment.


##File Listing
File | Description
--- | ---
runme.py | the main 'executable'
game_logic.py | the main logic and state for a game
game_logic_test.py | unit tests for game_logic
ui_text.py | UI for simple text only interface
ui_web.py | UI for a prettier web interface
bottle.py | the single file for the Bottle framework
\web | directory with all static web files. It's contents are fairly self explanatory
