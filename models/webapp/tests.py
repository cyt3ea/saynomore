from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import timezone
from webapp.models import User, Hair, Review, Stylist

# Create your tests here.

class ModelsTests(TestCase):

    fixtures = ['db']
    def setUp(self):
    	pass    	

    #TESTING REVIEW MODEL BELOW
    def test_create_review(self):
    	data = {'title':'Wowserz', 'body':'I am befuddled.', 'author':1, 'rating':3, 'review_upvotes':10, 'stylist':1} 
    	response = self.client.post(reverse('create-review'), data)
    	self.assertContains(response, 'title')

    def test_lookup_review(self):
    	response = self.client.get(reverse('lookup-review', kwargs={'review_id':1}))
    	self.assertContains(response, 'title')

    def test_delete_review(self):
    	response=self.client.delete(reverse('delete-review', kwargs={'review_id':1}))
    	self.assertNotContains(response, 'title')

    def test_update_review(self):
    	data = {'title':'YAAAAS'}
    	response=self.client.post(reverse('update-review', kwargs={'review_id':2}), data)
    	self.assertContains(response, "YAAAAS")

    #TESTING STYLIST MODEL BELOW
    def test_create_stylist(self):
    	data1 = {'stylist_phone_number':'123456789', 'years_experience':2, 'location': 'Basement', 'client_gender':'m', 'user': 1}
    	response1 = self.client.post(reverse('create-stylist'), data1)
    	self.assertContains(response1, 'stylist_phone_number')

    	data2 = {'stylist_phone_number':'24681012', 'years_experience':45, 'location': 'Cuba', 'client_gender':'f', 'user': 2}
    	response2 = self.client.post(reverse('create-stylist'), data2)
    	self.assertContains(response2, 'stylist_phone_number')

    def test_lookup_stylist(self):
    	response = self.client.get(reverse('lookup-stylist', kwargs={'stylist_id':1}))
    	self.assertContains(response, 'stylist_phone_number')
    
    def test_delete_stylist(self):
    	response=self.client.delete(reverse('delete-stylist', kwargs={'stylist_id':1}))
    	self.assertNotContains(response, 'stylist_phone_number')

    def test_update_stylist(self):
    	data = {'years_experience':15}
    	response=self.client.post(reverse('update-stylist', kwargs={'stylist_id':2}), data)
    	# print("Updated stylist: " + str(response.content))
    	self.assertContains(response, 15)

    def test_all_stylists(self):
    	response = self.client.get(reverse('all-stylists'))
    	# print("All stylists in fixture: " + str(response.content))
    	self.assertContains(response, 'stylist_phone_number')

    #TESTING HAIR MODEL BELOW
    def test_create_hair(self):
        data = {'location': 'TrashCan', 'price':9, 'hair_phone_number':'123456789', 'stylist':2, 'hair_upvotes': 9, 'author': 2, 'name': 'janx'}
        response = self.client.post(reverse('create-hair'), data)
        self.assertContains(response, 'price')

    def test_lookup_hair(self):
        response = self.client.get(reverse('lookup-hair', kwargs={'hair_id':1}))
        self.assertContains(response, 'price')
    
    def test_delete_hair(self):
        response=self.client.delete(reverse('delete-hair', kwargs={'hair_id':1}))
        self.assertNotContains(response, 'price')

    def test_update_hair(self):
        data = {'hair_upvotes':15}
        response=self.client.post(reverse('update-hair', kwargs={'hair_id':1}), data)
        self.assertContains(response, 15)

    def test_popular_hair(self):
        response = self.client.get(reverse('popular-hairs'))
        self.assertContains(response, 'price')

    def test_all_hair(self):
        response = self.client.get(reverse('all-hairs'))
        #print("All hairs in fixture: " + str(response.content))
        self.assertContains(response, 'price')  

    #TESTING USER MODEL BELOW 
    def test_create_user(self):
        data = {'username':'jujuOnTheBeat', 'date_joined': timezone.now(), 'f_name': 'Nick', 'l_name': 'Qua', 'password':'jujubeans', 'is_active': 'true'}
        response = self.client.post(reverse('create-user'), data)
        self.assertContains(response, 'f_name')

    def test_lookup_user(self):
        response = self.client.get(reverse('lookup-user', kwargs={'user_id':2}))
        self.assertContains(response, 'f_name')
    
    def test_delete_user(self):
        response=self.client.delete(reverse('delete-user', kwargs={'user_id':1}))
        self.assertNotContains(response, 'f_name')

    def test_update_user(self):
        data = {'f_name':'Phatcheeekan'}
        response=self.client.post(reverse('update-user', kwargs={'user_id':2}), data)
        self.assertContains(response, 'Phatcheeekan')

    def tearDown(self):
    	pass