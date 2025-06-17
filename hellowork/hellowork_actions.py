# Actions for the scaper
import os
import sys
import time

import undetected_chromedriver as uc
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import hellowork.constants as const
from helpers.helpers import (
    extract_date_and_id,
    extract_experience_required,
    extract_matching_items,
    extract_salary,
    extract_sector,
    swap_place_of_work_and_zipcode,
)

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
            EC.element_to_be_clickable((By.ID, "hw-cc-notice-accept-btn"))
        )
        close_button.click()
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
    input_field = driver.find_element(
        By.XPATH,
        "//input[@id='k']",
    )
    input_field.send_keys(input_text)


def click_submit_btn_by_selecting_ID():
    """
    Selecting btn to submit the form and click to it
    """

    btn_submit = driver.find_element(
        By.XPATH,
        "//button[@data-cy='searchEngineSubmitButton']",
    )
    btn_submit.click()


def extract_href():
    """
    Extract href from a container of job offers
    """
    # Locate the container of job offers
    container_of_job_offers = driver.find_elements(
        By.XPATH, '//*[@id="turboSerp"]/section[2]/div[1]/section[3]/ul'
    )
    hrefs = []

    for container in container_of_job_offers:
        anchor_tags = container.find_elements(By.TAG_NAME, "a")
        for anchor in anchor_tags:
            hrefs.append(anchor.get_attribute("href"))
    return hrefs


def find_right_arrow_btn():
    """
    Select right arrow button in the bottom navbar
    """
    buttons_in_bottom_navbar = driver.find_elements(By.XPATH, "//button")
    btn_right_arrow = None

    for button in buttons_in_bottom_navbar:
        if "arrow-right.svg" in button.get_attribute("innerHTML"):
            btn_right_arrow = button
            break
    return btn_right_arrow


def navigate_through_paginated_results():
    """
    Navigate through paginated results by clicking on the right arrow in the bottom navbar
    """
    page_link_hrefs = []
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            btn_right_arrow = find_right_arrow_btn()

            # Check if the button is disabled (end of pagination)
            if "tw-pointer-events-none" in btn_right_arrow.get_attribute("class"):
                print("Reached the end of pagination.")
                break

            # Extract current page links
            page_links = driver.find_elements(
                By.XPATH,
                '//div[contains(@class, "tw-h-full") and contains(@class, "tw-relative") and contains(@class, "tw-flex") and contains(@class, "tw-flex-col") and contains(@class, "sm:tw-flex-row") and contains(@class, "sm:small-group:tw-flex-col")]//a',
            )
            for link in page_links:
                href = link.get_attribute("href")
                page_link_hrefs.append(href)

            # Scroll into view for the button
            driver.execute_script("arguments[0].scrollIntoView(true);", btn_right_arrow)
            time.sleep(1)  # Let the scroll animation complete

            # Click the button using JavaScript
            driver.execute_script("arguments[0].click();", btn_right_arrow)

            time.sleep(2)

        except (
            TimeoutException,
            NoSuchElementException,
            ElementNotInteractableException,
            StaleElementReferenceException,
        ) as e:
            print("Reached the end of pagination or an error occurred:", e)
            break

    return page_link_hrefs


def extract_details_from_upper_tag_list():
    """
    extract details from the upper_tag_list
    """
    list_items_co = driver.find_element(
        By.XPATH, "//ul[@class='tw-flex tw-flex-wrap tw-gap-3']"
    )

    list_item = list_items_co.find_elements(By.TAG_NAME, "li")

    # education
    education_required = extract_matching_items(list_item, const.REQUIRED_BAC)
    #  experience
    str_experience_required = extract_experience_required(list_item)
    # sector
    sector_details = extract_sector(list_item, const.EXCLUDED_PATTERN)
    # salary
    salary = extract_salary(list_item, const.SALARY_PATTERN)
    return (sector_details, education_required, str_experience_required, salary)


def extract_job_details(href):
    """
    Extracts job details from a single href.
    """
    driver.get(href)
    sector_details, education_required, str_experience_required, salary = (
        extract_details_from_upper_tag_list()
    )
    # enterprise
    try:
        entreprise = driver.find_element(
            By.XPATH,
            const.ENTERPRISE,
        )
        entreprise_text = entreprise.text
    except NoSuchElementException as e:
        print(
            f"NoSuchElementException: An exception occurred while locating the entreprise element: {e}"
        )
        entreprise_text = "N/A"
    # researched profile
    researched_profile = "N/A"
    try:
        researched_profile_h2 = driver.find_element(
            By.XPATH,
            const.RESEARCHED_PROFILE_H2,
        )
        if researched_profile_h2.text == "Le profil recherché":
            researched_profile = driver.find_element(
                By.XPATH,
                const.RESEARCHED_PROFILE,
            )
            researched_profile = researched_profile.text
    except NoSuchElementException as e:
        researched_profile = "N/A"
    job_offer_details_obj = {
        "id": extract_date_and_id(
            driver.find_element(
                By.XPATH,
                const.ID_AND_CREATION_DATE,
            ).text
        )[1],
        "intitule": driver.find_element(
            By.XPATH,
            const.TITLE,
        ).text,
        "description": driver.find_element(
            By.XPATH,
            "//section[1]/p",
        ).text,
        "dateCreation": extract_date_and_id(
            driver.find_element(
                By.XPATH,
                const.ID_AND_CREATION_DATE,
            ).text
        )[0],
        "researched_profile": researched_profile,
        "typeContrat": driver.find_element(
            By.CSS_SELECTOR,
            const.TYPE_OF_CONTRACT,
        ).text,
        "experienceLibelle": str_experience_required,
        "secteurActiviteLibelle": sector_details,
        "lieuTravail": {
            "libelle": swap_place_of_work_and_zipcode(
                driver.find_element(
                    By.XPATH,
                    const.PLACE_AND_ZIPCODE_LABEL,
                ).text
            )
        },
        "entreprise": {
            "nom": entreprise_text,
            "description": driver.find_element(
                By.XPATH,
                const.ENTERPRISE_DESCRIPTION,
            ).text,
        },
        "salaire": {
            "commentaire": salary,
        },
        "origineOffre": href,
        "qualificationLibelle": education_required,
    }
    return job_offer_details_obj


def report_result():
    """
    Build an array of object as a results
    """
    list_of_offers = []
    hrefs_list = navigate_through_paginated_results()
    for href in hrefs_list:
        try:

            job_offer_obj = extract_job_details(href)
            list_of_offers.append(job_offer_obj)
        except Exception as e:
            print(f"Exception: An exception occurred while visiting link {href}: {e}")
    return list_of_offers
