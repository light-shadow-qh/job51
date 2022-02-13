# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Job51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fieldnames = [
        'job_id',
        'keyword',
        'job_name',
        'date',
        'company_name',
        'salary',
        'workplace',
        'job_exp',
        'job_edu',
        'job_rent',
        'company_type',
        'company_size',
        'job_welfare',
        'company_industry',
        'job_info',
        'job_type',
    ]
    for field in fieldnames:
        exec('%s = Field()' % field)

