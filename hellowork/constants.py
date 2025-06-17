BASE_URL = "https://www.hellowork.com/fr-fr/"

REQUIRED_BAC = ["Bac +2", "Bac +3, Bac +4", "Bac +5"]

EXCLUDED_PATTERN = ["🏠\n", "🕑\n6", "€ /", "Exp.", "Bac"]
SALARY_PATTERN = "€ /"

# btn close banner
BTN_CLOSE_BANNER = "hw-cc-notice-accept-btn"

# input field
INPUT_FIELD = "//input[@id='k']"

# job_details_offer object properties
TITLE = "//span[@class='tw-block tw-typo-xl sm:tw-typo-3xl tw-mb-2' and @data-cy='jobTitle']"
ENTERPRISE = "//span[@class='tw-contents tw-typo-m tw-text-grey']"
SALARY = "//ul[@class='tw-mb-3 tw-flex']/li[@class='tw-tag-attractive-s tw-readonly']"
RESEARCHED_PROFILE_H2 = "/html/body/main/div[3]/div[3]/div[1]/div[2]/div/section[2]/h2"
RESEARCHED_PROFILE = "/html/body/main/div[3]/div[3]/div[1]/div[2]/div/section[2]"
ID_AND_CREATION_DATE = (
    "//span[@class='tw-block tw-typo-xs tw-text-grey tw-break-words']"
)

PLACE_AND_ZIPCODE_LABEL = "//span[@class='tw-inline-flex tw-typo-m tw-text-grey']"
ENTERPRISE_DESCRIPTION = "//section//p[contains(@class, 'tw-typo-long-m')]"
TYPE_OF_CONTRACT = "ul > li.tw-tag-grey-s.tw-readonly:nth-of-type(2)"

# dropdown
DROPDOWN_MENU = "//label[@for='collapseTags']"
DROPDOWN_ELEMENT_MENU = (
    "//ul[contains(@class, 'tw-flex') and contains(@class, 'tw-flex-wrap') and contains(@class, 'tw-gap-3') and contains(@class, 'lg:tw-mb-3')]",
)
