from django.test import TestCase
from webapp.models import User, Hair, Review, Stylist

# Create your tests here.

class EntryModelTest(TestCase):

    def setUp(self):
    	Stylist.objects.create(stylist_phone_number='123456789', years_experience='2', location='Basement', client_gender='m')
    	Stylist.objects.create(stylist_phone_number='987654321', years_experience='1', location='Ceiling', client_gender='m')
    def test_stylist_years(self):
    	x = Stylist.objects.get(client_gender='m', location='Basement')
    	self.assertEqual(x.years_experience, 2)

    def test_stylist_phone_number(self):
    	x = Stylist.objects.get(client_gender='m', location='Ceiling')
    	self.assertEqual(x.stylist_phone_number, '123456789')


