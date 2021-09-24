import scrapy
import re
import logging
import codecs
import json
from scrapy.utils.log import configure_logging
import logging
from datetime import timedelta, datetime


class QuotesSpider(scrapy.Spider):
    name = "urlspider"
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='urlspiderlog.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def start_requests(self):
        #timesOfIndiaUrlCode =; this variable increments itself as 1,
        # while we are increment the days number as 1,
        # (This *number*.cms came from timesOfIndıa.).
        timesOfIndiaUrlCode = 43101
        url=  'https://timesofindia.indiatimes.com/2018/1/1/archivelist/year-2018,month-1,starttime-43101.cms'
        date_start = datetime(2018,1,1)
        date_end = datetime(2021,9,22)
        #date_number = The number of days between the start and end date.
        date_number = date_end - date_start 
        numberOfDays=date_number.days
        for i in range(numberOfDays):
            timesOfIndiaUrlCode+=1
            yield scrapy.Request(url=url, callback=self.parse)
            self.date_start += timedelta(days=1)
            url = ("https://timesofindia.indiatimes.com/" + self.date_start.strftime('%Y/%m/%d/archivelist/year-%Y,month-%m,starttime-'+str(timesOfIndiaUrlCode)+'.cms')).replace('-0', '-').replace('/0','/')
           

    def parse(self, response):
        print(response.url)
        urlfilename = re.sub(r"\/|:", r"_", response.url)
           

        urls = response.xpath('//td[@width="49%"]//a/@href').extract()
        filename = 'urls.jl'
        with codecs.open(filename, 'a', 'utf-8') as f:
            for rl in urls:
                line = json.dumps(rl,ensure_ascii=False) + "\n"
                f.write(line)        

