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

    # with open("main.py", "r") as file:
    #     entrypoint_script = file.read()

    #     resp = requests.post(
    #         f"{HEAD_NODE_ADDRESS}/api/jobs/",
    #         data={
    #             "entrypoint": "echo hello?",
    #             "runtime_env": {},
    #             "metadata": {"project_id": "75341ae6-8eb9-490f-8744-695dd90a7981"},
    #         },
    #         headers={"Authorization": f"Bearer {jwt_token}"},
    #         files={"file": ("main.py", entrypoint_script, "text/plain")}
    #     )

    # with open("main.py", "r") as file:
    #     entrypoint_script = file.read()

    # tmp_dir = "tmp"
    # if not os.path.exists(tmp_dir):
    #     os.makedirs(tmp_dir)

    # local_zipped_dir = shutil.make_archive(
    #     os.path.join(tmp_dir, "runtime_env"), "zip", "runtime_env", "main.py"
    #     )

    resp = requests.post(
        f"{HEAD_NODE_ADDRESS}/api/jobs/",
        json={
                    "runtime_env": {
                        "working_dir": "https://runtime-env-test-ray.s3.us-east-1.amazonaws.com/runtime_env2.zip?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFsaCXVzLWVhc3QtMSJGMEQCIEF8CnLnCFK%2F6oRnptmKxMW%2BJUl%2BwJdIyPS7aDoZ68v8AiBKTKVRCYFfCbn92W1gZB6U0HFKyuZ7a8Qcus66VRS53yr5AghEEAAaDDkzMTMxMzUwNzcyMCIMM8FaWTRQmGuXw45TKtYCbrWKpU%2FA%2F1HW09VqOyclTj31FACBi0oNJWKzLHiCmhWP4NoZXNvkKN5yEIwe2eWq4VieDhddmRzZTgtqyrtuQ9%2FMi3LYd%2BL5y35h9nYjKvf8nBdUTYW9LvR%2B01uSSEFJO%2FLFj%2Bf%2FP8peXlo7Owa2J5vbLdZypNmR2Xuwhy8g%2B8aAdD92ND9IdsSE%2BvA4SwMxdoLu1LpKQnR0ma43WayeQ2YV3cU9KtFGUwA%2BWMcGLNV1eYtHqL0BhoYdzYsZFQwwqDWMgQ6ZGoz3Y8F3%2BLYM9BqYcm%2FsMjwubZTuabyYvhjZN5gZdaBUW5Ydahg1l301%2BG9iV55FVSphWXLxQYMQQsiJV0PIZ4ueb0bU7RYutWMxRxaMEjVhAt02hGJbwmcsId5KIQGY0afaCxCxQp%2BqNA56pLvC0XDB09W1QUMdbk3t2bnbXV599X7nbt1HVZTEFSezXHfWMJ6Ao7UGOogCUcj3E2sH2KHxYVinzLTgYoVS32CH10D1SpRTskN09snjLbRpggUr%2FmRsLsmNjMWyLaTZq%2F4NmUF%2BA27f6P0jVCWXqUU%2F4rWyi2iB8rv1IsDJ4%2BRomRuRDvvg%2FzSgioysrJ4IyRjH%2BJXSLbATCW7cA2prKPDlhJGXAA7HdbIqGXIE4XMb2J%2BpsPU9NM90sgsrQva1mNaJtUQhbOCPDgNDQIlcctXpo%2BMqnp8PvgglS05snPdIfKzAtAQhFgmvYoV%2FAORai6laPe0YW9GfqDsRZ3aVmGPcBYeZGrhiWeQmDDORPI5gJFMbS%2FjKFJ%2FixiCcRN6GQJrPNppJnYM%2F68eAlsYuhHi3aIdw&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240730T103018Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA5RVU4LWEGFIVXBNV%2F20240730%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=c5d346c3b5e90b8496235bc992ef57a3435c45f1a0bca56949b9c5f2520e5e42",
                    },
                    "entrypoint": (
                        "python main2.py"
                    ),
                    "metadata": {"project_id": "5150c0aa-1dd8-4da5-9089-e46bc82408f8"},
                    },
        # json={
        #     "entrypoint": "python main.py",
        #     "runtime_env": {"working_dir": local_zipped_dir},
        #     "metadata": {"project_id": "75341ae6-8eb9-490f-8744-695dd90a7981"},
        # },
        headers={"Authorization": f"Bearer {jwt_token}"},
        # files={"file": ("main.py", entrypoint_script, "text/plain")}
    )

    print("response: ", resp.text)
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
