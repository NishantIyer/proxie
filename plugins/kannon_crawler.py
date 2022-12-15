import sys
import threading
import traceback
import time
from random import shuffle
from html.parser import HTMLParser

import requests
import elasticsearch

es = elasticsearch.Elasticsearch()


class WorkQueue():
    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()

    def __len__(self):
        return len(self._queue)

    def put(self, task):
        with self._lock:
            self._queue.append(task)

    def get(self):
        with self._lock:
            shuffle(self._queue)
            return self._queue.pop()

    def qsize(self):
        return len(self)


work_queue = WorkQueue()
doc_set = set()
search_set = set()

http_session = requests.Session()
http_session.headers.update({'Authorization': 'Token c5f8198fc82933df0bc328b5fe65125c9e7fe34a'})

seed_queries = ['india+doctypes:judgments', 'supremecourt+doctypes:judgments', 'delhi+doctypes:judgments',
                'bombay+doctypes:judgments', 'kolkata+doctypes:judgments', 'chennai+doctypes:judgments',
                'allahabad+doctypes:judgments', 'andhra+doctypes:judgments', 'chattisgarh+doctypes:judgments',
                'gauhati+doctypes:judgments', 'jammu+doctypes:judgments', 'srinagar+doctypes:judgments',
                'kerala+doctypes:judgments', 'lucknow+doctypes:judgments', 'orissa+doctypes:judgments',
                'uttaranchal+doctypes:judgments', 'gujarat+doctypes:judgments', 'himachal_pradesh+doctypes:judgments',
                'jharkhand+doctypes:judgments', 'karnataka+doctypes:judgments', 'madhyapradesh+doctypes:judgments',
                'patna+doctypes:judgments', 'punjab+doctypes:judgments', 'rajasthan+doctypes:judgments',
                'sikkim+doctypes:judgments', 'kolkata+doctypes:judgments', 'jodhpur+doctypes:judgments',
                'patna_orders+doctypes:judgments', 'meghalaya+doctypes:judgments']


class Cleaner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def add_doc(doc_id):
    if doc_id not in doc_set:
        work_queue.put({'type': 'doc', 'payload': doc_id})
        doc_set.add(doc_id)


def add_search(query_dict):
    query_dict['keyword'] = query_dict['keyword'].strip()
    if (query_dict['keyword'], query_dict['page']) not in search_set:
        work_queue.put({'type': 'search', 'payload': query_dict})
        search_set.add((query_dict['keyword'], query_dict['page']))


def search(query_dict):
    print('Performing search: %s' % query_dict)
    keyword = query_dict['keyword']
    page = query_dict['page']
    time.sleep(5)
    response = http_session.post('https://api.indiankanoon.org/search/?formInput=%s&pagenum=%s' % (keyword, page))
    resp_json = response.json()
    for doc in resp_json['docs']:
        add_doc(doc['tid'])
    for category in resp_json['categories']:
        if 'Related Queries' in category:
            for item in category[1]:
                add_search({'keyword': item['value'], 'page': 0})
    if page < 20:
        add_search({'keyword': keyword, 'page': page + 1})


def load_doc(doc_id):
    time.sleep(5)
    response = http_session.post('https://api.indiankanoon.org/doc/%s/' % doc_id)
    resp_json = response.json()
    index = resp_json['divtype']
    del resp_json['divtype']

    # Handle citations
    cited_by_list = []
    for cite in resp_json['citedbyList']:
        doc_id = cite['tid']
        cited_by_list.append(doc_id)
        add_doc(doc_id)
    resp_json['citedbyList'] = cited_by_list
    cite_list = []
    for cite in resp_json['citeList']:
        doc_id = cite['tid']
        cite_list.append(doc_id)
        add_doc(doc_id)
    resp_json['citeList'] = cite_list

    # Clean doc
    parser = Cleaner()
    parser.feed(resp_json['doc'])
    resp_json['doc'] = parser.get_data()

    es.index(index=index, doc_type='json', body=resp_json, id=doc_id)
    print('Indexed doc with ID %s' % doc_id)


def worker():
    while True:
        try:
            task = work_queue.get()
            if task['type'] == 'search':
                search(task['payload'])
            else:
                load_doc(task['payload'])
        except Exception:
            traceback.print_exc()


def add_init_tasks():
    for query in seed_queries:
        add_search({'keyword': query, 'page': 0})


def doc_count():
    while True:
        print('Number of tasks: %s' % work_queue.qsize())
        time.sleep(10)


def main():
    add_init_tasks()

    threads = []
    for i in range(int(sys.argv[1])):
        th = threading.Thread(target=worker)
        th.start()
        threads.append(th)

    doc_show = threading.Thread(target=doc_count)
    doc_show.start()
    threads.append(doc_show)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()