# Actions for the scaper
import time

import undetected_chromedriver as uc
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import apec.constants as const
from helpers.helpers import build_id_from_REF_APEC

# Set up undetected-chromedriver
uc_chrome_options = uc.ChromeOptions()
uc_chrome_options.add_argument("--no-sandbox")
uc_chrome_options.add_argument("--disable-dev-shm-usage")
uc_chrome_options.add_argument("--blink-settings=imagesEnabled=false")
uc_chrome_options.add_argument("--headless")

# Initialize the Chrome driver with the specified options and service
chrome_driver = ChromeDriverManager().install()
driver = uc.Chrome(service=Service(chrome_driver), options=uc_chrome_options)


def land_first_page():
    """
    Get url of the page and land to it
    """
    driver.get(const.BASE_URL)


def close_banner():
    """
    Click on the banner to close it
    """
    try:
        close_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
        )
        close_button.click()
    # TimeoutException to manage the absence of the banner after the first iteration
    except TimeoutException:
        print(
            "TimeoutException: Timed out waiting for the banner close button to be clickable."
        )
    except NoSuchElementException:
        print("NoSuchElementException: Close button not found on the page.")
    except Exception as e:
        print(f"Exception: An exception occurred: {e}")


def write_input(input_text):
    """
    Write input string into input field
    """
    input_field = driver.find_element(By.ID, "keywords")
    input_field.send_keys(input_text)


def click_submit_btn_by_selecting_ID():
    """
    Selecting btn to submit the form and click to it
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "info"))
        )
        btn_submit = driver.find_element(By.ID, const.BTN_SUBMIT_ID)
        btn_submit.click()
    except Exception as e:
        print("Exception: Exception occurred:", str(e))


def extract_href_attributes(page_links, page_links_hrefs):
    """
    Extract href attributes from a list of page link elements and appends them to the page_links_hrefs list.
    """
    for link in page_links:
        href = link.get_attribute("href")
        page_links_hrefs.append(href)


def click_next_page(pagination):
    """
    Attempts to click the 'Suiv.' button to navigate to the next page.
    Returns True if successful, False if the button does not exist.
    """
    try:
        btn_suiv = pagination.find_elements(
            By.XPATH, "//li[@class='page-item next']/a[contains(text(), 'Suiv.')]"
        )
        if btn_suiv:
            driver.execute_script("arguments[0].scrollIntoView(true);", btn_suiv[0])
            btn_suiv[0].click()
            return True
        else:
            return False
    except StaleElementReferenceException:
        print("StaleElementReferenceException: the button does not exist anymore.")
        return False
    except Exception as e:
        print(f"Exception: An exception occurred while clicking next page: {e}")
        return False


def navigate_through_paginated_results():
    """
    Navigate through paginated result, if a stale element reference occurs, the while loop is re-launched
    """
    wait = WebDriverWait(driver, 10)
    page_links_hrefs = []
    try:
        while True:
            try:
                pagination = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pagination"))
                )
                time.sleep(1)
                page_links = driver.find_elements(
                    By.XPATH, "//a[@queryparamshandling='merge']"
                )
                time.sleep(1)
                extract_href_attributes(page_links, page_links_hrefs)
                if not click_next_page(pagination):
                    break
            except StaleElementReferenceException:
                print("StaleElementReferenceException occurred")
                continue
    except TimeoutException:
        print("TimeoutException: Timeout waiting for pagination element.")
    except Exception as e:
        print(f"Exception: An exception occurred: {e}")
    return page_links_hrefs


def extract_job_details(href):
    """
    Extracts job details from a single href.
    """
    driver.get(href)
    # Using explicit wait for h1 element
    try:
        h1_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
    except Exception as e:
        print(e)
    job_offer_details_obj = {
        "id": build_id_from_REF_APEC(
            driver.find_element(By.XPATH, "//div[@class='ref-offre']").text
        ),
        "intitule": h1_element.text,
        "description": driver.find_element(
            By.XPATH,
            '//div[@class="details-post"]/h4[text()="Descriptif du poste"]/following-sibling::p',
        ).text,
        "dateCreation": driver.find_element(
            By.XPATH, '//div[@class="date-offre mb-10"]'
        ).text,
        "dateActualisation": driver.find_element(
            By.XPATH,
            '//div[@class="date-offre" and not(contains(@class, "mb-10"))]',
        ).text,
        "researched_profile": driver.find_element(
            By.XPATH,
            '//div[@class="details-post"]/h4[text()="Profil recherché"]/following-sibling::p',
        ).text,
        "typeContrat": driver.find_element(
            By.XPATH, '//ul[@class="details-offer-list mb-20"]/li/span'
        ).text,
        "experienceLibelle": driver.find_element(
            By.XPATH,
            '//div[@class="col-lg-4"]/div[@class="details-post"][3]/span',
        ).text,
        "secteurActiviteLibelle": driver.find_element(
            By.XPATH,
            '//div[@class="col-lg-4"]/div[@class="details-post"][h4[text()="Métier"]]/span',
        ).text,
        "lieuTravail": {
            "libelle": driver.find_element(
                By.XPATH,
                '//ul[@class="details-offer-list mb-20"]/li[3]',
            ).text
        },
        "entreprise": {
            "nom": driver.find_element(
                By.XPATH,
                '//ul[@class="details-offer-list mb-20"]/li[1]',
            ).text,
            "description": driver.find_element(
                By.XPATH,
                '//div/h4[text()="Entreprise"]/following-sibling::p[1]',
            ).text,
        },
        "salaire": {
            "commentaire": driver.find_element(
                By.XPATH,
                '//div[@class="col-lg-4"]/div[@class="details-post"][1]/span',
            ).text
        },
        "origineOffre": {"urlOrigine": href},
    }
    return job_offer_details_obj


def report_result():
    """
    Build an array of object as a results
    """
    hrefs_list = navigate_through_paginated_results()
    list_of_offers = []
    for href in hrefs_list:
        try:
            job_offer_details_obj = extract_job_details(href)
            list_of_offers.append(job_offer_details_obj)
        except Exception as e:
            print(f"Exception: An exception occurred while visiting link {href}: {e}")
    return list_of_offers
