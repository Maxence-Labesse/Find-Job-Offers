from bs4 import BeautifulSoup
import requests
from datetime import datetime
from datetime import timedelta
import pandas as pd


def next_pages_url_build(keyword, page_num):
    return "https://fr.indeed.com/jobs?q=" + keyword + "&sort=date&start=" + str((page_num - 1) * 10)


def get_job_ids(soup):
    a_jobs = soup.find_all("a")
    job_list = []
    for a in a_jobs:
        try:
            if a["id"].startswith("job_"):
                job_list.append(a["id"])
        except KeyError:
            pass

    return job_list


def get_job_infos(soup, job_id):
    infos_dict = {}
    a = soup.find("a", id=job_id)

    # Title
    job_title_class = "jobTitle jobTitle-color-purple jobTitle-newJob"
    job_title_zone = a.find("h2", class_=job_title_class)
    title = [span.text for span in job_title_zone.find_all("span")][1]

    # Company
    try:
        company = a.find("a", class_="turnstileLink companyOverviewLink").text
    except AttributeError:
        company = a.find("span", class_="companyName").text

    # Date
    # Published Date
    job_date = a.find("span", class_="date").text[6:]  # ou utiliser job.find(...).span.text
    if job_date in ["Publiée à l'instant", "Aujourd'hui"]:
        date = datetime.today().strftime('%Y-%m-%d')
    else:
        # print(job_date.split(" "))
        days_before = job_date.split(" ")[3]
        # print(days_before)
        date = (datetime.today() - timedelta(days=int(days_before))).strftime('%Y-%m-%d')
        """
        try:
            days_before = job_date.split(" ")["3"]
            date = (datetime.today() - timedelta(days=days_before)).strftime('%Y-%m-%d')
        except:
            date = "No date"
            print(job_date.split(" "))
    """
    # print(job_date)

    # Link
    link = "Not found"
    raw_link = a.get("href")
    if raw_link.startswith('/company'):
        processed_link = raw_link.split("-")[-1].split("?")[0]
        link = "https://fr.indeed.com/voir-emploi?jk=" + processed_link + "&vjs=3"
    elif raw_link.startswith('/rc'):
        link = "https://fr.indeed.com/voir-emploi?" + raw_link[8:]

    infos_dict['title'] = title
    infos_dict['company'] = company
    infos_dict['date'] = date
    infos_dict['link'] = link

    return infos_dict


# job_scraping(first_page_url)


def job_scraping(keyword, historical_depth):
    captcha = False
    max_date = (datetime.today() - timedelta(days=historical_depth)).strftime('%Y-%m-%d')
    first_page_url = "https://fr.indeed.com/jobs?q=" + keyword + "&sort=date"
    i = 2
    data = []

    url = first_page_url
    last_date = datetime.today().strftime('%Y-%m-%d')

    while last_date >= max_date and i <= 30:

        # print(url)
        html_text = requests.get(url).text
        # print(html_text)
        soup = BeautifulSoup(html_text, 'lxml')
        job_list = get_job_ids(soup)

        # print(i)

        if len(job_list) == 0:
            captcha = True
            break

        for job_id in job_list:
            d_job = get_job_infos(soup, job_id)
            data.append(list(d_job.values()))
            # print(d_job['date'])
            last_date = d_job['date']

        url = next_pages_url_build(keyword, i)

        i += 1

    df = pd.DataFrame(data, columns=['Title', 'Company', 'Date', 'Link'])

    df.to_excel('jobs_' + keyword + '_' + str(historical_depth) + '.xlsx', index=False)

    return captcha

# key_word = "SAP"
# historical_depth = 3

# job_scraping(key_word, historical_depth)
