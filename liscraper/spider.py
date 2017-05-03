import json
from collections import OrderedDict

from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest

# LinkedIn is returning localized data so it is necessary to split it using
# localized separator. Here are only three of possible separators in
# english, polish and german
OCCUPATION_SEPARATORS = [' at ', ' w ', ' bei ']


class LinkedInSearchSpider(InitSpider):
    """ Scraper for LinkedIn search people """
    name = 'linkedin_spider'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    search_url = 'https://www.linkedin.com/search/results/index/?keywords={}'

    def __init__(self, login_email, login_pass, keyword, *args, **kwargs):
        super(LinkedInSearchSpider, self).__init__(*args, **kwargs)
        self.login_email = login_email
        self.login_pass = login_pass
        self.start_urls = [self.search_url.format(keyword)]

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
        included = []
        code_elements = response.xpath('body/code/text()')
        for element in code_elements:
            try:
                jel = json.loads(element.extract())
                # extract only 'included' element from parsed json
                if 'included' in jel:
                    included.extend(jel['included'])
            except ValueError:
                # Continue and try to parse next <code></code> elements
                self.log("Problem with parsing json data.")
                continue

        results = self.extract_search_results(included)

        for item in results:
            yield self.profile_fields_parser(item)

    def extract_search_results(self, data):
        """ Extract search results from LinkedIn objects """
        search_result = None
        users = {}
        relations = {}
        locations = {}
        for i in data:
            # find object with search result object ids
            if i.get('$type') == 'com.linkedin.voyager.search.SearchCluster':
                if i.get('hitType') == 'PEOPLE':
                    search_result = i
            # save users objects
            elif i.get('$type') == 'com.linkedin.voyager.identity.shared.MiniProfile':
                users[i["objectUrn"]] = i
            # save relations between user profile and search results
            elif i.get('$type') == 'com.linkedin.voyager.search.SearchProfile':
                # extract hitId and objectUrn
                hit_id = i['$id'].split(',hitInfo')[0]
                relations[hit_id] = i['backendUrn']
                # extract location data from relation objects
                locations[i['backendUrn']] = i['location']

        if search_result is None:
            self.log('There has been problem with extracting search result')
            return []

        # Put together user profile and location data
        for user in users.values():
            user['location'] = locations.get(user['objectUrn'])

        return [users[relations[i]] for i in search_result['elements']]

    def profile_fields_parser(self, item):
        """ Parser for LinkedIn profile object. Extracts only some of user's data."""
        # For simplicity assume that if user has more occupations than one then
        # we only take the first one
        occupation = item['occupation'].split(", ")[0]
        # Naively split occupation using localized separators
        # Assume that user did not provide any company in his profile
        position = occupation
        company = ""
        # If occupation string contains separator then we will split it
        for separator in OCCUPATION_SEPARATORS:
            splited = occupation.split(separator)
            if len(splited) == 2:
                position = splited[0]
                company = splited[1]
                break

        # Split location data
        # expected formats: "city, province, country" or "city area, country"
        location = item['location']
        splited = location.split(', ', 3)
        if len(splited) >= 2:
            city = splited[0]
            country = splited[-1]
        else:
            # no way to determine
            city = ""
            country = ""

        return OrderedDict([
            ('first_name', item.get('firstName', 'Unknown')),
            ('last_name', item.get('lastName', 'Unknown')),
            ('position', position),
            ('company', company),
            ('city', city),
            ('country', country),
        ])
