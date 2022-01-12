"""This module provides functions to collect offers information
   on indeed.fr website

functions
---------
collect_offer:
    collect and store information about job offers
build_indeed_url:
    build url for specific job or skill and a period of time
get_offer_ids:
    collect offers ids from web page html code
get_offer_info:
    collect offer information from web page html code according to its id

"""
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import time
import random


def collect_offers(job_to_search, offers_days_depth, time_between_requests=False):
    """get offers informations for a job keyword and a
       specific period of time.

    Outputs are stored in a .xlsx file

    Parameters
    ----------
    job_to_search: string
        job desired
    offers_days_depth: int
        max days from today
    time_between_requests: bool
        If True, random time (1 to 3 seconds) between each
        request

    Returns
    -------
    bool:
        True if requests got blocked, False otherwise

    """
    request_got_blocked = False
    l_offers_infos = []

    # set limits of scraping (offer date and number of pages)
    max_page = 30
    offer_date_min = (datetime.today() - timedelta(days=offers_days_depth)).strftime('%Y-%m-%d')
    last_offer_date = datetime.today().strftime('%Y-%m-%d')

    # build url for the first job search page
    url = build_indeed_url(job_to_search, 1)
    current_page = 1

    while last_offer_date >= offer_date_min and current_page <= max_page:

        # make a request to get html code
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # get offers ids for the current page:
        # if requests does not find any offer, we can guess
        # it got blocked by website
        # else, get offers information
        l_offers_ids = get_offer_ids(soup)
        if l_offers_ids is None:
            request_got_blocked = True
            return request_got_blocked
        else:
            for offer_id in l_offers_ids:
                d_offer_infos = get_offer_info(soup, offer_id)
                l_offers_infos.append(list(d_offer_infos.values()))

            # update last_offer_date, current_page and next url
            last_offer_date = d_offer_infos['date']
            url = build_indeed_url(job_to_search, current_page)
            current_page += 1

        if time_between_requests:
            random_time = random.randint(100, 300) / 100
            time.sleep(random_time)

    # store offers informations in .xlsx file
    df = pd.DataFrame(l_offers_infos, columns=['Title', 'Company', 'Date', 'Link'])

    df.to_excel('jobs_' + job_to_search + '_' + date.today().strftime("%d-%b-%Y") + '.xlsx', index=False)

    return request_got_blocked


def build_indeed_url(job_to_search, page_num):
    """build url from indeed website for a job keyword and a page number

    Parameters
    ----------
    job_to_search: string
        job you look for
    page_num : int
        page number

    Returns
    -------
    string:
        built url
    """
    if page_num == 1:
        return "https://fr.indeed.com/jobs?q=" + job_to_search + "&sort=date"
    else:
        return "https://fr.indeed.com/jobs?q=" + job_to_search + "&sort=date&start=" + str((page_num - 1) * 10)


def get_offer_ids(soup):
    """
    get offers ids from a html page

    Parameters
    ----------
    soup : BeautifulSoup
        html code

    Returns
    -------
    list[string]:
        offers ids
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
    """get information about a specific offer according to its id

    information: title, company name, published date, link

    Parameters
    ----------
    soup: BeautifulSoup
        html code
    offer_id: str
        offer identifier

    Returns
    -------
    dict:
        offer informations
    """
    infos_dict = {}

    # find <a> tag for the offer
    a = soup.find("a", id=offer_id)

    # get title
    job_title_zone = a.find("h2", class_="jobTitle jobTitle-color-purple jobTitle-newJob")
    try:
        title = [span.text for span in job_title_zone.find_all("span")][1]
    except:
        title = "Not found"

    # get company name
    try:
        company = a.find("a", class_="turnstileLink companyOverviewLink").text
    except AttributeError:
        try:
            company = a.find("span", class_="companyName").text
        except AttributeError:
            company = "Not found"

    # get published date
    try:
        offer_date_info = a.find("span", class_="date").text[6:]
        if offer_date_info in ["Publiée à l'instant", "Aujourd'hui"]:
            published_date = datetime.today().strftime('%Y-%m-%d')
        else:
            days_before = offer_date_info.split(" ")[3]
            published_date = (datetime.today() - timedelta(days=int(days_before))).strftime('%Y-%m-%d')
    except:
        published_date = datetime.today().strftime('%Y-%m-%d')

    # get link
    raw_link = a.get("href")
    if raw_link.startswith('/company'):
        processed_link = raw_link.split("-")[-1].split("?")[0]
        link = "https://fr.indeed.com/voir-emploi?jk=" + processed_link + "&vjs=3"
    elif raw_link.startswith('/rc'):
        link = "https://fr.indeed.com/voir-emploi?" + raw_link[8:]
    else:
        link = "Not found"

    # store informations in dict
    infos_dict['title'] = title
    infos_dict['company'] = company
    infos_dict['date'] = published_date
    infos_dict['link'] = link

    return infos_dict
