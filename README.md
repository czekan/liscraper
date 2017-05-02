# LinkedIn search scraper

Simple command line tool for scraping LinkedIn search results and saving them to CSV file.
Python 3.5+ is required.

# Installation:

Clone repository:
```
$ git clone https://github.com/czekan/liscraper
```

Create virtualenv with python 3.5+ in repository folder:
```
$ cd liscraper && virtualenv env --python=/usr/bin/python3.6 && source env/bin/activate
```

Install requirements:
```
(env)$ pip install -r requirements.txt
```

# Usage:

Run it inside virtualenv in interactive mode
```
(env)$ python liscrapy/scraper.py
```
or pass required credentials as inline options
```
(env)$ python liscrapy/scraper.py --login_email=your_linkedin@email.com --login_pass=yourpassword --keyword=python
```

# Help:

```
(env)$ python liscrapy/scraper.py --help
```
