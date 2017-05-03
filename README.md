# LinkedIn search scraper

Simple command line tool for scraping LinkedIn search results and saving them to CSV file.
This package is python 2 and 3 compatible.

## Installation from pypi:

Install package with pip:
```
$ pip install liscraper
```

## Installation from repository:

Clone repository:
```
$ git clone https://github.com/czekan/liscraper
```

Create virtualenv with python 2.6+/3.4+ in repository folder:
```
$ cd liscraper && virtualenv env --python=/usr/bin/python3.6 && source env/bin/activate
```
You may need to alter python path in above command.


Install requirements:
```
(env)$ pip setup.py install
```

## Usage:

Run it inside virtualenv in interactive mode
```
(env)$ liscraper
```
or pass required credentials as inline options
```
(env)$ liscraper --login_email=your_linkedin@email.com --login_pass=yourpassword --keyword=python --output=searchexport.csv
```
