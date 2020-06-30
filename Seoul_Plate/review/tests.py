from django.contrib.auth.models import User

# Create your tests here.
from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Restaurant
from review.models import Review


class ReviewTestCase(APITestCase):
    def setUp(self) -> None:
        """
        Ready before test
        Create random reviews(3) , random user(1), random restaurant(1)
        """
        self.temp_password = '12345'
        self.test_user = User.objects.create(username="test", password=self.temp_password)
        # self.test_reviews = baker.make('review.Review', _quantity=3, )
        self.test_restaurant = Restaurant.objects.create(rest_name='test1',
                                                         rest_star=3.0,
                                                         rest_address='abcd',
                                                         rest_phone_number='010123',)
        self.review = Review.objects.create(review_text="for delete",
                                            owner_rest=self.test_restaurant,
                                            owner_user=self.test_user,
                                            taste_value="SOSO",)

    def test_should_get_review(self):
        """
        Detail review information
        Request : GET - /api/review/{review_id}
        """
        test_review = self.review
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(f'/api/review/{test_review.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], test_review.id)
        self.assertEqual(response.data['review_text'], test_review.review_text)
        self.assertEqual(response.data['review_image'], test_review.review_image)
        self.assertEqual(response.data['owner_rest'], test_review.owner_rest_id)
        self.assertEqual(response.data['owner_user'], test_review.owner_user_id)

    def test_should_create_review(self):
        """
        Request : POST - /api/review
        """
        data = {"review_text": "new review",
                # "review_image": None,
                "taste_value": "SOSO",
                "owner_rest": self.test_restaurant.id,
                "owner_user": self.test_user.id,
                }
        self.client.force_authenticate(user=self.test_user)

        response = self.client.post('/api/review', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review_response = Munch(response.data)
        self.assertTrue(review_response.id)
        self.assertEqual(review_response.review_text, data['review_text'])
        self.assertEqual(review_response.owner_rest, data['owner_rest'])
        self.assertEqual(review_response.owner_user, data['owner_user'])
        # self.assertEqual(review_response.review_image, data['review_image'])

    def test_should_delete_review(self):
        """
        Request : DELETE - /api/review/{review_id}
        """
        self.client.force_authenticate(user=self.test_user)
        entry = Review.objects.get(id=self.review.id)
        response = self.client.delete(f'/api/review/{self.review.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=entry.id).exists())

    def test_should_update_review(self):
        """
        Request : PUT - /api/review/{review_id}
        """
        prev_text = self.review.review_text
        prev_taste_value = self.review.taste_value
        data = {"review_text": "updated review",
                # "review_image": None,
                "taste_value": "GOOD",
                "owner_rest": self.test_restaurant.id,
                "owner_user": self.test_user.id,
                }
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put(f'/api/review/{self.review.id}', data=data)

        review_response = Munch(response.data)
        self.assertTrue(review_response.id)
        self.assertNotEqual(review_response.review_text, prev_text)
        self.assertNotEqual(review_response.taste_value, prev_taste_value)

    def test_should_patch_review(self):
        """
        Request : PATCH - /api/review/{review_id}
        """
        prev_text = self.review.review_text
        prev_taste_value = self.review.taste_value
        data = {"review_text": "patched review",
                "taste_value": "BAD",
                }
        self.client.force_authenticate(user=self.test_user)
        response = self.client.patch(f'/api/review/{self.review.id}', data=data)

        review_response = Munch(response.data)
        self.assertTrue(review_response.id)
        self.assertNotEqual(review_response.review_text, prev_text)
        self.assertNotEqual(review_response.taste_value, prev_taste_value)
