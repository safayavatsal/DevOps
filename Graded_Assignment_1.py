#1
import re

def check_password_strength(password):
    # Check the length of the password
    if len(password) < 8:
        return False
    
    # Check for uppercase and lowercase letters
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
        return False
    
    # Check for at least one digit
    if not re.search(r'[0-9]', password):
        return False
    
    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True

def main():
    password = input("Enter a password to check its strength: ")
    if check_password_strength(password):
        print("The password is strong.")
    else:
        print("The password is weak. It should be at least 8 characters long, contain both uppercase and lowercase letters, at least one digit, and at least one special character.")

if __name__ == "__main__":
    main()


#2
import psutil
import time

def monitor_cpu(threshold=80):
    try:
        while True:
            # Get the current CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)

            # Check if the CPU usage exceeds the threshold
            if cpu_usage > threshold:
                print(f"ALERT! CPU usage is above {threshold}%: {cpu_usage}%")
            else:
                print(f"CPU usage is {cpu_usage}%")

            # Sleep for a short period before checking again
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoring interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define the CPU usage threshold
    cpu_threshold = 80
    monitor_cpu(cpu_threshold)



#3
import json
import sqlite3
from flask import Flask, jsonify
from configparser import ConfigParser

app = Flask(__name__)

# Function to read configuration file
def read_config(file_path):
    config_data = {}
    config = ConfigParser()
    try:
        config.read(file_path)
        for section in config.sections():
            config_data[section] = {}
            for key, value in config.items(section):
                config_data[section][key] = value
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"Error: {e}")
    return config_data

# Function to save data as JSON in the database
def save_to_db(data, db_path='config.db'):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY, data TEXT)''')
        cursor.execute('DELETE FROM config')  # Clear any existing data
        cursor.execute('INSERT INTO config (data) VALUES (?)', [json.dumps(data)])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Route to fetch the configuration data
@app.route('/get_config', methods=['GET'])
def get_config():
    try:
        conn = sqlite3.connect('config.db')
        cursor = conn.cursor()
        cursor.execute('SELECT data FROM config')
        data = cursor.fetchone()
        conn.close()
        if data:
            return jsonify(json.loads(data[0]))
        else:
            return jsonify({"error": "No data found"}), 404
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {e}"}), 500

if __name__ == '__main__':
    config_file_path = 'config.txt'
    config_data = read_config(config_file_path)
    if config_data:
        save_to_db(config_data)
    app.run(debug=True)



#4
import os
import shutil
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='Backup files from source to destination directory.')
    parser.add_argument('source', type=str, help='Source directory to backup.')
    parser.add_argument('destination', type=str, help='Destination directory for backup.')
    return parser.parse_args()

def backup_files(source, destination):
    if not os.path.exists(source):
        print(f"Error: Source directory '{source}' does not exist.")
        return
    if not os.path.exists(destination):
        print(f"Error: Destination directory '{destination}' does not exist.")
        return

    for item in os.listdir(source):
        source_file = os.path.join(source, item)
        if os.path.isfile(source_file):
            destination_file = os.path.join(destination, item)
            if os.path.exists(destination_file):
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                destination_file = os.path.join(destination, f"{item}_{timestamp}")
            try:
                shutil.copy2(source_file, destination_file)
                print(f"Copied '{source_file}' to '{destination_file}'")
            except Exception as e:
                print(f"Error copying '{source_file}': {e}")

if __name__ == '__main__':
    args = parse_args()
    backup_files(args.source, args.destination)
