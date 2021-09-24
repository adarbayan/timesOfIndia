import scrapy
import json
import codecs
import re
from scrapy.utils.log import configure_logging
import logging

class QuotesSpider(scrapy.Spider):
    name = "sp"
    count = 0

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def start_requests(self):
        with codecs.open("new_urls.jl",'r','utf-8') as f:
            urls = f.readlines()
        for url in urls:
            url = re.sub(r"\n| |\r|\"", r"", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(re.findall(r"\d+", response.url)[-1])
        filename = re.sub(r"\/|:", r"_", response.url)
        with open("./news/%s" %filename , 'wb') as f:
            f.write(response.body)
#farkli filelara url ismi file ismi olcak sekilde indir
