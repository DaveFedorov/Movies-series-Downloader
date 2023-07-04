import json
import pprint
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import re
import time

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"} 

driver = webdriver.Chrome(
    r"chromedriver.exe",
    desired_capabilities=capabilities,
)
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
                

driver.get("link") #link to the website from which you want to download video content

logs = driver.get_log("performance")

process_browser_logs_for_network_events(logs)
find_url()



