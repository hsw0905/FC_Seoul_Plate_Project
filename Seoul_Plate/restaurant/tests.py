from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import Restaurant


class RestaurantTestCase(APITestCase):
    def setUp(self) -> None:
        # self.test_restaurant = baker.make('restaurant.Restaurant', _quantity=3)
        self.test_restaurant = Restaurant.objects.create(rest_name='test1',
                                                         rest_star=3.0,
                                                         rest_address='abcd',
                                                         rest_phone_number='010123',
                                                         )

        self.test_restaurant2 = Restaurant.objects.create(rest_name='test2',
                                                          rest_star=1.0,
                                                          rest_address='abaacd',
                                                          rest_phone_number='010456',
                                                          )
        self.query_set = Restaurant.objects.all()

    def test_should_list_restaurant(self):
        """
        Request : GET - /api/restaurant/
        """
        response = self.client.get('/api/restaurant/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for test_rest, response_rest in zip(self.query_set, response.data['results']):
            self.assertEqual(test_rest.id, response_rest['id'])
            self.assertEqual(test_rest.rest_name, response_rest['rest_name'])

    def test_should_detail_restaurant(self):
        """
        Request : GET - /api/restaurant/{restaurant_id}
        """
        test_restaurant = self.test_restaurant
        response = self.client.get(f'/api/restaurant/{test_restaurant.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_restaurant.id, response.data['id'])