# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Chris <goabonga@pm.me>
import os
import sys
from typing import Any

import httpx
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

SAFE_BROWSING_API_KEY: str = os.getenv("SAFE_BROWSING_API_KEY")

if not SAFE_BROWSING_API_KEY:
    raise RuntimeError("SAFE_BROWSING_API_KEY is not set in your .env file")

SAFE_BROWSING_API_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={SAFE_BROWSING_API_KEY}"
SAFE_BROWSING_FORM_URL = "https://safebrowsing.google.com/safebrowsing/report_phish/"

def check_url_blacklisted(url: str) -> bool:
    payload: dict[str, Any] = {
        "client": {
            "clientId": "safebrowsing-submit",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    with httpx.Client() as client:
        response = client.post(SAFE_BROWSING_API_URL, json=payload)
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return "matches" in result

def submit_url_with_selenium(url: str, details: str = "This page mimics Microsoft Outlook login.") -> None:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(SAFE_BROWSING_FORM_URL)

        report_type = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-0")))
        report_type.click()
        option = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//mat-option//span[contains(text(), 'This page is not safe')]"
        )))
        option.click()

        url_input = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        url_input.send_keys(url)

        details_input = wait.until(EC.presence_of_element_located((By.ID, "mat-input-1")))
        details_input.send_keys(details)

        submit_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[contains(text(), 'Submit')]]"
        )))

        submit_button.click()

        print(f"✅ URL submitted for review: {url}")

    except Exception as e:
        print(f"❌ Error during Selenium submission: {e}")
    finally:
        driver.quit()

def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python safebrowsing_submit.py https://example.com \"This page mimics Microsoft Outlook login.\"")
        sys.exit(1)

    target_url: str = sys.argv[1]
    details: str = sys.argv[2]
    print(f"🔍 Checking Safe Browsing DB for: {target_url}")
    is_blacklisted: bool = check_url_blacklisted(target_url)
    print(f"Blacklisted: {is_blacklisted}")

    if is_blacklisted:
        print("⚠️ Already blacklisted, skipping submission.")
    else:
        print("🚀 Not blacklisted, submitting report via Selenium...")
        submit_url_with_selenium(target_url, details)

if __name__ == "__main__":
    main()
