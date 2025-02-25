import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from workday_urls import company_urls

def scrape_workday(driver, company_name, start_url):
    """
    1) Load the 'list' page of job postings.
    2) Extract job-card links (or job IDs) from that page.
    3) For each job, navigate to the detail page and parse the data.
    4) Return a list of dictionaries with the fields you want.
    """
    results = []

    # 1) Load the main listing page
    driver.get(start_url)
    time.sleep(3)  # rudimentary wait; better to use WebDriverWait

    # 2) Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Example selector for job links:
    # Many Workday pages have <a data-automation-id="jobTitle" ...>
    job_link_tags = soup.select('a[data-automation-id="jobTitle"]')

    # Gather the partial href or full link from each job card
    # Some sites include only a relative path, e.g. "/en-US/BDO/job/Calgary-AB/..."
    # so you might need to build the absolute URL or just do driver.get() with the partial link appended.
    for link_tag in job_link_tags:
        # e.g. retrieve the job detail URL
        partial_href = link_tag.get("href")
        print("url link: ", partial_href)
        if not partial_href:
            continue
        
        job_url = urljoin(start_url, partial_href)
        print("job url: ", job_url)
        # 3) Now open each job’s detail page
        driver.get(job_url)
        time.sleep(2)  # Wait for dynamic content to load

        detail_soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract relevant fields.  For example:
        # Title
        title_el = detail_soup.select_one('[data-automation-id="jobPostingHeader"]')
        job_title = title_el.get_text(strip=True) if title_el else None

        # Location
        location_el = detail_soup.select_one('[data-automation-id="location"]')
        job_location = location_el.get_text(strip=True) if location_el else None

        # Posted date (some pages have data-automation-id="jobPostingPostedDate" or
        # you might find it in a span that says "Posted X Days Ago")
        posted_date_el = detail_soup.find("span", text=lambda t: t and "Posted" in t)
        posted_date = posted_date_el.get_text(strip=True) if posted_date_el else None

        # Job description might be in a big <div data-automation-id="jobPostingDescription">
        desc_el = detail_soup.select_one('[data-automation-id="jobPostingDescription"]')
        job_desc = desc_el.get_text(" ", strip=True) if desc_el else None

        # As an example, we store each job as a dictionary
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
    # Set up headless Chrome (adjust to your liking)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    all_jobs = []

    # Loop over each Workday site in your config
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

    # Example: write results to CSV
    with open("workday_jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["company","url","title","location","posted_date","description"])
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"Finished scraping. Total jobs: {len(all_jobs)}")

if __name__ == "__main__":
    main()
