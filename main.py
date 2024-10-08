#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import subprocess
from datetime import datetime
import os
import pandas as pd

# Define a list of valid commands
VALID_COMMANDS = [
    "scan", "read", "find", "trend", "update", "sesh", "train", "testing model", "push", "live",
    "new sesh", "avg", "cluster", "full anal", "fcast", "fcast 3d", "build","summary", "corr", 
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
    
    # Perform a scan for compatible BLE devices
    if usrinpt in VALID_COMMANDS:  
        if usrinpt == "scan":
            from scan import stats
            print(stats)

        # Runs read.py
        elif usrinpt == "read":
            subprocess.run(["python", "read.py"])
        elif usrinpt == "find":
            from find import device_id
            print(device_id)

        # Begins a proper data collection session. Pings every 10 minutes.
        elif usrinpt == "sesh":
            while True:
                print("Starting read session...")
                subprocess.run(["python", "read.py"])
                time.sleep(600)

        # Update current sesh.json with most recent sensor data
        elif usrinpt == "update":
            subprocess.run(["python", "files/mini_insert.py"])

        # Neural Network Commands

        # Train prediction model with data range set in model.py
        elif usrinpt == "train":
            subprocess.run(["python", "tools/neural_net/modular/model.py","--from_main"])

        # Train prediction model with data range set in model.py
        elif usrinpt == "cluster":
            subprocess.run(["python", "tools/auto-cluster.py","--from_main"])


        # not sure what testing does, Its too early to think
        elif usrinpt == "testing model":
            subprocess.run(["python", "tools/neural_net/modular/model-test.py","--from_main"])

        # Push a record to sesh.py and immediately run the prediction model
        elif usrinpt == "push":
                print("Starting read session...")
                subprocess.run(["python", "read.py"])
                subprocess.run(["python", " tools/neural_net/modular/model.py","--from_main"])

        # Start Live Session
        elif usrinpt == "live":
                print("Starting web interface processes...")
                subprocess.run(["python", "web_ui/app.py"])
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
                    subprocess.run(["python", "read.py"])
                    time.sleep(600)
            else:
                print("New session cancelled.")
        
        # Compare averages, showing trends, between sensor readings (accross all devices) and
        elif usrinpt == "avg":
            subprocess.run(["python", "tools/plot/avg.py"]) # Altered to process test and control data
        elif usrinpt == "trend":                                
            subprocess.run(["python", "tools/plot/trends.py"]) # Altered to process test and control data
        elif usrinpt == "fcast":
            subprocess.run(["python", "tools/plot/forecast.py"])
        elif usrinpt == "fcast 3d":
            subprocess.run(["python", "tools/plot/data3d.py"])
        elif usrinpt == "summary":
            subprocess.run(["python", "tools/summary.py"])           

        # Analysis commands
        elif usrinpt == "corr":
            print("Correlation Analysis:")
            subprocess.run(["python", "tools/plot/corr.py"]) # Altered to process test and control data
        elif usrinpt == "pred":
            subprocess.run(["python", "tools/neural_net/arima.py"])
        elif usrinpt == "cleaner":
            subprocess.run(["python", "tools/cleaner.py"])
        elif usrinpt == "nn":
            subprocess.run(["python", "tools/neural_net/nn.py", "--from_main"])
        
        # Export commands

        elif usrinpt == "export":
            # reading the file
            data = pd.read_json("sesh.json")
            cleaned_data = clean_data(data)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            if not os.path.exists("files/export"):
                os.makedirs("files/export")
            data.to_json(f'files/export/{timestamp}.json')
            print('')
            print('Current session saved as JSON in exports folder.')
            print('')


        elif usrinpt == "export csv":
            # reading the file
            data = pd.read_json("sesh.json")
            cleaned_data = clean_data(data)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            if not os.path.exists("files/export"):
                os.makedirs("files/export")
            data.to_csv(f'files/export/{timestamp}.csv')
            print('')
            print('Current session saved as CSV in exports folder.')
            print('')
        
        elif usrinpt == "export xl":
            # reading the file
            data = pd.read_json("sesh.json")
            cleaned_data = clean_data(data)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            if not os.path.exists("files/export"):
                os.makedirs("files/export")
            data.to_excel(f'files/export/{timestamp}.xlsx')
            print('')
            print('Current session saved as CSV in exports folder.')
            print('')
            
# AGT_DB.SENSOR_READINGS DATA SOURCE FOR BELOW COMMANDS
            
        elif usrinpt == "build":
            subprocess.run(["python","/home/jeremy/Documents/AGT/tools/report/build_report.py"])
        
        # Database connection check
        elif usrinpt == "dbconn":
            subprocess.run(["python", "files/db_connect.py"])

# Sensor reading data insertion commands
        elif usrinpt == "dbconn":
            subprocess.run(["python", "files/db_update.py"])

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
