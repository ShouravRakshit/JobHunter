import time
import csv
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from workday_urls import company_urls
from bs4 import BeautifulSoup


def scrape_workday(driver, company_name, start_url):
    results = []
    driver.get(start_url)
    time.sleep(2)  # wait for page to load

    page_num = 1
    prev_out_text = None  

    while True:
        # Parse the Listing Page ---
        print(f"\nProcessing page {page_num}...")
        
        # Wait for the page to fully load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='jobOutOfText']"))
            )
        except:
            print("Couldn't find jobOutOfText element. Page may be empty or different format.")
        
        # Get updated page source after waiting
        soup = BeautifulSoup(driver.page_source, "html.parser")

        job_out_el = soup.select_one('[data-automation-id="jobOutOfText"]')
        if job_out_el:
            current_out_text = job_out_el.get_text(strip=True)
            print(f"Currently showing: {current_out_text}")
        else:
            current_out_text = None
            print("No job count indicator found on this page.")

        
        if current_out_text and current_out_text == prev_out_text:
            print("Pagination appears stuck (jobOutOfText is the same). Breaking out.")
            break
        prev_out_text = current_out_text

        # Collect all job links
        job_links = soup.select('a[data-automation-id="jobTitle"]')
        if not job_links:
            print(f"No job links found on this page for {company_name}. Stopping.")
            break

        print(f"Found {len(job_links)} jobs on this page.")

        # for each job scrape details
        for link_tag in job_links:
            partial_href = link_tag.get("href")
            if not partial_href:
                continue

            job_url = urljoin(start_url, partial_href)
            print(f"Scraping job detail => {job_url}")

            # Load detail page
            driver.get(job_url)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='jobPostingHeader']"))
                )
            except:
                print(f"Timeout on detail page: {job_url}")
                continue

            detail_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract title, location, posted date, description
            title_el = detail_soup.select_one('[data-automation-id="jobPostingHeader"]')
            job_title = title_el.get_text(strip=True) if title_el else None

            # Posted date
            posted_block = detail_soup.select_one('[data-automation-id="postedOn"]')
            if posted_block:
                posted_dd = posted_block.select_one('dd')
                posted_date = posted_dd.get_text(strip=True) if posted_dd else None
            else:
                posted_date = None

            # Location
            loc_block = detail_soup.select_one('[data-automation-id="locations"]')
            if loc_block:
                dd_tags = loc_block.select("dd")
                job_location = ", ".join(dd.get_text(strip=True) for dd in dd_tags) if dd_tags else None
            else:
                job_location = None

            # Description
            desc_el = detail_soup.select_one('[data-automation-id="jobPostingDescription"]')
            job_desc = desc_el.get_text("\n", strip=True) if desc_el else None

            # Store in results
            results.append({
                "company": company_name,
                "url": job_url,
                "title": job_title,
                "posted_date": posted_date,
                "location": job_location,
                "description": job_desc
            })

            driver.back()
            time.sleep(2)  # wait time after returning to listing

        # navigate to next page 
        page_num += 1
        
       
        next_page_found = False
        
        try:
            page_btn_selector = f"button[aria-label='page {page_num}']"
            page_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, page_btn_selector))
            )
            print(f"Found button for page {page_num}, clicking it...")
            driver.execute_script("arguments[0].scrollIntoView(true);", page_btn)
            time.sleep(1)
            page_btn.click()
            next_page_found = True
            
        except Exception as e:
            print(f"Couldn't find direct link to page {page_num}: {e}")
            
            # finding and clicking the next button
            try:
                next_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='next']"))
                )
                
                # check if the next button is disabled
                if next_btn.get_attribute("aria-disabled") == "true":
                    print("Next button is disabled. We're on the last page.")
                    break
                    
                print("Clicking 'next' button...")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                time.sleep(1)
                next_btn.click()
                next_page_found = True
                
            except Exception as e2:
                print(f"Couldn't find or click 'next' button: {e2}")
                try:
                    current_page_btn = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-current='page']"))
                    )
                    current_page_num = current_page_btn.get_attribute("aria-label").replace("page ", "")
                    print(f"Currently on page {current_page_num}")
                    
                    # find all pagination buttons
                    pagination_parent = driver.find_element(By.CSS_SELECTOR, "nav[aria-label='pagination']")
                    page_buttons = pagination_parent.find_elements(By.TAG_NAME, "button")
                    
                    for btn in page_buttons:
                        if btn.get_attribute("aria-label") == f"page {int(current_page_num) + 1}":
                            print(f"Found button for page {int(current_page_num) + 1}, clicking it...")
                            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                            time.sleep(1)
                            btn.click()
                            next_page_found = True
                            break
                except:
                    print("All pagination strategies failed")
        
        # break out of loop if no next page was found
        if not next_page_found:
            print("No next page found. Ending pagination.")
            break
        
        # wait for the new page to load
        time.sleep(4)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='jobOutOfText']"))
            )
            
            new_soup = BeautifulSoup(driver.page_source, "html.parser")
            new_job_out_el = new_soup.select_one('[data-automation-id="jobOutOfText"]')
            new_out_text = new_job_out_el.get_text(strip=True) if new_job_out_el else None
            
            if new_out_text == prev_out_text:
                print("Page didn't change after navigation attempt. Breaking out of pagination loop.")
                break
                
        except:
            print("Couldn't verify page change. Continuing anyway...")

    return results


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.set_window_size(1920, 1080)

    all_jobs = []

    for entry in company_urls:
        name = entry["company_name"]
        url = entry["url"]
        print(f"\nScraping {name} from {url}")

        try:
            company_jobs = scrape_workday(driver, name, url)
            all_jobs.extend(company_jobs)
            print(f"Collected {len(company_jobs)} jobs from {name}")
        except Exception as e:
            print(f"Error scraping {name}: {e}")

    driver.quit()

    # saving to CSV
    with open("workday_jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "company","url","title","posted_date","location","description"
        ])
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"\nDone. Collected {len(all_jobs)} total jobs.")


if __name__ == "__main__":
    main()