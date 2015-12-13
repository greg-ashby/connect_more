mode = input("What mode would you like to play ('text' or 'web')? ")
modes = ["text", "web", "desktop"]

if mode in modes:
    if mode == modes[0]:
        import ui_text
        ui_text.run()
    elif mode == modes[1]:
        import ui_web
        ui_web.run()
    else:
        print("Option not yet implemented. Developer got lazy. :)")
else:
    print("unknown option, exiting...")
