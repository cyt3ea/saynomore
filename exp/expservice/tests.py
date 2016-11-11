from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import timezone

import json

# Create your tests here.

class ExperienceTests(TestCase):

	def setUp(self):
		pass    	

	def test_no_search_results(self):
		search = {'query': 'aslkdjsalkdjlskjdkals'}
		hairResponse = self.client.post(reverse('find-hairs'), search)
		self.assertContains(hairResponse, 'false')


	def test_search_by_name(self):
		search = {'query': 'McFlurry'}
		hairResponse = self.client.post(reverse('find-hairs'), search)
		self.assertContains(hairResponse, 'true')

	def test_search_by_stylist(self):
		search = {'query': 'Clark'}
		hairResponse = self.client.post(reverse('find-hairs'), search)
		self.assertContains(hairResponse, 'true')

	def test_search_by_price(self):
		search = {'query': 7.99}
		hairResponse = self.client.post(reverse('find-hairs'), search)
		self.assertContains(hairResponse, 'true')

	def tearDown(self):
		pass