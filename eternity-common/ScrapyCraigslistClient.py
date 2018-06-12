from mongodb.CraigslistMongoDbDao import CraigslistMongoDbDao
import datetime
import scrapy
import requests
from bs4 import BeautifulSoup
from lxml import html


class ScrapyCraigslistClient(scrapy.Spider):
    name = "craigslist_vehicle_spider"
    start_urls = ['https://sfbay.craigslist.org/search/mcy']

    def __init__(self):
        self.filename_prefix = "craigslist_vehicle_spider_detail_"
        self.filename_extension = ".html"
        self.host = "https://sfbay.craigslist.org"
        self.item_details = {}
        self.item_dao = CraigslistMongoDbDao('vehicle')
        # print(os.path.dirname(IndeedMongoDbDao.__file__))

    def load_detail_page(self):
        for index, item_tuple in enumerate(self.item_details):
            (item_id, item_detail_url) = item_tuple
            r = requests.get(item_detail_url)
            content = r.content
            detail_soup = BeautifulSoup(content, "html.parser")
            item_detail_title = detail_soup.find(
                True, {'class': ['postingtitletext']}).text
            item_detail_summary = detail_soup.find(
                True, {'id': ['postingbody']})
            str_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            try:
                if not self.item_dao.check_if_itemid_exists(item_id):
                    self.write_html(item_id, r.text, str_datetime)
                    print('Item id:{0} html file written.'.format(item_id))
                    self.item_dao.insert_item_record(
                        item_id, item_detail_title, str(item_detail_summary))
                    print('Item id:{0} db record written.'.format(item_id))
                else:
                    print('Item id:{0} already existed.'.format(item_id))
            except Exception as e:
                print(e)

    def write_html(self, item_id, text, str_datetime):
        with open(self.filename_prefix + str(item_id) + "_" + str_datetime + self.filename_extension,
                  'w') as html_writer:
            html_writer.write(text)
            html_writer.close()

    def parse(self, response):

        div = response.xpath("//*[@ id = 'sortable-results']").extract()
        soup = BeautifulSoup(div[0], 'html.parser')
        # result_items = list(soup.findAll(True, {'class': ['result-row']}))
        items = list(soup.findAll(True, {'class': ['result-row']}))
        # items = list(soup.select('a')) # data-pid
        item_detail_ids = list()
        item_detail_urls = list()
        for item in items:
            item_soup = BeautifulSoup(str(item), 'html.parser')
            attributes_dictionary = item_soup.find('li').attrs
            item_detail_ids.append(attributes_dictionary['data-pid'])
            tree = html.fromstring(str(item_soup))
            item_href = tree.xpath('//a')[0].get("href")
            item_detail_urls.append(item_href)
        self.item_details = zip(item_detail_ids, item_detail_urls)
        self.load_detail_page()
