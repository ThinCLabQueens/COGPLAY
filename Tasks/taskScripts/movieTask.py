from psychopy import visual
from psychopy import core, event
import os.path
import pandas as pd
from taskScripts import ESQ
import random
import time


###################################################################################################
def runexp(filename, timer, win, writer, resdict, runtime, dfile, seed):
    writera = writer[1]
    writer = writer[0]
    random.seed(seed)

    resdict["Timepoint"], resdict["Time"] = "Movie Task Start", timer.getTime()
    writer.writerow(resdict)
    resdict["Timepoint"], resdict["Time"] = None, None

    # user can update instructions for task here if required.
    instructions = f"""Please ask the attending researcher to load:\n{filename}"""
    start_screen = """While playing, the screen will at times prompt you to answer a series of questions related to your ongoing thoughts.
                    \nPress enter/return when you are ready to begin.
                    """
    stop_screen = (
        """Please pause the game, and press enter/return on the tablet to continue."""
    )
    game_screen = """Please play the game on the screen"""

    transition_text = """Please resume playing the game on the screen"""
    # create text stimuli to be updated for start screen instructions.
    stim = visual.TextStim(win, "", color=[-1, -1, -1], pos=(0, 0))

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
    resdict["Timepoint"], resdict["Time"] = "Movie Init", timer.getTime()
    writer.writerow(resdict)
    resdict["Timepoint"], resdict["Time"] = None, None

    # Create two different lists of videos for trial 1 and trial 2.

    trialname = "Game Task-" + filename

    # present film using moviestim
    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
        "Game Start",
        timer.getTime(),
        filename,
    )
    writer.writerow(resdict)
    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = None, None, None

    def select_numbers():
        def generate_valid_numbers():
            return [random.uniform(3, 8) for _ in range(100)]

        while True:
            valid_numbers = generate_valid_numbers()
            random.shuffle(valid_numbers)
            selected = valid_numbers[:3]
            if (
                abs(selected[0] - selected[1]) >= 2
                and abs(selected[0] - selected[2]) >= 2
                and abs(selected[1] - selected[2]) >= 2
            ):
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
    while newtimer.getTime() < 600:
        if i < 3:
            if newtimer.getTime() > newnumbers[i]:
                win.color = "#84ff7c"
                win.flip()
                stim.setText(stop_screen)
                stim.draw()
                win.flip()
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
        stim.setText(game_screen)
        stim.draw()
        win.flip()

    return trialname
