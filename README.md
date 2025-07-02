# safebrowsing-submit

**Check if a URL is blacklisted by Google Safe Browsing and submit it for review using Selenium.**  
This script checks the URL via the Safe Browsing v4 API, and if not flagged, automatically opens and fills the phishing report form.

---

## ⚙️ Installation (with Poetry)

### 1. Clone and enter the project

```bash
git clone https://github.com/youruser/safebrowsing-submit.git
cd safebrowsing-submit
```

### 2. Create a .env file with your Google API key

```bash
SAFE_BROWSING_API_KEY=your_google_safe_browsing_api_key
```

### 3. Install dependencies 

```bash
poetry install
```

## 🚀 Usage

```bash
poetry run safebrowsing-submit https://example.com "This site mimics Microsoft Outlook login"
```

- The script will:
  - Query the Google Safe Browsing API.
  - If the URL is not flagged, open the phishing report form in Chrome via Selenium.
  - Automatically fill in:
    - Report type
    - URL
    - Description (you provide it)
  - Submit the form.

## 💻 Notes

Make sure Google Chrome and ChromeDriver are installed and compatible.

You can disable headless mode inside the script to debug visually.

Supports Python >= 3.13 (adjust in pyproject.toml if needed).

## 🧪 Example

```bash
poetry run safebrowsing-submit https://fake-outlook-login.biz "Fake Outlook phishing page targeting login credentials"
```

## 📦 Dependencies

- selenium
- httpx
- python-dotenv

## 📝 License

MIT – Copyright © 2025 Chris <goabonga@pm.me>
