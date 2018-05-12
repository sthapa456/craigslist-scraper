## Synopsis

This project is intended to create a web scrapping framework to aid implementation of simple web scrapper.  Given the search listing page and some unique css id/class to identify the items, the scrapper will scan these items for their href links and will then access these links to get the item title and detail before storing into html file and to MongoDB for future analytic purpose.

## Code Example

How to execute the script:
	
	In command prompt, scrapy runspider ScrapyIndeedClient.py

## Motivation

	Quick and easy implementation of web scrapping on web site with simple layout

## Installation

Pre-requisite:

	1. Python 3.6.x
	2. Scrapy module for Python 3.6.x	

## API Reference

	Future works:
		
		1. Development API for easier reusability 
		2. Analytic API for text analysis

## Tests

	CraigslistMongoDbDaoTest.py class contains the MongoDB DAO layer testing, require MongoDB to installed with default port

## Contributors

	Raymond wai yan Ko

## License

	TBD
