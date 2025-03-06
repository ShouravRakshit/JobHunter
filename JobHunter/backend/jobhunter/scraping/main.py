import time
import csv
from urllib.parse import urljoin
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from workday_urls import company_urls

def gather_all_workday_links(driver, start_url):
    
    job_urls = {}  # key = job URL, value = page number
    driver.get(start_url)
    time.sleep(2)  # Allow page to load

    page_num = 1

    while True:
        print(f"\nProcessing page {page_num}...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_tags = soup.select("a[data-automation-id='jobTitle']")
        
        new_links = 0
        for tag in job_tags:
            href = tag.get("href")
            if href:
                full_url = urljoin(start_url, href)
                if full_url not in job_urls:
                    job_urls[full_url] = page_num
                    new_links += 1
        print(f"Found {new_links} new links on page {page_num}; total unique links so far: {len(job_urls)}.")

        # Attempt to click the "Next" button
        try:
            next_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='next']"))
            )
            if next_btn.get_attribute("aria-disabled") == "true":
                print("Next button is disabled. Reached the last page.")
                break
            print("Clicking Next button to load the next page...")
            next_btn.click()
            time.sleep(3)  # Wait for next page to load
        except Exception as e:
            print(f"No Next button found or error clicking it: {e}. Ending pagination.")
            break

        page_num += 1

    return job_urls


def scrape_workday_listings(driver, company_name, start_url):
   
    print(f"\nGathering job listing URLs for {company_name} ...")
    job_dict = gather_all_workday_links(driver, start_url)
    print(f"Collected {len(job_dict)} unique job URLs for {company_name}.")

    results = []
    for url, page_found in job_dict.items():
        print(f"Scraping job detail => {url} (from page {page_found})")
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='jobPostingHeader']"))
            )
        except Exception as e:
            print(f"Timeout waiting for job detail at {url}: {e}")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract Title
        title_el = soup.select_one('[data-automation-id="jobPostingHeader"]')
        job_title = title_el.get_text(strip=True) if title_el else None

        # Extract Posted Date
        posted_block = soup.select_one('[data-automation-id="postedOn"]')
        if posted_block:
            posted_dd = posted_block.select_one("dd")
            posted_date = posted_dd.get_text(strip=True) if posted_dd else None
        else:
            posted_date = None

        # Extract Location
        loc_block = soup.select_one('[data-automation-id="locations"]')
        if loc_block:
            dd_tags = loc_block.select("dd")
            location = ", ".join(dd.get_text(strip=True) for dd in dd_tags) if dd_tags else None
        else:
            location = None

        # Extract Description
        desc_el = soup.select_one('[data-automation-id="jobPostingDescription"]')
        description = desc_el.get_text("\n", strip=True) if desc_el else None

        results.append({
            "company": company_name,
            "url": url,
            "title": job_title,
            "posted_date": posted_date,
            "location": location,
            "description": description,
            "page_found": page_found  # stored the page number for debugging
        })
    
    return results

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    driver = webdriver.Chrome(options=chrome_options)
    
    all_jobs = []
    
    for entry in company_urls:
        company_name = entry["company_name"]
        start_url = entry["url"]
        print(f"\nScraping {company_name} from {start_url}")
        
        try:
            company_jobs = scrape_workday_listings(driver, company_name, start_url)
            all_jobs.extend(company_jobs)
            print(f"Collected {len(company_jobs)} jobs from {company_name}")
        except Exception as e:
            print(f"Error scraping {company_name}: {e}")
    
    driver.quit()
    
    data_folder = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
    csv_path = os.path.join(data_folder, "raw_jobs.csv")
    print(f"Saving CSV to: {csv_path}")

    # Save results to CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["company", "url", "title", "posted_date", "location", "description", "page_found"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_jobs)
    
    print(f"\nDone. Collected {len(all_jobs)} total jobs.")

if __name__ == "__main__":
    main()
