# Jobwatch webscraper

# Description

Jobwatch webscraper is a Python application to retrieve data of job offers from APEC and Hellowork websites and send them to S3 server.
Selenium Python is used to perform scraping and collect data. 
The scraper performs a research by writing keywords present in keyword.yaml file in the input field. Then, the search button is clicked and the research is launched. It navigates through paginated results storing the job offers's hrefs inside a list "page_links_hrefs". At that point, it loops over the hrefs in "page_links_hrefs" collecting data in objects. One object "job_offer_details_obj "corresponds to one job offers. Next, each object is appended in a list "list_of_offers" that represents the final output.
object output example

```json
{
    "intitule": "Développeur Rust Smart Contract F/H",
    "description": "Poste et Missions\nEn ....",
    "dateCreation": "Publiée le 31/05/2024",
    "dateActualisation": "Actualisée le 24/06/2024",
    "researched_profile": "Profil recherché\nVous vous reconnaissez ...",
    "typeContrat": " CDI ",
    "experienceLibelle": "Minimum 2 ans",
    "secteurActiviteLibelle": "Développeur",
    "lieuTravail": {"libelle": "Emirats Arabes Unis"},
    "entreprise": {
        "nom": "TOMORROW JOBS",
        "description": "Entreprise\nTomorrow Jobs ...",
    },
    "salaire": {"commentaire": "A négocier"},
    "origineOffre": {
        "urlOrigine": "https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/173946739W?motsCles=Rust&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687&selectedIndex=0&page=0"
    },
}
```
list_of_offers is a list containing object like the descibed previously.

# Files and folders

## main.py
entry point of the application. Keywords presents in keywords.yaml are extracted and stocked in an array. Then a loop over the array is performed. At each iteration, one research is done, data are collected and sent to s3 server.

## s3 folder
It contains the utilities to send data to the S3 server. Functions to read and delete data are available as well.

## apec folder
It contains all the utilities for apec website scraping (navigation and data collections).

## hellowork
It contains all the utilities for helllork website scraping (navigation and data collections).

# keywords.yaml
It contains variables for parametric research

# Details

## Undected webdriver and options

Undetected webdriver is used 

Options for webdriver are added to allow compatibility with a docker environment:

uc_chrome_options = uc.ChromeOptions()
uc_chrome_options.add_argument("--no-sandbox")
uc_chrome_options.add_argument("--disable-dev-shm-usage")
uc_chrome_options.add_argument("--blink-settings=imagesEnabled=false")
uc_chrome_options.add_argument("--headless")


chrome_driver = ChromeDriverManager().install()
driver = uc.Chrome(service=Service(chrome_driver), options=uc_chrome_options)

It is possible to remove the options to restore a graphical interface and test locally:

uc_chrome_options = uc.ChromeOptions()
uc_chrome_options.add_argument("--no-sandbox")
uc_chrome_options.add_argument("--disable-dev-shm-usage")
uc_chrome_options.add_argument("--blink-settings=imagesEnabled=false")

chrome_driver = ChromeDriverManager().install()
driver = uc.Chrome(service=Service(chrome_driver), options=uc_chrome_options)

Or to remove all the options

uc_chrome_options = uc.ChromeOptions()
uc_chrome_options.add_argument("--no-sandbox")
uc_chrome_options.add_argument("--disable-dev-shm-usage")
uc_chrome_options.add_argument("--blink-settings=imagesEnabled=false")

chrome_driver = ChromeDriverManager().install()
driver = uc.Chrome(service=Service(chrome_driver))

## Docker

requirements.txt file contains python packages to include into the docker image

build docker image:

in the project root folder, launch the command 
./build.sh

the image created is named 
rg.fr-par.scw.cloud/cenotelie/skillsup-jobwatch-webscraper

running project via docker 
docker run rg.fr-par.scw.cloud/cenotelie/skillsup-jobwatch-webscraper

# Running project

## Docker
docker run rg.fr-par.scw.cloud/cenotelie/skillsup-jobwatch-webscraper

## Python
 /bin/python3 /home/user/cenotelie/cenotelie-webscraper/main.py

In this case one error can show up:

selenium.common.exceptions.SessionNotCreatedException: Message: session not created: cannot connect to chrome at 127.0.0.1:59525
from session not created: This version of ChromeDriver only supports Chrome version 129
Current browser version is 128.0.6613.113

It is due to ancient version of Google Chrome Browser installed. To solve it, update Google Chrome Browser.

Linux - Ubuntu:
Open a new terminal
-sudo apt update 
-sudo apt --only-upgrade install google-chrome-stable
