import json
import pprint
import tkinter as tk
import clipboard
from selenium import webdriver
from tkinter import messagebox, ttk
from tkinter import Tk, Text, Button, Label, Entry
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
import time
from datetime import datetime, timedelta

chrome_options = Options()
chrome_options.add_argument("--headless")

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"} 

driver = webdriver.Chrome(r"chromedriver.exe", desired_capabilities=capabilities, options=chrome_options)
network_log = []

def process_browser_logs_for_network_events(logs):
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            network_log.append(log)
        
def find_url():
    for log in network_log:
        if 'params' in log and 'response' in log['params']:
            url = log['params']['response']['url']
            match = re.search(r'http://(.*?)m3u8', url)
            if match:
                extracted_url = match.group(0)
                delete_after = ".mp4"
                index = extracted_url.find(delete_after)
                if index != -1:
                    mod_link = extracted_url[:index+4]
                    print(mod_link)
                    return mod_link
                
def on_confirm():
    driver.get(entry_link.get()) 
    download_link_title = tk.Label(window, text="Download link:")
    download_link_title.pack()
    field_with_lk = tk.Entry(window, width=50)
    field_with_lk.pack()
    def copy_link():
        link = field_with_lk.get()
        clipboard.copy(link)
        messagebox.showinfo("Link Copied", "The link has been copied to the clipboard.")
    button_copy = tk.Button(window, text="Copy Link", command=copy_link)
    button_copy.pack()
    
    
    end_time = datetime.now() + timedelta(seconds=2)
    while datetime.now() < end_time:
        logs = driver.get_log("performance")
        process_browser_logs_for_network_events(logs)
    driver.quit()
    mod_link = find_url()
    field_with_lk.insert(0, mod_link)

window = tk.Tk()
window.geometry("400x300")
window.title("Download-HDrezka")

# Create the link label and entry field
label_link = tk.Label(window, text="Link to what you want to download:")
label_link.pack()
entry_link = tk.Entry(window, width=50)
entry_link.pack()

# Create the download button
button_confirm = tk.Button(window, text="Get download link", command=on_confirm)
button_confirm.pack()

# Start the Tkinter event loop
window.mainloop()


