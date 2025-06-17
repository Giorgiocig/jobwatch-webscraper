import apec.apec_actions as apec_action
from helpers.helpers import extract_keywords_from_yaml
from s3.s3 import insert_data_to_s3


def apec_main():
    keywords = extract_keywords_from_yaml("keywords.yaml")
    for keyword in keywords:
        apec_action.land_first_page()
        apec_action.close_banner()
        apec_action.write_input(keyword)
        apec_action.click_submit_btn_by_selecting_ID()
        results = apec_action.report_result()
        insert_data_to_s3("apec", results)
