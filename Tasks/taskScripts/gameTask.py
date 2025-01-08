from psychopy import visual
from psychopy import core, event, sound
import os.path
import pandas as pd
from taskScripts import ESQ
import random
import time
import pandas as pd


###################################################################################################
def runexp(gamenum, timer, win, writer, resdict, runtime, dfile, seed):
    writera = writer[1]
    writer = writer[0]
    random.seed(seed)
    print(os.getcwd())
    notification_sound = sound.Sound('taskScripts/resources/Game_Task/notif.wav')  # Replace 'notification.wav' with your audio file path
    
    # filename = dfile.loc[dfile['gamecode'] == gamenum, 'title']

    filename = dfile[dfile.gamecode==gamenum].title.item()

    gameinstr = dfile[dfile.gamecode==gamenum].shorthand.item().lower() + ".txt"
    
    resdict["Timepoint"], resdict["Time"] = "Game Task Start", timer.getTime()
    writer.writerow(resdict)
    resdict["Timepoint"], resdict["Time"] = None, None

    # user can update instructions for task here if required.
    instructions = f"""Please ask the attending researcher to load:\n\n{filename}"""

    start_screen = """While playing, the screen will at times prompt you to answer a series of questions related to your ongoing thoughts.
                    \n\nPress enter/return when you are ready to begin.
                    """
    stop_screen = (
        """Please pause the game, and press enter/return on the tablet to continue."""
    )

    try:
        with open(os.path.join(os.getcwd(),"resources/Game_Task/game_controls/" + gameinstr), encoding = 'utf8') as f:
            controls = f.read()

        with open(os.path.join(os.getcwd(),"resources/Game_Task/game_controls/" + gameinstr), encoding = 'utf8') as fp:
            numlines = len(fp.readlines())

    except:
        with open(os.path.join(os.getcwd(),"taskScripts/resources/Game_Task/game_controls/" + gameinstr), encoding = 'utf8') as f:
            controls = f.read()

        with open(os.path.join(os.getcwd(),"taskScripts/resources/Game_Task/game_controls/" + gameinstr), encoding = 'utf8') as fp:
            numlines = len(fp.readlines())

    
    if numlines <= 10 :
        game_screen = visual.TextStim(win, "", color=[-1, -1, -1], pos = (0, 0), alignText='center', wrapWidth = 1.3)

    else:
        instrheight = 1/numlines
        game_screen = visual.TextStim(win, "", color=[-1, -1, -1], pos = (0, 0), height = instrheight, alignText='center', wrapWidth = 1.3)

    transition_text = """Please resume playing the game on the screen"""

    # create text stimuli to be updated for start screen instructions.
    stim = visual.TextStim(win, "", color=[-1, -1, -1], pos=(0, 0), alignText='center', anchorVert='center', wrapWidth = 1.3)

    # update text stim to include instructions for task.
    stim.setText(instructions)
    stim.draw()
    win.flip()
    time.sleep(1)
    # Wait for user to press enter to continue.
    event.waitKeys(keyList=(["return"]))

    # update text stim to include start screen for task.
    stim.setText(start_screen)
    stim.draw()
    win.flip()
    time.sleep(1)
    # Wait for user to press enter to continue.
    event.waitKeys(keyList=(["return"]))

    # Write when it's initialized
    resdict["Timepoint"], resdict["Time"] = "Game Init", timer.getTime()
    writer.writerow(resdict)
    resdict["Timepoint"], resdict["Time"] = None, None

    # Create two different lists of videos for trial 1 and trial 2.
    trialname = filename

    # present film using moviestim
    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
        "Game Start",
        timer.getTime(),
        filename
    )
    writer.writerow(resdict)
    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = None, None, None

    def generate_valid_numbers():
            return [random.uniform(3, 8) for _ in range(100)]

    def select_numbers(numprobes=2):
        
        while True:
            valid_numbers = generate_valid_numbers()
            random.shuffle(valid_numbers)
            selected = valid_numbers[:numprobes]
            # if (
            #     abs(selected[0] - selected[1]) >= 2
            #     and abs(selected[0] - selected[2]) >= 2
            #     and abs(selected[1] - selected[2]) >= 2
            # ):
            if abs(selected[0] - selected[1]) >= 2 :
                return selected

    selected_numbers = select_numbers()
    selected_numbers = sorted([x * 60 for x in selected_numbers])

    newnumbers = []
    for en, s in enumerate(selected_numbers):
        if en == 0:
            newnumbers.append(s)
            continue
        newnumbers.append(selected_numbers[en] - selected_numbers[en - 1])

    finaltimer = 600 - selected_numbers[-1]
    i = 0
    newtimer = core.Clock()
    tasktimer = core.Clock()
    while newtimer.getTime() < 420:
        if i < 2:
            if newtimer.getTime() > newnumbers[i]:
                win.color = "#84ff7c"
                win.flip()
                stim.setText(stop_screen)
                stim.draw()
                win.flip()
                notification_sound.play()
                event.waitKeys(keyList=(["return"]))
                win.color = "white"
                win.flip()

                resdict["Assoc Task"] = None
                resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
                    f"ESQ {i + 1}",
                    timer.getTime(),
                    selected_numbers[i],
                )
                writer.writerow(resdict)
                resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
                    None,
                    None,
                    None,
                )

                writera.writerow({'Timepoint':'EXPERIMENT DATA:','Time':'Experience Sampling Questions'})
                writera.writerow({'Timepoint':'Start Time','Time':timer.getTime()})

                ESQ.runexp(
                    None,
                    timer,
                    win,
                    [writer, writera],
                    resdict,
                    None,
                    None,
                    None,
                    movietype=trialname,
                )
                i += 1
                subTimer = core.Clock()
                while subTimer.getTime() < 5:
                    stim.setText(transition_text)
                    stim.draw()
                    win.flip()
                newtimer.reset()
        elif newtimer.getTime() > finaltimer:
            break
        game_screen.setText(controls)
        game_screen.draw()
        win.flip()

    win.color = "#84ff7c"
    win.flip()
    stim.setText(stop_screen)
    stim.draw()
    win.flip()
    notification_sound.play()
    event.waitKeys(keyList=(["return"]))
    win.color = "white"
    win.flip()

    resdict["Assoc Task"] = None
    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
        f"ESQ {i + 1}",
        timer.getTime(),
        tasktimer.getTime(),
    )

    writer.writerow(resdict)
    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
        None,
        None,
        None,
    )

    writera.writerow({'Timepoint':'EXPERIMENT DATA:','Time':'Experience Sampling Questions'})
    writera.writerow({'Timepoint':'Start Time','Time':timer.getTime()})

    ESQ.runexp(
        None,
        timer,
        win,
        [writer, writera],
        resdict,
        None,
        None,
        None,
        movietype=trialname,
    )

    return trialname
