import tempfile

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status

from account.models import Account
from advertisement.models import Advertisement, Category


def get_temporary_image():
    image = Image.new('RGB', (100, 100), color='white')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    image.save(temp_file, 'JPEG')
    temp_file.close()
    with open(temp_file.name, 'rb') as f:
        image_data = f.read()
        uploaded_image = SimpleUploadedFile(temp_file.name, image_data, content_type='image/jpeg')
        return uploaded_image


class AdvertisementViewSetTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', password='<PASSWORD>')
        self.user2 = User.objects.create_user(username='test2', password='<PASSWORD>')
        self.account1 = Account.objects.create(user=self.user1)
        self.account2 = Account.objects.create(user=self.user2)
        self.category = Category.objects.create()
        self.advertisement1 = Advertisement.objects.create(title="title1", description="description1", price=1000,
                                                           author_id=self.user1.id, category_id=self.category.id)
        self.advertisement2 = Advertisement.objects.create(title="title2", description="description2", price=2000,
                                                           author_id=self.user2.id, category_id=self.category.id)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_advertisement_without_login(self):
        main_picture = get_temporary_image()

        response = self.client.post(
            "/api/advertisement/",
            {
                "title": "title",
                "description": "description",
                "price": 12000,
                "main_picture": main_picture,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_advertisement(self):
        self.client.login(username='test1', password='<PASSWORD>')
        picture1 = default_storage.save('pictures/test1.jpg', get_temporary_image())
        picture2 = default_storage.save('pictures/test2.jpg', get_temporary_image())

        data = {
            "title": "title",
            "description": "description",
            "price": 12000,
            "pictures": [
                {"picture": picture1},
                {"picture": picture2}
            ],
            "category": self.category.id
        }
        response = self.client.post("/api/advertisement/", data, content_type='application/json')

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["author"], self.user1.id)
        self.assertEqual(response_data["status"], 1)

    def test_list_advertisement(self):
        response = self.client.get("/api/advertisement/")

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]["id"], self.advertisement1.id)
        self.assertEqual(response_data[1]["id"], self.advertisement2.id)

    def test_retrieve_advertisement(self):
        response = self.client.get("/api/advertisement/{}/".format(self.advertisement2.id))

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], self.advertisement2.id)
        self.assertEqual(response_data["title"], self.advertisement2.title)
        self.assertEqual(response_data["description"], self.advertisement2.description)

    def test_update_advertisement_no_access(self):
        self.client.login(username='test1', password='<PASSWORD>')

        response = self.client.patch(
            "/api/advertisement/{}/".format(self.advertisement2.id),
            {
                "title": "changed title",
            },
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_advertisement_have_access(self):
        self.client.login(username='test1', password='<PASSWORD>')

        response = self.client.patch(
            "/api/advertisement/{}/".format(self.advertisement1.id),
            {
                "title": "changed title",
            },
            content_type='application/json',
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["title"], "changed title")
