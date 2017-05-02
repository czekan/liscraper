import click
from scrapy.crawler import CrawlerProcess

from spider import LinkedInSearchSpider


@click.command()
@click.option('--login_email', prompt=True, help='Email used for LinkedIn auth')
@click.option('--login_pass', prompt=True, hide_input=True, help='Password used for LinkedIn auth')
def run(login_email, login_pass):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 Gecko/20100101 Firefox/52.0',
    })
    process.crawl(
        LinkedInSearchSpider,
        login_email=login_email,
        login_pass=login_pass,
    )
    process.start()


if __name__ == '__main__':
    run()
