from psychopy import visual 
from psychopy import core,event
import os.path
import pandas as pd

import random

###################################################################################################
def runexp(filename, timer, win, writer, resdict, runtime,dfile,seed):
    writera = writer[1]
    writer = writer[0]
    random.seed(seed)
    
    resdict['Timepoint'], resdict['Time'] = 'Movie Task Start', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    
    # user can update instructions for task here if required.
    instructions =      """You are about to watch a clip from a movie.
                        """
    start_screen = """Following this, there will be a series of questions related to your ongoing thoughts, and the content of the clip. 
                    \nPress enter/return when you are ready to begin.
                    """

    # create text stimuli to be updated for start screen instructions.
    stim = visual.TextStim(win, "", color = [-1,-1,-1], wrapWidth = 1300, units = "pix", height=40)

    # update text stim to include instructions for task. 
    stim.setText(instructions)
    stim.draw()
    win.flip()
    # Wait for user to press enter to continue. 
    event.waitKeys(keyList=(['return']))

    # update text stim to include start screen for task. 
    stim.setText(start_screen)
    stim.draw()
    win.flip()
    
    # Wait for user to press enter to continue. 
    event.waitKeys(keyList=(['return']))
    
    # Write when it's initialized
    resdict['Timepoint'], resdict['Time'] = 'Movie Init', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    
    # Create two different lists of videos for trial 1 and trial 2. 
    
    trialvideo = os.path.join(os.getcwd(), 'taskScripts//resources//Movie_Task//videos') + "/" + filename

    trialname = "Movie Task-" + trialvideo.split(".")[0].split("/")[-1]
    


    
    # present film using moviestim
    resdict['Timepoint'], resdict['Time'],resdict['Auxillary Data'] = 'Movie Start', timer.getTime(), filename
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'],resdict['Auxillary Data'] = None,None,None
    

     
    mov = visual.MovieStim3(win, trialvideo, size=(1920, 1080), flipVert=False, flipHoriz=False, loop=False)
    while mov.status != visual.FINISHED:
        mov.draw()
        win.flip()

    return trialname
