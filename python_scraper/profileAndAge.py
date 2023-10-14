import os
import time
import re
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

CORS(app)

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

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')


driver = get_driver()


@app.route("/get_profile", methods=["POST"])
def get_profile():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = data.get("username")
    profile_uri = data.get("profile_uri")
    if not username:
        return jsonify({"error": "Missing 'username' in JSON"}), 400
    if not profile_uri:
        return jsonify({"error": "Missing 'profile_uri' in JSON"}), 400

    driver.get(f"{profile_uri}")
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
            bullet_items = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".pv-top-card--list-bullet li")
                )
            )
            if len(bullet_items) == 2:
                followers_elem = bullet_items[0].find_element(
                    By.CSS_SELECTOR, "span.t-bold"
                )
                followers = followers_elem.text
                connections_elem = bullet_items[1].find_element(
                    By.CSS_SELECTOR, "span.t-bold"
                )
                connections = connections_elem.text
            elif len(bullet_items) == 1:
                followers = None
                connections_elem = bullet_items[0].find_element(
                    By.CSS_SELECTOR, "span.t-bold"
                )
                connections = connections_elem.text
        except (TimeoutException, NoSuchElementException):
            followers = None

        profile_data = {
            "username": username,
            "profile_pic_url": profile_image_url,
            "connections": connections,
            "followers": followers,
        }

        return jsonify(profile_data), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/get_earliest_activity", methods=["POST"])
def get_earliest_activity():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    profile_uri = data.get("profile_uri")
    if not profile_uri:
        return jsonify({"error": "Missing 'profile_uri' in JSON"}), 400

    driver.get(f"{profile_uri}/detail/recent-activity/")
    wait = WebDriverWait(driver, 20)

    try:
        previous_activity_count = 0
        no_change_count = 0
        while no_change_count < 3:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(8)
            activity_elements = driver.find_elements(
                By.CSS_SELECTOR,
                ".update-components-text-view.break-words span span[aria-hidden='true']",
            )
            if len(activity_elements) > previous_activity_count:
                previous_activity_count = len(activity_elements)
                no_change_count = 0
            else:
                no_change_count += 1

        if activity_elements:
            activity_text = activity_elements[-1].text.split(" • ")[0]
            match = re.match(r"(\d+)(\D+)", activity_text)
            if match:
                number = int(match.group(1))
                unit = match.group(2).strip()
                return (
                    jsonify(
                        {
                            "earliest_activity_number": number,
                            "earliest_activity_unit": unit,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Unexpected activity format."}), 500
        else:
            return jsonify({"error": "No activity found."}), 404

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
