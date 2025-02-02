# Main script written by Ian Goodall-Halliwell. Subscripts are individually credited. Many have been extensively modified, for better or for worse (probably for worse o__o ).
# Original script modified for COGPLAY by Louis Chitiz

from psychopy import core, visual, gui, event
import pandas as pd
import numpy as np
import time
import csv
import sys
import yaml
import string

# from Tasks.taskScripts import memoryTask
# import taskScripts
from taskScripts import ESQ, gameTask
import os
import random

os.chdir(os.path.dirname(os.path.realpath(__file__)))
if not os.path.exists(os.path.join(os.getcwd(), "log_file")):
    os.mkdir(os.path.join(os.getcwd(), "log_file"))


# This class is responsible for creating and holding the information about how each task should run.
# It contains the number of repetitions and a global runtime variable.
# It also contains the subject ID, and will eventually use the experiment seed to randomize trial order.
class metadatacollection:
    def __init__(self, INFO):  # , main_log_location):
        self.INFO = INFO
        # self.main_log_location = main_log_location

        # Don't really know what this is, best to leave it be probably
        self.sbINFO = "Test"

    # This opens the GUI
    def rungui(self):
        self.sbINFO = gui.DlgFromDict(self.INFO)

    # This writes info collected from the GUI into the logfile
    def collect_metadata(self):
        if not self.sbINFO.OK :
            quit()
        print(self.sbINFO.data)
        if not os.path.exists(os.path.join(os.getcwd(), "log_file")):
            os.mkdir(os.path.join(os.getcwd(), "log_file"))
        f = open(
            os.path.join(
                os.getcwd()
                + "/log_file/output_log_{}_{}_full.csv".format(
                    self.sbINFO.data[2], self.INFO["Experiment Seed"]
                )
            ),
            "w",
            newline="",
        )
        fq = open(
            os.path.join(
                os.getcwd()
                + "/log_file/output_log_{}_{}.csv".format(
                    self.sbINFO.data[2], self.INFO["Experiment Seed"]
                )
            ),
            "w",
            newline="",
        )
        metawriter = csv.writer(f)
        metawriter2 = csv.writer(fq)
        metawriter.writerow(["METADATA:"])
        metawriter.writerow(self.sbINFO.inputFieldNames)
        metawriter.writerow(self.sbINFO.data)
        metawriter2.writerow(["METADATA:"])
        metawriter2.writerow(self.sbINFO.inputFieldNames)
        metawriter2.writerow(self.sbINFO.data)
        random.seed(a=int(metacoll.INFO["Experiment Seed"]))
        metawriter.writerow(["Time after setup", taskbattery.time.getTime()])
        metawriter2.writerow(["Time after setup", taskbattery.time.getTime()])
        writer = csv.DictWriter(f, fieldnames=taskbattery.resultdict)
        writer.writeheader()
        writer2 = csv.DictWriter(fq, fieldnames=taskbattery.resultdict)
        writer2.writeheader()
        f.close()
        fq.close()


# Creates a list of all the tasks, and allows you to iterate through them without closing the window
class taskbattery(metadatacollection):
    time = core.Clock()
    resultdict = {
        "Timepoint": None,
        "Time": None,
        "Is_correct": None,
        "Experience Sampling Question": None,
        "Experience Sampling Response": None,
        "Task": None,
        "Task Iteration": None,
        "Participant ID": None,
        "Response_Key": None,
        "Auxillary Data": None,
        "Assoc Task": None,
    }

    def __init__(self, tasklist, ESQtask, INFO):
        self.tasklist = tasklist
        taskbattery.ESQtask = ESQtask
        self.INFO = INFO
        self.taskexeclist = []
        self.win = visual.Window(
            size=(1920, 1280), color="white", winType="pyglet", fullscr=True
        )
        self.text = visual.TextStim(
            win=self.win,
            name="text_2",
            text="Welcome to our experiment. \n\n Please follow the instructions on-screen and notify the attending researcher if anything is unclear. \n\n We are thankful for your participation. \n\n Press <return/enter> to continue.",
            font="Arial",
            anchorHoriz="center",
            anchorVert="center",
            wrapWidth=1.3,
            ori=0,
            color="black",
            colorSpace="rgb",
            opacity=1,
            languageStyle="LTR",
            depth=0.0,
        )
        taskbattery.win = self.win

    # def initializeBattery(self):
    # for i in self.tasklist:

    def run_battery(self):
        self.text.draw(self.win)
        self.win.flip()
        time.sleep(1)
        event.waitKeys(keyList=["return"])
        self.win.flip()

        for en, i in enumerate(self.tasklist):
            os.chdir(os.getcwd())
            i.show()
            i.run()
            pp = len(self.tasklist)
            if en < len(self.tasklist):
                i.end()


