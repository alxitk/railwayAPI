from django.contrib.auth import get_user_model
from stations.models import Train, TrainType
from stations.serializers import TrainSerializer
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


TRAIN_URL = reverse("stations:train-list")


def sample_train(**params):
    defaults = {
        "name": "test Bus",
        "cargo": 20,
        "places_in_cargo": 10,
    }
    defaults.update(params)
    return Train.objects.create(**defaults)

class UnAuthTrainApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_auth_required(self):
        response = self.client.get(TRAIN_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthTrainApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="<EMAIL>",
            password="<PASSWORD>",
        )
        self.client.force_authenticate(user=self.user)


    def test_train_list(self):
        sample_train()

        train_with_type = sample_train()
        train_type = TrainType.objects.create(name="test type")

        train_with_type.train_type = train_type
        train_with_type.save()

        response = self.client.get(TRAIN_URL)
        trains =Train.objects.all()
        serializer = TrainSerializer(trains, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_trains_by_train_type(self):
        train_without_train_type = sample_train()
        train_with_train_type = sample_train(name="test train 1")
        train_type = TrainType.objects.create(name="test train type")

        train_with_train_type.train_type = train_type
        train_with_train_type.save()

        response = self.client.get(
            TRAIN_URL,
            {"train_type": f"{train_type.id}"}
        )

        serializer_without_train_type = TrainSerializer(train_without_train_type)
        serializer_with_train_type = TrainSerializer(train_with_train_type)

        self.assertIn(serializer_with_train_type.data, response.data["results"])
        self.assertNotIn(serializer_without_train_type.data, response.data["results"])

    def test_retrieve_train_detail(self):
        train = sample_train()
        train_type = TrainType.objects.create(name="test type")
        train.train_type = train_type
        train.save()

        url = reverse("stations:train-detail", kwargs={"pk": train.pk})

        response = self.client.get(url)

        serializer = TrainSerializer(train)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_train_forbidden(self):
        payload = {
            "name": "test Bus",
            "cargo": 20,
            "places_in_cargo": 10,
        }

        response = self.client.post(TRAIN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="<EMAIL>",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_train(self):
        payload = {
            "name": "test Bus",
            "cargo": 20,
            "places_in_cargo": 10,
        }

        response = self.client.post(TRAIN_URL, payload)
        train = Train.objects.get(id=response.data["id"])

        for key in payload:
            self.assertEqual(payload[key], getattr(train, key))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_train_with_train_type(self):
        train_type = TrainType.objects.create(name="test type")
        payload = {
            "name": "test Bus",
            "cargo": 20,
            "places_in_cargo": 10,
            "train_type": train_type.name,
        }

        response = self.client.post(TRAIN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        train = Train.objects.get(id=response.data["id"])
        self.assertEqual(train.train_type, train_type)
        self.assertEqual(TrainType.objects.count(), 1)


















