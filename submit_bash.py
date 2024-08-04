import os
from pathlib import Path
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from ray.job_submission import JobStatus

HEAD_NODE_ADDRESS = "http://ec2-52-22-46-66.compute-1.amazonaws.com:3000"
HEAD_NODE_ADDRESS = "http://localhost:3000"

TOKEN_FILE = "jwt_token.txt"

def get_jwt_token():
    # Check if token file exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            jwt_token = file.read().strip()
        # Verify token validity
        resp = requests.get(
            f"{HEAD_NODE_ADDRESS}/api/jobs/",
            headers={"Authorization": f"Bearer {jwt_token}"}
        )
        if resp.status_code == 401:
            print("Token has expired or is invalid. Please log in again.")
        else:
            return jwt_token

    # Set up the WebDriver (this example uses Chrome)
    driver = webdriver.Chrome()
    try:
        # Open the login page
        driver.get(f"{HEAD_NODE_ADDRESS}/login")

        # Wait for the user to log in manually
        print("Please log in manually on the browser window that opened.")
        
        # This waits for a maximum of 60 seconds for the user to log in
        # Adjust the wait time as needed
        for _ in range(60):
            time.sleep(1)
            # Check if the JWT token is set in local storage
            jwt_token = driver.execute_script("return localStorage.getItem('token');")  # Update the key if different
            if jwt_token:
                break

        if jwt_token:
            # Save the token to a file
            with open(TOKEN_FILE, "w") as file:
                file.write(jwt_token)
            print("JWT token saved to jwt_token.txt")
        else:
            print("JWT token not found or login not completed in time")
            return None
    finally:
        # Close the browser
        driver.quit()
    
    return jwt_token

def submit_and_monitor_job(jwt_token):


    resp = requests.post(
        f"{HEAD_NODE_ADDRESS}/api/jobs/",
        json={
                    "entrypoint": "echo hello?",
                    "metadata": {"project_id": "5150c0aa-1dd8-4da5-9089-e46bc82408f8"},
                    },

        headers={"Authorization": f"Bearer {jwt_token}"},

    )

    rst = json.loads(resp.text)
    submission_id = rst["submission_id"]

    start = time.time()
    while time.time() - start <= 10:
        resp = requests.get(
            f"{HEAD_NODE_ADDRESS}/api/jobs/{submission_id}",
            headers={"Authorization": f"Bearer {jwt_token}"}
        )

        rst = json.loads(resp.text)
        status = rst["status"]

        if status in {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED}:
            break
        time.sleep(1)

# Main script logic
jwt_token = get_jwt_token()
if jwt_token:
    submit_and_monitor_job(jwt_token)
else:
    print("Failed to obtain JWT token.")
