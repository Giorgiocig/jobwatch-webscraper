import os

import yaml


def build_id_from_REF_APEC(string):
    return string.split("/")[0].split(":")[1].strip()


def load_yaml_file(filename):
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Construct the full path to the yaml file file
    yaml_file_path = os.path.join(script_dir, "..", filename)
    with open(yaml_file_path, "r") as f:
        return yaml.safe_load(f)


def load_config_from_env():
    config = {}
    config["s3"] = {}
    config["aws"] = {}
    config["s3"]["endpoint_url"] = os.environ["CONFIG_S3_ENDPOINT_URL"]
    config["aws"]["bucket_name"] = os.environ["CONFIG_S3_BUCKET_NAME"]
    config["aws"]["access_key"] = os.environ["CONFIG_S3_ACCESS_KEY"]
    config["aws"]["secret_key"] = os.environ["CONFIG_S3_SECRET_KEY"]
    return config


def extract_keywords_from_yaml(filename):
    keywords_yaml = load_yaml_file(filename)
    keywords = keywords_yaml["keywords"]
    list_of_keywords = []
    for keyword in keywords.values():
        list_of_keywords.append(keyword)
    return list_of_keywords


def extract_date_and_id(string):
    date_part, id_part = string.split(" - ")
    date = date_part.split()[-1]
    id = id_part.split(" : ")[-1]
    return date, id


def swap_place_of_work_and_zipcode(string):
    if " - " in string:
        place_of_work, zipcode = string.split(" - ")
        swapped_element = [zipcode, " - ", place_of_work]
        return "".join(swapped_element)
    else:
        return string


def convert_string_number_representation_to_int(string):
    formatted_string = string.replace("\u202f", "")
    return int(formatted_string)


def extract_matching_items(list_items, allowed_items):
    matching_items = []
    for item in list_items:
        if item.text in allowed_items:
            matching_items.append(item.text)
    return " , ".join(matching_items)


def extract_experience_required(list_items):
    exp_required = []
    for item in list_items:
        if (
            item.text == "Exp. 1 à 7 ans"
            or item.text == "Exp. - 1 an"
            or item.text == "Exp. + 7 ans"
        ):
            exp_required.append(item.text)
    if len(exp_required) == 0:
        exp_required = ["N/A"]
    return " , ".join(exp_required)


def extract_sector(list_items, excluded_patterns):
    sector_details = []
    for item in list_items:
        if not any(sub in item.text for sub in excluded_patterns):
            sector_details.append(item.text)
    return " , ".join(sector_details)


def extract_salary(list_items, salary_pattern):
    salary = "N/A"
    for item in list_items:
        if salary_pattern in item.text:
            salary = item.text
    return salary
