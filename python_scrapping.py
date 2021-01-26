import csv
from datetime import datetime
import requests  # to send request to a server to het HTML
from bs4 import BeautifulSoup


# ---------------------------
position=input("Enter position, for ex. data analyts, accountant, developer: ")
location=input("Enter location, for ex. Vilnius, Kaunas, Alytus: ")

def get_url(position, location):
    """Generate URL from position and location"""
    template = "https://www.cvbankas.lt/?miestas={}&padalinys%5B%5D=&keyw={}"
    url = template.format(position, location)
    return url


def get_record(card):
    atag = card.a
    job_title = card.find("h3", "list_h3").text.strip()
    job_url = atag.get("href")
    company = card.find("span", "dib mt5").text.strip()
    location = card.find("span", "list_city").text.strip()
    try:
        post_date = card.find("span", "txt_list_2").text.strip()

    except AttributeError:
        post_date = ""

    try:
        salary = card.find("span", "salary_amount").text.strip()
    except AttributeError:
        salary = ""

    record = (job_title, job_url, company, location, post_date, salary)

    return record


def bankas_main(position, location):
    """RUn the main program routine"""

    records = []
    url = get_url(position, location)

    while True:
        response = requests.get(url)  # print(response) - 200 means working
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all(
            "article",
            "list_article list_article_rememberable jobadlist_list_article_rememberable",
        )

        for card in cards:
            record = get_record(card)
            records.append(record)

        toliau = soup.find("li", "prev_next")
        try:
            next_btn = toliau.a.get("href")
            print("next butn:", next_btn)
            url = "https://www.cvbankas.lt" + next_btn
        except AttributeError:
            break

    with open("bothsitesresults1.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["job_title", "job_url", "company", "location", "post_date", "salary"]
        )
        writer.writerows(records)


# run the main function passing on the job title and location

bankas_main(location.capitalize(), position.lower())
# bankas_main("Vilnius", "data analyst")


def get_url_cvonline(position, location):
    """Generate URL from position and location"""
    template = "https://www.cvonline.lt/darbo-skelbimai/q-{}/vilniaus-{}?sort=inserted&dir=desc"
    url = template.format(position, location)
    return url


def get_record_cvonline(card):
    atag = card.h2.a
    job_title = card.find(itemprop="title").get_text()
    # job_url = "https://www.cvonline.lt" + atag.get("href")
    job_url = "https:" + atag.get("href")
    company = card.find("span", {"itemprop": "hiringOrganization"}).get_text()
    location = card.find("span", {"itemprop": "jobLocation"}).get_text()
    post_date = card.find("span", {"itemprop": "datePosted"}).get_text()

    record = (job_title, job_url, company, location, post_date)

    return record


def main(position, location):
    """RUn the main program routine"""

    records = []
    url = get_url_cvonline(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", "cvo_module_offer_content")

        for card in cards:
            record = get_record_cvonline(card)
            records.append(record)

        toliau = soup.find("li", "page_next")
        try:
            next_btn = toliau.a.get("href")
            url = "https://www.cvonline.lt" + next_btn
        except AttributeError:
            break

    with open("bothsitesresults1.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["job_title", "job_url", "company", "location", "post_date", "salary"]
        )
        writer.writerows(records)


# run the main function passing on the job title and location
main(position.lower(), location.lower())
# main("data analyst", "vilnius")

