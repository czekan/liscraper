from setuptools import setup, find_packages


setup(
    name="liscraper",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[
        'scrapy>=1.3.3',
        'click>=6.7'
    ],
    entry_points={
        'console_scripts': [
            'liscraper = liscraper.scraper:run',
        ],
    },
    author="Tomasz Czekanski",
    author_email="t.czekanski@gmail.com",
    description="LinkedIn search people result scraper",
    long_description="""
    Simple command line tool for scraping LinkedIn search results and saving them to CSV file.
    """,
    license="GPL",
    keywords=["linkedin", "scraper"],
    url="https://github.com/czekan/liscraper",
)
