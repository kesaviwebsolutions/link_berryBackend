import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

load_dotenv()  

LINKEDIN_EMAIL = os.environ.get("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.environ.get("LINKEDIN_PASSWORD")


def get_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    return driver


driver = get_driver()


@app.route("/get_profile", methods=["POST"])
def get_profile():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = data.get("username")
    if not username:
        return jsonify({"error": "Missing 'username' in JSON"}), 400

    driver.get(f"https://www.linkedin.com/in/{username}/")
    wait = WebDriverWait(driver, 10)  # wait up to 10 seconds

    try:
        try:
            profile_image_elem = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button.pv-top-card-profile-picture img")
                )
            )
            profile_image_url = profile_image_elem.get_attribute("src")
        except (TimeoutException, NoSuchElementException):
            profile_image_url = None

        try:
            followers_elem = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".pv-top-card--list-bullet li:nth-child(1) span.t-bold",
                    )
                )
            )
            followers = followers_elem.text
        except (TimeoutException, NoSuchElementException):
            followers = None

        try:
            connections_elem = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".pv-top-card--list-bullet li:nth-child(2) span.t-bold",
                    )
                )
            )
            connections = connections_elem.text
        except (TimeoutException, NoSuchElementException):
            connections = None

        profile_data = {
            "username": username,
            "profile_pic_url": profile_image_url,
            "connections": followers,
            "followers": connections,
        }

        return jsonify(profile_data), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
