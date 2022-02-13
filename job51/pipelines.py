# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class Job51Pipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:
    def __init__(self, host, user, password, port, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.table = table

    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS %s(
        job_id INT(20) NOT NULL,
        keyword VARCHAR(100) NOT NULL,
        job_name VARCHAR(100) NOT NULL,
        date DATETIME NOT NULL,
        company_name VARCHAR(100) NOT NULL,
        salary VARCHAR(20) NOT NULL,
        workplace VARCHAR(255) NOT NULL,
        job_exp VARCHAR(10) NOT NULL,
        job_edu VARCHAR(10) NOT NULL,
        job_rent VARCHAR(20) NOT NULL,
        company_type VARCHAR(20) NOT NULL,
        company_size VARCHAR(20) NOT NULL,
        job_welfare VARCHAR(100) NOT NULL,
        company_industry VARCHAR(100) NOT NULL,
        job_info TEXT NOT NULL,
        job_type VARCHAR(100) NOT NUll,
        PRIMARY KEY (job_id, keyword)
        );
        """ % self.table
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e.args)
        # else:
        #     self.conn.commit()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PWD'),
            port=crawler.settings.get('MYSQL_PORT'),
            database=crawler.settings.get('MYSQL_DB'),
            table=crawler.settings.get('MYSQL_TABLE'),
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(list(data.keys()))
        values = ', '.join(['%s'] * len(data.keys()))
        sql = 'REPLACE INTO %s(%s) VALUES(%s)' % (self.table, keys, values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
        except Exception as e:
            print(e.args)
            self.conn.rollback()
        else:
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()