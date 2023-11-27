import json
import csv
import os
import re
import mysql.connector
import string
import nltk
from nltk.corpus import stopwords


class JsonExportPipeline:
    def __init__(self):
        self.file = open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        item['post_description'] = self.remove_html_tags(item['post_description'])
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

    def remove_html_tags(self, html):
        tmp = html.replace('\n', '')
        tag_pattern = re.compile(r'<.*?>')
        text = re.sub(tag_pattern, '', tmp)
        return text


class CsvExportPipeline:
    def __init__(self):
        if os.path.exists('data.csv'):
            self.csv_file = open('data.csv', 'a', newline='', encoding='utf-8')
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=['title', 'post_url', 'company_name', 'company_location', 'post_description'])
        else:
            self.csv_file = open('data.csv', 'w', newline='', encoding='utf-8')
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=['title', 'post_url', 'company_name', 'company_location', 'post_description'])
            self.csv_writer.writeheader()

    def process_item(self, item, spider):
        item['post_description'] = self.remove_html_tags(item['post_description'])
        self.csv_writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.csv_file.close()

    def remove_html_tags(self, html):
        tmp = html.replace('\n', '')
        tag_pattern = re.compile(r'<.*?>')
        text = re.sub(tag_pattern, '', tmp)
        return text


class MySQLPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.get('MYSQL_SETTINGS', {})
        return cls(db_settings)

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(**self.db_settings)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        item['post_description'] = self.preprocessing(item['post_description'])
        sql = "INSERT INTO post_list (title, post_url, company_name, company_location, scraped_date, post_description) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            item['title'],
            item['post_url'],
            item['company_name'],
            item['company_location'],
            item['scraped_date'],
            item['post_description']
        )

        self.cursor.execute(sql, values)
        return item

    def preprocessing(self, text):
        tmp = text.replace('\n', '')
        tag_pattern = re.compile(r'<.*?>')
        text = re.sub(tag_pattern, '', tmp)

        words = text.split()

        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        words = [re_punc.sub('', w) for w in words]
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english')).union(set(stopwords.words('french')))
        words = [w for w in words if not w in stop_words]

        text = ' '.join(words)
        return text



