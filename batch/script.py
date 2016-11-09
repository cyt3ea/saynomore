from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import time
# >>> es = Elasticsearch(['es'])
# >>> some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id':42}
# >>> es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
# {'created': True, '_version': 1, '_shards': {'successful': 1, 'total': 2, 'failed': 0}, '_index': 'listing_index', '_id': '42', '_type': 'listing'}
# >>> es.indices.refresh(index="listing_index")
# >>> es.search(index='listing_index', body={'query': {'query_string': {'query': 'macbook air'}}, 'size': 10})
# {'timed_out': False, 'hits': {'total': 1, 'hits': [{'_score': 0.10848885, '_index': 'listing_index', '_source': {'id': 42, 'description': 'This is a used Macbook Air in great condition', 'title': 'Used MacbookAir 13"'}, '_id': '42', '_type': 'listing'}], 'max_score': 0.10848885}, '_shards': {'successful': 5, 'total': 5, 'failed': 0}, 'took': 21}
# >>> 

print("HI!")
while True:
	time.sleep(30)
	es = Elasticsearch(['es'])
	try:
		consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
	except:
		time.sleep(30)
		consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
	for message in consumer:
		print(json.loads((message.value).decode('utf-8')))