# OPEN THE TRIAL FILES AND CUT THEM INTO BLOCKS


# This creates a class which feeds all the necessary information into the task functions imported from each task file
# Allows you to create different task instances, which will be useful for creating blocks (my current project)
# Saves the log file after each task. It takes some extra time, but it prevents a crash from corrupting the file
class task(taskbattery, metadatacollection):
    def __init__(
        self,
        task_module,
        main_log_location,
        backup_log_location,
        name,
        trialclass,
        runtime,
        dfile,
        esq=False,
    ):  # , trialfile, ver):
        self.main_log_location = main_log_location
        self.backup_log_location = backup_log_location  # Not yet implemented
        self.task_module = task_module  # The imported task function
        self.name = name  # A name for each task to be written in the logfile

        self.trialclass = trialclass  # Has something to do with writing task name into the logfile I think? Probably don't touch this.
        self.runtime = runtime  # A "universal" "maximum" time each task can take. Will not stop mid trial, but will prevent trial repetions after the set time in seconds
        self.esq = esq
        self.dfile = dfile
        # super.__init__()

    def initvers(self):

        incrordecr = random.choice([-1, 1])
        amnt = random.randint(5, 15)
        self.runtime = self.runtime + amnt * incrordecr
        with open(self.main_log_location, "a", newline="") as o:
            metawrite = csv.writer(o)
            metawrite.writerow(" ")
            metawrite.writerow(["Runtime Mod", (amnt * incrordecr)])

    def run(self, *args, **kwargs):
        print(args, kwargs)
        global prevname
        if not os.path.exists(self.main_log_location):
            if self.main_log_location.split(".")[1] == None:
                os.mkdir(self.main_log_location.split("/")[0])
        fr = open(self.main_log_location, "a", newline="")
        f = open((self.main_log_location.split(".")[0] + "_full.csv"), "a", newline="")
        fre = csv.writer(fr)
        r = csv.writer(f)

        writer = csv.DictWriter(f, fieldnames=taskbattery.resultdict)
        r.writerow(["EXPERIMENT DATA:", self.name])
        r.writerow(["Start Time", taskbattery.time.getTime()])
        writer2 = csv.DictWriter(fr, fieldnames=taskbattery.resultdict)
        fre.writerow(["EXPERIMENT DATA:", self.name])
        fre.writerow(["Start Time", taskbattery.time.getTime()])

        taskbattery.resultdict = {
            "Timepoint": None,
            "Time": None,
            "Is_correct": None,
            "Experience Sampling Question": None,
            "Experience Sampling Response": None,
            "Task": self.name,
            "Task Iteration": "1",
            "Participant ID": self.trialclass[1],
            "Response_Key": None,
            "Auxillary Data": None,
            "Assoc Task": None,
        }

        if self.esq == False:
            # if self.ver == 1:
            self.task_module.runexp(
                self.backup_log_location,
                taskbattery.time,
                taskbattery.win,
                [writer, writer2],
                taskbattery.resultdict,
                self.runtime,
                self.dfile,
                int(metacoll.INFO["Experiment Seed"]),
            )

        if self.esq == True:

            taskbattery.resultdict = {
                "Timepoint": None,
                "Time": None,
                "Is_correct": None,
                "Experience Sampling Question": None,
                "Experience Sampling Response": None,
                "Task": self.name,
                "Task Iteration": "1",
                "Participant ID": self.trialclass[1],
                "Response_Key": None,
                "Auxillary Data": None,
                "Assoc Task": taskbattery.prevname,
            }

            self.task_module.runexp(
                self.backup_log_location,
                taskbattery.time,
                taskbattery.win,
                [writer, writer2],
                taskbattery.resultdict,
                self.runtime,
                None,
                int(metacoll.INFO["Experiment Seed"]),
                args,
                kwargs,
            )

        f.close()
        fr.close()
        taskbattery.resultdict = {
            "Timepoint": None,
            "Time": None,
            "Is_correct": None,
            "Experience Sampling Question": None,
            "Experience Sampling Response": None,
            "Task": None,
            "Task Iteration": None,
            "Participant ID": None,
            "Response_Key": None,
            "Auxillary Data": None,
            "Assoc Task": None,
        }

        taskbattery.prevname = self.name


