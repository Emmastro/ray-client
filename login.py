from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver (this example uses Chrome)
driver = webdriver.Chrome()

try:
    # Open the login page
    driver.get("http://localhost:3000/login")

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
        with open("jwt_token.txt", "w") as file:
            file.write(jwt_token)
        print("JWT token saved to jwt_token.txt")
    else:
        print("JWT token not found or login not completed in time")

finally:
    # Close the browser
    driver.quit()
