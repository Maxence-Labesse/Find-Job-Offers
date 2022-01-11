from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pandas as pd
from datetime import date


def scrape_offers(keyword, days_from_today_max):
    """
    get all offers informations for a job keyword and a specific period of time.
    store the outputs in an .xlsx file.

    Parameters
    ----------
    keyword (string): job keyword
    days_from_today_max (int): max days from today

    Returns
    -------
    (Boolean): Test if html requets get blocked by captcha

    """
    test_captcha = False
    l_offers_infos = []

    # parameters
    max_date = (datetime.today() - timedelta(days=days_from_today_max)).strftime('%Y-%m-%d')
    page_date = datetime.today().strftime('%Y-%m-%d')

    url = build_indeed_url(keyword, 1)
    page_num = 2
    # scraping stops when date max is reached or when 30 pages are scraped
    while page_date >= max_date and page_num <= 30:

        # get html code
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        # get offers ids
        l_offers_ids = get_offer_ids(soup)
        # if no jobs are found, we can guess it's a captcha problem and we stop the scraping
        if len(l_offers_ids) == 0:
            test_captcha = True
            break
        # get offers informations
        for offer in l_offers_ids:
            d_offer_infos = get_offer_info(soup, offer)
            l_offers_infos.append(list(d_offer_infos.values()))

        # set new page_date and next page url
        page_date = d_offer_infos['date']
        url = build_indeed_url(keyword, page_num)
        page_num += 1

    # store offers informations in .xlsx file
    df = pd.DataFrame(l_offers_infos, columns=['Title', 'Company', 'Date', 'Link'])
    df.to_excel('jobs_' + keyword + '_' + date.today().strftime("%d-%b-%Y") + '_' + str(days_from_today_max) + '.xlsx',
                index=False)

    return test_captcha


def build_indeed_url(keyword, page_num):
    """
    build url from indeed website for a job keyword and a page number

    Parameters
    ----------
    keyword (string): job keyword
    page_num (int) : page number

    Returns
    -------
    (string): built url
    """
    if page_num == 1:
        return "https://fr.indeed.com/jobs?q=" + keyword + "&sort=date"
    else:
        return "https://fr.indeed.com/jobs?q=" + keyword + "&sort=date&start=" + str((page_num - 1) * 10)


def get_offer_ids(soup):
    """
    get offer ids from a html page

    Parameters
    ----------
    soup (BeautifulSoup): html code

    Returns
    -------
    (list[string]): offer ids list
    """
    l_offer_ids = []

    # find all <a> tags from html code and get id if it starts with "job"
    a_tags = soup.find_all("a")
    for a in a_tags:
        try:
            if a["id"].startswith("job_"):
                l_offer_ids.append(a["id"])
        except KeyError:
            pass

    return l_offer_ids


def get_offer_info(soup, offer_id):
    """
    get informations about a specific offer according to its id
    informations: title, company name, published date, link

    Parameters
    ----------
    soup (BeautifulSoup): html code
    job_id (string): offer identifier

    Returns
    -------
    dict: offer informations
    """
    infos_dict = {}

    # find <a> tag for the offer
    a = soup.find("a", id=offer_id)

    # get title
    # print("\n")
    # print(a.prettify())
    job_title_zone = a.find("h2", class_="jobTitle jobTitle-color-purple jobTitle-newJob")
    title = [span.text for span in job_title_zone.find_all("span")][1]

    # get company name
    try:
        company = a.find("a", class_="turnstileLink companyOverviewLink").text
    except AttributeError:
        company = a.find("span", class_="companyName").text

    # get published date
    job_date = a.find("span", class_="date").text[6:]
    if job_date in ["Publiée à l'instant", "Aujourd'hui"]:
        date = datetime.today().strftime('%Y-%m-%d')
    else:
        days_before = job_date.split(" ")[3]
        date = (datetime.today() - timedelta(days=int(days_before))).strftime('%Y-%m-%d')

    # get link
    link = "Not found"
    raw_link = a.get("href")
    if raw_link.startswith('/company'):
        processed_link = raw_link.split("-")[-1].split("?")[0]
        link = "https://fr.indeed.com/voir-emploi?jk=" + processed_link + "&vjs=3"
    elif raw_link.startswith('/rc'):
        link = "https://fr.indeed.com/voir-emploi?" + raw_link[8:]

    # store informations in dict
    infos_dict['title'] = title
    infos_dict['company'] = company
    infos_dict['date'] = date
    infos_dict['link'] = link

    return infos_dict
