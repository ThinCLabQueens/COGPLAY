import os
import pandas as pd
import numpy as np
import shutil
from datetime import datetime
import random
from tqdm import tqdm
import re


if os.path.exists(os.path.join(os.getcwd(),"Analysis/output.csv")):
    creation_time = os.path.getctime("Analysis/output.csv")
    creation_dt = datetime.fromtimestamp(creation_time)
    dt = creation_dt.strftime('%Y_%m_%d')
    filecode = random.randint(10000, 99999)

    shutil.move("Analysis/output.csv", "Analysis/old_output/output_" + str(dt) + "_" + str(filecode) + ".csv")

output = pd.DataFrame() 

mDES = []

for file in tqdm(os.listdir("Tasks/log_file")):
    
    ftemp = file.split('.')[0]

    if not 'full' in ftemp.split('_'):

        _,_,subject,seed = ftemp.split("_")
        subject = "subject_"+str(re.findall(r'\d+', subject)[0])


        sub_df = pd.read_csv(os.path.join("Tasks\\log_file",file), skiprows=4)

        line_dict = {}
        enum = 0
        for index, row in sub_df.iterrows():

            line_dict["subject_id"] = subject

            if row['Timepoint'] == 'Runtime Mod':
                line_dict["Runtime_mod"] = row[1]
                prev_run = row[1]

            elif row['Timepoint'] == 'ESQ':
                enum += 1

                task_name = row['Assoc Task']                    

                line_dict["Task_name"] = task_name.replace(" ","_")

                if float(row['Experience Sampling Response']) >= 1 :
                    line_dict[row['Experience Sampling Question']]=row['Experience Sampling Response']
                else:
                    line_dict[row['Experience Sampling Question']]=np.nan


            if enum == 16:
                if float(row['Experience Sampling Response']) >= 1 :
                    line_dict[row['Experience Sampling Question']]=row['Experience Sampling Response']
                else:
                    line_dict[row['Experience Sampling Question']]=np.nan

                enum = 0
                mDES.append(line_dict)

                line_dict = {'Runtime_mod':prev_run}

    else:

        continue


test_df = pd.DataFrame(mDES)

test_df = test_df[test_df.Task_name != "()"]


test_df.to_csv('Analysis/output.csv', index = False)