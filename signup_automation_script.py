import os
import time
import re
import random
import imaplib
import email
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# 1. red key
load_dotenv()
GMAILUSER = os.getenv("GMAIL_USER")
GMAILAPPPASS = os.getenv("GMAIL_APP_PASS")

# otb fetch
def get_otp_from_gmail():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAILUSER, GMAILAPPPASS)

    for _ in range(10):  
        time.sleep(3)
        mail.select("inbox")
        _, data = mail.search(None, "UNSEEN")
        mail_ids = data[0].split()

        if mail_ids:
            _, msg_data = mail.fetch(mail_ids[-1], "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() in ("text/plain", "text/html"):
                        body += part.get_payload(decode=True).decode(errors="ignore")
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            match = re.search(r"\b\d{6}\b", body)
            if match:
                mail.logout()
                return match.group(0)

    mail.logout()
    return None

# 1 open browser
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

driver.get("https://authorized-partner.vercel.app/")

# 2 get started button
getstarted=wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/register']")))
getstarted.click()

# checkbox and continue
check=wait.until(ec.element_to_be_clickable((By.ID, "remember")))
check.click()

continuebtn=wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a[href='register?step=setup']")))
continuebtn.click()

#step 1

# fill step1 boxes
fname=wait.until(ec.visibility_of_element_located((By.NAME, "firstName")))
fname.send_keys("Test")
lname=wait.until(ec.visibility_of_element_located((By.NAME, "lastName")))
lname.send_keys("Partner")

testnum = f"98421{random.randint(10000, 99999)}"
phone=wait.until(ec.visibility_of_element_located((By.NAME, "phoneNumber")))
phone.send_keys(testnum)

pw = "Test@1234"
passw = wait.until(ec.visibility_of_element_located((By.NAME, "password")))
passw.send_keys(pw)
cpassw= wait.until(ec.visibility_of_element_located((By.NAME, "confirmPassword")))
cpassw.send_keys(pw)

# make gmail id
namepart, domainpart = GMAILUSER.split("@")
testmail = f"{namepart}+{random.randint(10000, 99999)}@{domainpart}"
print("Using email:", testmail)

wait.until(ec.visibility_of_element_located((By.NAME, "email"))).send_keys(testmail)
time.sleep(2)

# click next
next=wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]")))
next.click()

# for otp screen
verifybtn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Verify Code')]")))
print("Checking Gmail for OTP...")
otpcode = get_otp_from_gmail()
print("Got OTP:", otpcode)

otpinputs = driver.find_elements(By.TAG_NAME, "input")
if len(otpinputs) == 1:
    otpinputs[0].send_keys(otpcode)
else:
    for box, digit in zip(otpinputs[:6], otpcode):
        box.send_keys(digit)

verifybtn.click()

# step 1 copmleted

# agency part

#1 name of agncy
agencyname = wait.until(ec.visibility_of_element_located((By.NAME, "agency_name")))
agencyname.send_keys("abcd agency")

#2 role in agency
driver.find_element(By.NAME, "role_in_agency").send_keys("abcd role")

#3 email of agency
driver.find_element(By.NAME, "agency_email").send_keys(testmail)

#4 website of agency
driver.find_element(By.NAME, "agency_website").send_keys("abcdagency.com")

#5 address of agency
driver.find_element(By.NAME, "agency_address").send_keys("Kathmandu, Nepal")

#6 country of agency
driver.find_element(By.CSS_SELECTOR, "button[role='combobox']").click()
wait.until(ec.element_to_be_clickable((By.XPATH, "//span[text()='Nepal']/parent::div"))).click()
driver.find_element(By.CSS_SELECTOR, "button[role='combobox']").click()

#7 click next
driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

# step 2 completed
#step 3

# student nu
students = wait.until(ec.visibility_of_element_located((By.NAME, "number_of_students_recruited_annually")))
students.send_keys("2")

# experience
driver.find_element(By.CSS_SELECTOR, "button[role='combobox']").click()
wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@role='option'][2]"))).click()

# focus area
driver.find_element(By.NAME, "focus_area").send_keys("bachelor masters")

# success 
driver.find_element(By.NAME, "success_metrics").send_keys("0")

# services checkbox
driver.find_element(By.CSS_SELECTOR, "button[role='checkbox']").click()

# next 
driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

# step 3 completed

# step 4
#registration number

registration = wait.until(ec.visibility_of_element_located((By.NAME, "business_registration_number")))
registration.send_keys("1234")

# countries
driver.find_element(By.CSS_SELECTOR, "button[role='combobox']").click()
wait.until(ec.element_to_be_clickable((By.XPATH, "//span[text()='Australia']/parent::div"))).click()
driver.find_element(By.CSS_SELECTOR, "button[role='combobox']").click()

#institution type
driver.find_element(By.CSS_SELECTOR, "button[role='checkbox']").click()

#upload flie
filepath = os.path.abspath("test.pdf")
fileinput = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
fileinput[0].send_keys(filepath)

#submitt
driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()

time.sleep(15)
driver.quit()