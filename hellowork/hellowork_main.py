import hellowork.hellowork_actions as hellowork_action
from helpers.helpers import extract_keywords_from_yaml
from s3.s3 import insert_data_to_s3


def hellowork_main():
    keywords = extract_keywords_from_yaml("keywords.yaml")
    for keyword in keywords:
        hellowork_action.land_first_page()
        hellowork_action.close_banner()
        hellowork_action.write_input(keyword)
        hellowork_action.click_submit_btn_by_selecting_ID()
        results = hellowork_action.report_result()
        insert_data_to_s3("hellowork", results)
