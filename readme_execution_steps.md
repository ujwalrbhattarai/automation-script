# signup automation in selenium

Automated signup script for `https://authorized-partner.vercel.app/` using Python and Selenium.

Handles the full multi-step signup flow without manual intervention

## what's in this repo

- `signup_automation_script.py` - main script
- `test.pdf` - sample document last
- `demo_video.mp4` - screen recording of test run
- `readme_execution_steps.md` - setup and execution 

## Prerequisites

- **Python**: 3.10 or higher
- **Google Chrome**: Installed locally
- **Gmail Account**: With 2fa enabled

## 1. Setup & Dependencies

Clone the repo and switch to the project directory:

```bash
git clone https://github.com/ujwalrbhattarai/automation-script.git
cd automation-script
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install required packages:

```bash
pip install selenium python-dotenv
```

## 2. Gmail App Password

The script uses a 16-character Google App Password (not your normal account password) to fetch the OTP over IMAP:

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
2. Create an App Password (name it anything, e.g. `qa-test`).
3. Copy the 16-character code into your `.env` without spaces.

## 3. Environment Variables (`.env`)

Create a `.env` file in the root directory (alongside `signup_automation_script.py`):

```env
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASS=your16characterapppassword
```

## 4. How Test Data Is Handled

- **Dynamic Email Aliasing:** The registration portal rejects already-registered emails. The script reads `GMAIL_USER` and automatically appends a random plus-alias on every run (e.g. `yourname+48291@gmail.com`). Gmail routes all plus-aliases to your primary inbox, so you can re-run the test repeatedly without burning new emails or editing files.
- **Random Phone Numbers:** Generates a randomized valid test phone number per run to avoid duplication errors.
- **Document Upload:** Uses `test.pdf` in the workspace root. The script converts it to an absolute path (`os.path.abspath("test.pdf")`) before passing it to the file input.

## 5. Running the Automation

Make sure your virtual environment is active and run:

```bash
python signup_automation_script.py
```

### Script Execution Flow:
1. Opens Chrome maximized and navigates to the landing page.
2. Clicks **Get Started**, accepts terms, and proceeds to the setup form.
3. Fills personal details (random name, phone, password, and aliased email) and submits.
4. Waits for the verification view, connects to `imap.gmail.com:993`, extracts the 6-digit OTP code, fills each digit, and confirms.
5. Fills Agency information (agency name, role, email, website, address, and selects country from the dropdown).
6. Fills Agency operational details (students recruited, experience dropdown, focus area, success metrics, and services checkbox).
7. Fills Business Registration number, selects country, checks institution type, attaches `test.pdf`, and submits the registration.
8. Holds for 15 seconds post-submission for visual confirmation before cleanly quitting the driver.
