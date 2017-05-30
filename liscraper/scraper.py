import click
from scrapy.crawler import CrawlerProcess

from liscraper.spider import LinkedInSearchSpider


@click.command()
@click.option('--login_email', prompt=True, help='Email used for LinkedIn auth')
@click.option('--login_pass', prompt=True, hide_input=True, help='Password used for LinkedIn auth')
@click.option('--keyword', prompt=True, help='Search keyword')
@click.option('--output', prompt='Output CSV file', help='CSV output filename')
@click.option('--pages', prompt=True, help='Number of pages to scrape', default=5)
def run(login_email, login_pass, keyword, output, pages):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 Gecko/20100101 Firefox/52.0',
        'FEED_FORMAT': 'CSV',
        'FEED_URI': output,
    })
    process.crawl(
        LinkedInSearchSpider,
        login_email=login_email,
        login_pass=login_pass,
        keyword=keyword,
        pages=pages
    )
    process.start()


if __name__ == '__main__':
    run()
