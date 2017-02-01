from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import time
import json

# es = Elasticsearch(['es'])
# some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id':42}
# es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
# {'created': True, '_version': 1, '_shards': {'successful': 1, 'total': 2, 'failed': 0}, '_index': 'listing_index', '_id': '42', '_type': 'listing'}
# es.indices.refresh(index="listing_index")
# es.search(index='listing_index', body={'query': {'query_string': {'query': 'macbook air'}}, 'size': 10})
# {'timed_out': False, 'hits': {'total': 1, 'hits': [{'_score': 0.10848885, '_index': 'listing_index', '_source': {'id': 42, 'description': 'This is a used Macbook Air in great condition', 'title': 'Used MacbookAir 13"'}, '_id': '42', '_type': 'listing'}], 'max_score': 0.10848885}, '_shards': {'successful': 5, 'total': 5, 'failed': 0}, 'took': 21}

while True:
	time.sleep(90)
	hair_fixture_one = {'price' : 18.77, 'stylist' : 'Robby McJimbers', 'hair_upvotes' : 2,	'name': 'McFlurry', 'id': 1}
	hair_fixture_two = {'price' : 7.99, 'stylist' : 'Clark McHarrington', 'hair_upvotes' : 1,	'name': 'The Womanizer', 'id': 2}
	es = Elasticsearch(['es'])
	es.index(index='listing_index', doc_type='listing', id=hair_fixture_one['id'], body=hair_fixture_one)
	es.index(index='listing_index', doc_type='listing', id=hair_fixture_two['id'], body=hair_fixture_two)
	es.indices.refresh(index="listing_index")
	try:
		consumer = KafkaConsumer('new-hair-listing', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
	except:
		time.sleep(30)
		consumer = KafkaConsumer('new-hair-listing', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
	for message in consumer:
		print(json.loads((message.value).decode('utf-8')))
		some_new_listing = json.loads((message.value).decode('utf-8'))
		es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
		es.indices.refresh(index="listing_index")