# Find Job Offers
![Demo](images/demo.gif)

> A Python application to collect offers information from indeed.fr website
> All you have to do is to define a job keyword and period of time and get
> results in an Execel (.xlsx) file.

`Disclaimer :` 
- Web Scraping may be against the <ins>terms of use</ins> of some websites a
  nd users may be subject to legal ramifications depending on where and how 
  they attempt to scrape information.
- So, Always inspect the Robots.txt as many websites specifies what is 
  considered as good behaviour on that site, such as areas that are allowed 
  to be crawled, restricted pages, and frequency limits for crawling.

## Installation (Windows)
git clone the project, then install package requirements:

Using terminal:
```
py -m pip install -r requirements.txt
```
## Usage
Using terminal (at project root):
```shell
py -m src.main
```
Note: You can add time between web page requests using 
`time_between_requets` argument as follow:
```shell
py -m src.main time_between_offers=True
```
## Release History
* 0.0.1
    * First realease

## Meta

LABESSE Maxence - maxence.labesse@yahoo.fr

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/Maxence-Labesse/Find-Job-Offers]()