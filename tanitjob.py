from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

# -------- CONFIG --------
URL = 'https://www.tanitjobs.com/jobs/?listing_type%5Bequal%5D=Job&keywords%5Ball_words%5D=react&GooglePlace%5Blocation%5D%5Bvalue%5D=tunis'
PROFILE_DIR = r"C:/Users/ibtihelbs/selenium-profile"
TODAY_FILE = "tanit_jobs_today.csv"
PREVIOUS_FILE = "tanit_jobs_previous.csv"
CHANGES_FILE = "tanit_jobs_changes.csv"

# -------- SETUP SELENIUM --------
options = Options()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")  # use your profile
options.add_argument("--start-maximized")  # optional
# options.add_argument("--headless")  # do NOT use headless initially with Cloudflare

driver = webdriver.Chrome(options=options)
driver.get(URL)

# -------- WAIT UNTIL JOBS LOAD --------
wait = WebDriverWait(driver, 15)
jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[contains(@class,"listing-item")]')))

# -------- SCRAPE JOBS --------
data = []
for job in jobs:
    try:
        title_el = job.find_element(By.XPATH, './/a[@class="link"]')
        title = title_el.text.strip()
        link = title_el.get_attribute('href')
        company = job.find_element(By.XPATH, './/span[contains(@class,"listing-item-info-company")]').text.strip()
        location = job.find_element(By.XPATH, './/span[contains(@class,"listing-item-info-location")]').text.strip()
        date = job.find_element(By.XPATH, './/div[contains(@class,"listing-item__date")]').text.strip()
        short_desc = job.find_element(By.XPATH, './/div[contains(@class,"listing-item__desc")]').text.strip()
        data.append([title, company, location, date, short_desc, link])
    except:
        continue

driver.quit()

# -------- SAVE TODAY'S DATA --------
df_today = pd.DataFrame(data, columns=["Title", "Company", "Location", "Date", "ShortDesc", "Link"])
df_today.to_csv(TODAY_FILE, index=False)
df_today.to_json("tanit_jobs_today.json", orient="records")

# -------- COMPARE WITH PREVIOUS --------
if os.path.exists(PREVIOUS_FILE):
    df_prev = pd.read_csv(PREVIOUS_FILE)
    merged = df_today.merge(df_prev, on="Title", how="outer", suffixes=("_today","_prev"), indicator=True)

    new_jobs = merged[merged["_merge"] == "left_only"]
    removed_jobs = merged[merged["_merge"] == "right_only"]

    changes = pd.concat([new_jobs, removed_jobs])
    changes.to_csv(CHANGES_FILE, index=False)

    print(f"New jobs: {len(new_jobs)}, Removed jobs: {len(removed_jobs)}")

# -------- OVERWRITE PREVIOUS DATA --------
os.replace(TODAY_FILE, PREVIOUS_FILE)
