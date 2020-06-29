from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from bookmarks.models import Bookmark
from restaurant.models import Restaurant


class BookMarkTestCode(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='adasd', password='12345')

        self.users = baker.make('auth.User', _quantity=4)

        self.restaurant = Restaurant.objects.create(rest_name='test1',
                                                    rest_star=3.0,
                                                    rest_address='abcd',
                                                    rest_phone_number='010123',)

    def test_bookmark_create(self):
        self.client.force_authenticate(user=self.user)
        data = {'restaurant': self.restaurant.id, 'bookmarked_user': self.user.id}

        response = self.client.post('/api/bookmark/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['id'])
        self.assertEqual(response.data['restaurant'], data['restaurant'])

    def test_bookmark_delete(self):
        self.client.force_authenticate(user=self.user)
        test_bookmark = Bookmark.objects.create(bookmarked_user_id=self.user.id, restaurant_id=self.restaurant.id)
        response = self.client.delete(f'/api/bookmark/{test_bookmark.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Bookmark.objects.filter(id=test_bookmark.id).exists())

    def test_bookmark_duplicate(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'restaurant': self.restaurant.id, 'bookmarked_user': self.user.id
        }
        response = self.client.post('/api/bookmark/', data=data)
        print(response)
        response2 = self.client.post('/api/bookmark/', data=data)
        print(response2)
        self.assertEqual(Bookmark.objects.filter(restaurant=data['restaurant'], bookmarked_user=self.user).count(), 1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bookmark_count(self):
        for i in range(3):
            self.client.force_authenticate(user=self.users[i])
            data = {
                'restaurant': self.restaurant.id, 'bookmarked_user': self.users[i].id,
            }
            response = self.client.post('/api/bookmark/', data=data)

        self.assertEqual(Bookmark.objects.filter(restaurant=self.restaurant).count(), 3)