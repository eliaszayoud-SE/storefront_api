from django.contrib.auth.models import User
from rest_framework import status
import pytest
from model_bakery import baker
from store.models import Collection

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous_returns_401(self, create_collection):
        responce = create_collection({'title':'a'})

        assert responce.status_code == status.HTTP_401_UNAUTHORIZED 

    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
        authenticate()
        
        responce = create_collection({'title':'a'})

        assert responce.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_collection, authenticate):
        authenticate(is_staff=True)
        
        responce = create_collection({'title':''})

        assert responce.status_code == status.HTTP_400_BAD_REQUEST
        assert responce.data['title'] is not None         


    def test_if_data_is_valid_returns_201(self, create_collection, authenticate):

        authenticate(is_staff=True)
        responce = create_collection({'title':'a'})

        assert responce.status_code == status.HTTP_201_CREATED
        assert responce.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        # Arrange
        collection = baker.make(Collection)

        # Act
        responce = api_client.get(f'/store/collections/{collection.id}/')

        # Assert
        assert responce.status_code == status.HTTP_200_OK
        assert responce.data == {
            'id':collection.id,
            'title':collection.title,
            'products_count':0
        }