class taskgroup(taskbattery, metadatacollection):
    def __init__(self, tasks, instrpath):
        self.tasks = tasks
        self.instrpath = instrpath

    def show(self):
        text_inst = visual.TextStim(
            win=taskbattery.win,
            name="text_4",
            text="",
            font="Open Sans",
            pos=(0, 0),
            height=0.1,
            wrapWidth=1.3,
            ori=0.0,
            color="black",
            colorSpace="rgb",
            opacity=None,
            languageStyle="LTR",
            depth=0.0,
        )
        # try:
        #     with open(
        #         os.path.join(os.path.join(os.getcwd(), "taskScripts"), self.instrpath),
        #         newline="",
        #     ) as f:
        #         lines1 = f.read()
        # except:
        #     with open(os.path.join(os.getcwd(), self.instrpath), newline="") as f:
        #         lines1 = f.read()
        # text_inst.setText(lines1)
        # text_inst.draw()

        # taskbattery.win.flip()
        # time.sleep(1)
        # event.waitKeys(keyList=["return"])

    def run(self, *args, **kwargs):
        for taskgrp in self.tasks:
            if taskgrp == None:
                continue
            for task in taskgrp:
                print("Now initializing {}".format(task.name))
                task.initvers()
                print("Now setting up {}".format(task.name))
                print("Now running {}".format(task.name))
                task.run()
                print("Now starting ESQ for {}".format(task.name))
                print(task.backup_log_location)
                # taskbattery.ESQtask.run(videoname=task.backup_log_location)

    def end(self):
        text_inst = visual.TextStim(
            win=taskbattery.win,
            name="text_1",
            text="This is the end of the experiment \n\n Please inform the Researcher that you have finished. \n\n Thank you for your participation. \n\n Press <return/enter> to continue.",
            font="Open Sans",
            pos=(0, 0),
            height=0.1,
            wrapWidth=1.3,
            ori=0.0,
            color="black",
            colorSpace="rgb",
            opacity=None,
            languageStyle="LTR",
            depth=0.0,
        )
        text_inst.draw()
        taskbattery.win.flip()
        time.sleep(1)
        event.waitKeys(keyList=["return"])
        taskbattery.win.flip()

    def shuffle(self):
        a = self.tasks
        for a in self.tasks:
            random.shuffle(a)
        random.shuffle(self.tasks)
        print("")


### HAVE TO EXPOSE ESQ TASK TO MOVIE SCRIPT

if __name__ == "__main__":

    with open(os.path.join(os.pardir, "config.yaml"), "r") as f:
        config = yaml.safe_load(f)
    # Info Dict
    INFO = {
        "Experiment Seed": random.randint(1, 9999999),
        "Subject": "Enter Name Here",
        "Number of Games": 6
    }

    # Main and backup data file

    # Run the GUI and save output to logfile
    metacoll = metadatacollection(INFO)
    metacoll.rungui()
    metacoll.collect_metadata()
    metacoll.INFO["Block Runtime"] = 48000

    # Defining output datafile
    datafile = str(
        os.getcwd()
        + "/log_file/output_log_{}_{}.csv".format(
            metacoll.INFO["Subject"], metacoll.INFO["Experiment Seed"]
        )
    )
    datafileBackup = "log_file/testfullbackup.csv"
    if not os.path.exists("tmp"):
        os.mkdir("tmp")

    ESQTask = task(
        ESQ,
        datafile,
        datafileBackup,
        "Experience Sampling Questions",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        None,
        esq=True,
    )

    numgames = metacoll.INFO["Number of Games"]

    games = list(string.ascii_uppercase)[:numgames]

    gamedf = pd.read_csv('taskScripts/resources/Game_Task/gamelist.csv')

    gamedf['gamecode'] = np.random.permutation(gamedf['gamecode'].values)

    gamedf = gamedf[gamedf['gamecode'].isin(games)]   

    # Defining each task as a task object
    gamegroup = []
    for game in games:
        gamegroup.append(
            task(
                gameTask,
                datafile,
                game,
                "Game Task",
                metacoll.sbINFO.data,
                int(metacoll.INFO["Block Runtime"]),
                gamedf,
            )
        )

    random.shuffle(gamegroup)
    game_main = taskgroup([gamegroup], "resources/group_inst/movie_main.txt")

    fulltasklist = [game_main]

    tasks = fulltasklist

    tbt = taskbattery(tasks, ESQTask, INFO)

    tbt.run_battery()
    print("Success")
