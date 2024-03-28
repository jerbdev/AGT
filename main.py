#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import subprocess
from datetime import datetime
import os
import pandas as pd

# Define a list of valid commands
VALID_COMMANDS = [
    "scan", "read", "find", "sesh", "train", "testing model", "push", "live",
    "new sesh", "line", "trend", "fcast", "fcast 3d", "build","summary", "corr", 
    "pred", "cleaner", "nn", "export", "export csv", "export xl", "dbconn"
]

print("")
print('AGT Live')
print('v0.1.3')
print('')
print('ctrl+z to quit                  ')
print("")

# Cleans up columns index header
def clean_data(data):
    data['Timestamp'] = pd.to_datetime(data['Timestamp'].str[0]).dt.strftime('%Y-%m-%d %H:%M:%S')
    data['MAC'] = data['MAC'].str[0]
    data['Moisture'] = data['Moisture'].str[0]
    data['Light'] = data['Light'].str[0]
    data['Temperature'] = data['Temperature'].str[0]
    data['Conductivity'] = data['Conductivity'].str[0]
    return data

while True:
    
    usrinpt = input(">>> ")
    
    if usrinpt in VALID_COMMANDS:  
        if usrinpt == "scan":
            from scan import stats
            print(stats)
        elif usrinpt == "read":
            subprocess.run(["python3", "read.py"])
        elif usrinpt == "find":
            from find import device_id
            print(device_id)
        elif usrinpt == "sesh":
            while True:
                print("Starting read session...")
                subprocess.run(["python3", "read.py"])
                time.sleep(600)

        # Neural Network Commands
        elif usrinpt == "train":
            subprocess.run(["python3", "__tools__/neural_net/modular/model.py","--from_main"])

        elif usrinpt == "testing model":
            subprocess.run(["python3", "__tools__/neural_net/modular/model-test.py","--from_main"])

        elif usrinpt == "push":
                print("Starting read session...")
                subprocess.run(["python3", "read.py"])
                subprocess.run(["python3", " __tools__/neural_net/modular/model.py","--from_main"])
        elif usrinpt == "live":
                print("Starting web interface processes...")
                subprocess.run(["python3", "web_ui/app.py"])
                time.sleep(600)

        # !! CAUTION !!
        # Session data reset commands
        elif usrinpt == "new sesh":
            confirm = input("Are you sure you want to start a new session? This will clear any current session data. (Y/N)? ")
            if confirm == "Y":
                print("Deleting previous session data...")
                subprocess.run(["rm", "-rf", "sesh.json"])
                while True:
                    print("Starting new read session...")
                    subprocess.run(["python3", "read.py"])
                    time.sleep(600)
            else:
                print("Cancelling new session...")
                
# Sesh.json source for below commands
        
        # Visualization Commands
        elif usrinpt == "line":
            subprocess.run(["python3", "__tools__/plot/line.py"]) # Altered for multi-device use
        elif usrinpt == "trend":
            subprocess.run(["python3", "__tools__/plot/trends.py"])
        elif usrinpt == "fcast":
            subprocess.run(["python3", "__tools__/plot/forecast.py"])
        elif usrinpt == "fcast 3d":
            subprocess.run(["python3", "__tools__/plot/data3d.py"])
        elif usrinpt == "summary":
            subprocess.run(["python3", "__tools__/summary.py"])           

        # Analysis commands
        elif usrinpt == "corr":
            print("Correlation Analysis:")
            subprocess.run(["python3", "__tools__/plot/corr.py"])
        elif usrinpt == "pred":
            subprocess.run(["python3", "__tools__/neural_net/arima.py"])
        elif usrinpt == "cleaner":
            subprocess.run(["python3", "__tools__/cleaner.py"])
        elif usrinpt == "nn":
            subprocess.run(["python3", "__tools__/neural_net/nn.py", "--from_main"])
        
        # Export commands

        elif usrinpt == "export":
            # reading the file
            data = pd.read_json("sesh.json")
            cleaned_data = clean_data(data)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            if not os.path.exists("__files__/export"):
                os.makedirs("__files__/export")
            data.to_json(f'__files__/export/{timestamp}.json')
            print('')
            print('Current session saved as JSON in exports folder.')
            print('')


        elif usrinpt == "export csv":
            # reading the file
            data = pd.read_json("sesh.json")
            cleaned_data = clean_data(data)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            if not os.path.exists("__files__/export"):
                os.makedirs("__files__/export")
            data.to_csv(f'__files__/export/{timestamp}.csv')
            print('')
            print('Current session saved as CSV in exports folder.')
            print('')
        
        elif usrinpt == "export xl":
            # reading the file
            data = pd.read_json("sesh.json")
            cleaned_data = clean_data(data)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            if not os.path.exists("__files__/export"):
                os.makedirs("__files__/export")
            data.to_excel(f'__files__/export/{timestamp}.xlsx')
            print('')
            print('Current session saved as CSV in exports folder.')
            print('')
            
# AGT_DB.SENSOR_READINGS DATA SOURCE FOR BELOW COMMANDS
            
        elif usrinpt == "build":
            subprocess.run(["python3","/home/jeremy/Documents/AGT/__tools__/report/build_report.py"])
        
        # Database connection commands
        elif usrinpt == "dbconn":
            subprocess.run(["python3", "__files__/db_connect.py"])

        # All else fails
    else:
        print("Invalid command!")

    # Attempt to evaluate or execute the input as Python code
    try:
        # Check if the input is a valid expression or statement
        compiled_code = compile(usrinpt, "<string>", "eval")
        result = eval(compiled_code)
        print(result)
    except SyntaxError:
        try:
            # Check if the input is a valid statement block
            compiled_code = compile(usrinpt, "<string>", "exec")
            exec(compiled_code)
        except Exception as e:
            print("ERROR:", e)
    except Exception as e:
        print("ERROR:", e)