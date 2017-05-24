import logging
from Trotter import *
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)



# Global vars
locsVisited = [] # List of last 7 locations visited
seqNum = [0] # Sequence number for GUI commands
listOptions = []
selOption = [1]
# Add context variable to identify the function asking for additional info
#session.attributes['numbers'] = numbers[::-1]  # reverse


@ask.launch
def welcome():
    seqNum[0] = 0
    GUICom("about", seqNum[0])
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.session_ended
def session_ended():
    return statement("")


@ask.intent("AMAZON.HelpIntent")
def help():
    seqNum[0] = (seqNum[0] + 1) % 3
    GUICom("help", seqNum[0])
    help_msg = render_template('help')
    help_rep_msg = render_template('help_rep')
    return question(help_msg).reprompt(help_rep_msg)


@ask.intent("VoiceHelpIntent")
def helpVoice():
    seqNum[0] = (seqNum[0] + 1) % 3
    GUICom("help", seqNum[0])
    help_msg = render_template('help_voice')
    help_rep_msg = render_template('help_rep')
    return question(help_msg).reprompt(help_rep_msg)


@ask.intent("GestureHelpIntent")
def helpGest():
    seqNum[0] = (seqNum[0] + 1) % 3
    GUICom("help", seqNum[0])
    help_msg = render_template('help_gesture')
    help_rep_msg = render_template('help_rep')
    return question(help_msg)


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement('OK')


@ask.intent("AboutIntent")
def about():
    about_msg = render_template('about')
    seqNum[0] = (seqNum[0] + 1) % 3
    GUICom("about", seqNum[0])
    return statement(about_msg)

@ask.intent("HistoryIntent")
def history():
    locsLen = len(locsVisited)
    hist_msg = "You have visited "
    if(locsLen == 0):
        no_hist_msg = render_template('no_hist')
        return question(no_hist_msg).reprompt("")
    else:
        for num in xrange(locsLen-1, 0, -1):
            hist_msg += locsVisited[num] + ", "
        hist_msg += "and " + locsVisited[0]
    #return question(hist_msg).reprompt("")
    return statement(hist_msg)


@ask.intent("IntroIntent")
def intro():
    intro_msg = render_template('intro')
    return statement(intro_msg)


@ask.intent("OutroIntent")
def outro():
    outro_msg = render_template('outro')
    return statement(outro_msg)


@ask.intent("TrottersIntent")
def trotters():
    seqNum[0] = (seqNum[0] + 1) % 3
    GUICom("globetrotters", seqNum[0])
    globetrotters_msg = render_template('globetrotters')
    #return question(globetrotters_msg).reprompt("")
    return statement(globetrotters_msg)



@ask.intent("DetailsIntent")
def details():
    if(len(listOptions) < 1):
        return question("where do you want to visit?")
    else:
        seqNum[0] = (seqNum[0] + 1) % 3
        GUICom("details", seqNum[0])
        global selOption
        details_msg = listOptions[selOption[0] - 1]['MoreInfo']
        return statement(details_msg)


@ask.intent("ViewIntent")
def view():
    seqNum[0] = (seqNum[0] + 1) % 3
    GUICom("switchView", seqNum[0])
    return statement("Switching map view")


@ask.intent("ZoomIntent", default={'zoomOpt': 'in'})
def zoom(zoomOpt):
    # AVS interprets 'in' as 'N' frequently
    if(zoomOpt == "N"):
        zoomOpt = "in"
    if(zoomOpt == "in" or zoomOpt == "out" or zoomOpt == "reset"):
        seqNum[0] = (seqNum[0] + 1) % 3
        GUICom(zoomOpt, seqNum[0])
        return question("Zooming {}".format(zoomOpt))
    else:
        return question("I did not get that. Please say again")


@ask.intent("RotateIntent", default={'rotateopt': 'none'})
def rotate(rotateopt):
    rotateopt = rotateopt.lower()
    # stores valid rotate responses
    validOpts = ('left', 'west', 'right', 'east', 'up', 'north', 'down', 'south', \
        'fast', 'faster', 'quicker', 'slow', 'slower', 'slowly', 'stop')
    for opt in validOpts:
        if(opt == rotateopt) : 
            globeCntrl(rotateopt)
            if(rotateopt == 'stop'):
                return statement('Rotation stopped')
            else:
                return statement('Rotating {}'.format(rotateopt))
    rotate_msg = render_template('rotate', invOpt=rotateopt)
    return question(rotate_msg)
        


# Add inside @ask.intent if param_name != slot_name: 
#, mapping={'param_name': 'slot_name'} 
@ask.intent("GoToIntent", default={'location': 'None'}) 
def goto(location):
    if(location == "None") : 
        return question("I did not get that. Please say the location again.")
    print("GoTo: looking up {}".format(location))
    # Get list of locations that meet the search query
    global listOptions
    listOptions = getAll(location)
    numOpts = len(listOptions) 
    # Reset selected location to 1st location in list
    global selOption
    selOption[0] = 1
    # Check if result is empty, one, or multiple locations
    try: 
        # List available Keys from results
        print("GoTo Avail Keys: {}".format(listOptions[0].keys()))
    except:
        print("GoTo: Location not found")
        loc_msg = render_template('no_loc')
        return question(loc_msg)

    if(numOpts == 1):
        loc_msg = listOptions[0]['Message']
    else:
        # handles case of multiple locations
        loc_msg = listOptions[0]['Message']
        loc_msg += ". To hear alternate locations say, what are my options?"
    
    if(len(locsVisited) > 6):
        # maintain history buffer of 7 locations
        del locsVisited[0]
        locsVisited.append(location)
    else:
        locsVisited.append(location)
    # Update GUI
    seqNum[0] = (seqNum[0] + 1) % 3
    GUI("map", seqNum[0], listOptions[0]['FullName'])
    globeCntrl(str(listOptions[0]['Lng']))
    loc_rep_msg = render_template('loc_rep')
    return question(loc_msg).reprompt(loc_rep_msg)    



@ask.intent("SelOptionIntent", default={'listOpt': 0})
def selectOpt(listOpt):
    # Check for selection of valid option
    try: 
        listOpt = int(listOpt)
    except:
        return question("please select a valid option")
    numOpts = len(listOptions)
    if(numOpts < 2):
        return statement("there are no options to choose from")
    elif(listOpt > numOpts or listOpt < 1):
        list_msg = render_template('valid_options', listOpt=numOpts)
        return question(list_msg)
    locName = listOptions[listOpt - 1]['Name']

    # Update history
    if(len(locsVisited) > 6):
        # maintain history buffer of 7 locations
        del locsVisited[0]
        locsVisited.append(locName)
    else:
        locsVisited.append(locName)

    # Update user selected location from list
    global selOption
    selOption[0] = listOpt
    # Update GUI
    seqNum[0] = (seqNum[0] + 1) % 3
    GUI("Option{}".format(listOpt), seqNum[0], listOptions[listOpt - 1]['FullName'])
    globeCntrl(str(listOptions[listOpt - 1]['Lng']))
    return question(listOptions[listOpt - 1]['Message'])




@ask.intent("ListOptionsIntent")
def listOpts():
    numOpts = len(listOptions)
    if(numOpts < 2):
        return statement("there are no options to choose from")
    else:
        loc_msg = " "
        for i in range(numOpts):
            loc_msg += " For {} say, select option {}.".format(listOptions[i]['FullName'], i + 1) 
        seqNum[0] = (seqNum[0] + 1) % 3
        GUICom("ShowList", seqNum[0])
        return question(loc_msg)







if __name__ == '__main__':
    app.run(debug=True)
    








