from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from webapp.models import User, Hair, Review, Stylist

# Create your tests here.

class EntryModelTest(TestCase):

    fixtures = ['db']
    def setUp(self):
    	pass

    def test_create_stylist(self):
    	data = {'stylist_phone_number':'123456789', 'years_experience':2, 'location': 'Basement', 'client_gender':'m', 'user': 1}
    	response = self.client.post(reverse('create-stylist'), data)
    	self.assertContains(response, 'stylist_phone_number')

    # def test_lookup_stylist(self):
    #     response = self.client.get(reverse('lookup-stylist', kwargs={'stylist_id':1}))
    #     self.assertContains(response, 'location')

    # def test_create_review(self):
    #     data = {'title': 'At least my grandma likes it.', 'body': 'Lord pliss help.', 'author': 1,'rating': 3,'review_upvotes':1, 'stylist':1}
    #     response = self.client.post(reverse('create-review'), data)
    #     self.assertContains(response, 'body')




