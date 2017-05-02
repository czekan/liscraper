import json

from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest


class LinkedInSearchSpider(InitSpider):
    """ Scraper for LinkedIn search people """
    name = 'linkedin_spider'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = [
        'https://www.linkedin.com/search/results/index/?keywords=python',
    ]

    def __init__(self, login_email, login_pass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_email = login_email
        self.login_pass = login_pass

    def init_request(self):
        """Before crawling starts make a request for login form."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Make login request with authorization credentials."""
        return FormRequest.from_response(
            response,
            formdata={
                'session_key': self.login_email,
                'session_password': self.login_pass
            },
            callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        # check if response contains cookie with authentication data
        if b'lidc' in response.headers.get('Set-Cookie'):
            self.log("Successfully logged in.")
            return self.initialized()
        else:
            self.log("There has been problem with login.")

    def parse(self, response):
        """Parse search response."""
        self.log("TODO Parsing")
