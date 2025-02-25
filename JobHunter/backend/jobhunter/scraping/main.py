import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from workday_urls import company_urls

# Function to scrape a Workday jobs listing page
def scrape_workday(driver, company_name, start_url):

    results = []

    # load the main listing page
    driver.get(start_url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-automation-id='jobTitle']"))
        )
    except Exception as e:
        print(f"Could not find any job links for {company_name}: {e}")
        return results  # Return empty list

    # parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # getting the job titles
    job_link_tags = soup.select('a[data-automation-id="jobTitle"]')

    # Loop over each job link
    for link_tag in job_link_tags:
        # e.g. retrieve the job detail URL
        partial_href = link_tag.get("href")
        print("url link: ", partial_href)
        if not partial_href:
            continue
        
        job_url = urljoin(start_url, partial_href)
        print("job url: ", job_url)
        # open each job’s detail page
        driver.get(job_url)
        time.sleep(2)  # Wait for dynamic content to load

        detail_soup = BeautifulSoup(driver.page_source, "html.parser")

        # extract job details
        # Title
        title_el = detail_soup.select_one('[data-automation-id="jobPostingHeader"]')
        job_title = title_el.get_text(strip=True) if title_el else None

        # Location
        location_block = detail_soup.select_one('[data-automation-id="locations"]')
        if location_block:
            location_dds = location_block.select('dd')
            if location_dds:
                job_location = ", ".join(dd.get_text(strip=True) for dd in location_dds)
            else:
                job_location = None
        else:
            job_location = None

        # Posted date 
        posted_block = detail_soup.select_one('[data-automation-id="postedOn"], [data-automation-id="time"]')
        if posted_block:
            posted_dd = posted_block.select_one('dd')
            posted_date = posted_dd.get_text(strip=True) if posted_dd else None
        else:
            posted_date = None

        # Job description 
        desc_el = detail_soup.select_one('[data-automation-id="jobPostingDescription"]')
        job_desc = desc_el.get_text(" ", strip=True) if desc_el else None

        # storing the job details in a list
        results.append({
            "company": company_name,
            "url": job_url,
            "title": job_title,
            "location": job_location,
            "posted_date": posted_date,
            "description": job_desc
        })

    return results


def main():
    # Set up headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    all_jobs = []

    # looping over all the items in the company_urls list
    for entry in company_urls:
        company_name = entry["company_name"]
        start_url = entry["url"]

        print(f"Scraping {company_name} from {start_url}")
        try:
            jobs = scrape_workday(driver, company_name, start_url)
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"Error scraping {company_name}: {e}")

    driver.quit()

    # saving the results to a CSV file
    with open("workday_jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["company","url","title","location","posted_date","description"])
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"Finished scraping. Total jobs: {len(all_jobs)}")

if __name__ == "__main__":
    main()
