from fastapi.testclient import TestClient

from app.product_listing_controller import app

import os
import requests

client = TestClient(app)


class ValueStorageProductListingCRUD:
    product_listing_ids = []
    user_ids = []
    access_token_admin = None
    access_token = None


class TestSuiteProductListingCRUD:
    def test_create_user_admin(self):
        user_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameProductListingAdmin",
                "email": "test@example.com",
                "password": "testPassword",
                "is_admin": True,
            },
        )

        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageProductListingCRUD.user_ids.append(user_response.json()["id"])

    def test_create_user(self):
        user_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameProductListing",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )

        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageProductListingCRUD.user_ids.append(user_response.json()["id"])

    def test_login_admin(self):
        response = client.post(
            "/login",
            data={
                "username": "testUsernameProductListingAdmin",
                "password": "testPassword",
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageProductListingCRUD.access_token_admin = response.json()[
            "access_token"
        ]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameProductListing", "password": "testPassword"},
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageProductListingCRUD.access_token = response.json()["access_token"]

    def test_create_product_listing_with_id(self):
        response = client.post(
            "/product-listings",
            json={
                "id": "testID",
                "seller": {"id": ValueStorageProductListingCRUD.user_ids[1]},
                "product": {
                    "name": "Surface Pro 7",
                    "brand": "Surface",
                    "category": "REFURBISHED_PRODUCT",
                    "sub_category": "LAPTOP",
                },
                "listed_price": 319.99,
            },
            headers={
                "Authorization": "Bearer " + ValueStorageProductListingCRUD.access_token
            },
        )
        assert response.status_code == 201
        assert response.json() == {"id": "testID"}
        ValueStorageProductListingCRUD.product_listing_ids.append(response.json()["id"])

    def test_create_product_listing_without_id(self):
        response = client.post(
            "/product-listings",
            json={
                "seller": {"id": ValueStorageProductListingCRUD.user_ids[1]},
                "product": {
                    "name": "Surface Pro 7",
                    "brand": "Surface",
                    "category": "REFURBISHED_PRODUCT",
                    "sub_category": "LAPTOP",
                },
                "listed_price": 319.99,
            },
            headers={
                "Authorization": "Bearer " + ValueStorageProductListingCRUD.access_token
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageProductListingCRUD.product_listing_ids.append(response.json()["id"])

    def test_create_product_listing_already_exists_same_id(self):
        response = client.post(
            "/product-listings",
            json={
                "id": "testID",
                "seller": {"id": ValueStorageProductListingCRUD.user_ids[1]},
                "product": {
                    "name": "Surface Pro 7",
                    "brand": "Surface",
                    "category": "REFURBISHED_PRODUCT",
                    "sub_category": "LAPTOP",
                },
                "listed_price": 319.99,
            },
            headers={
                "Authorization": "Bearer " + ValueStorageProductListingCRUD.access_token
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Product listing already exists"}

    def test_get_product_listings(self):
        response = client.get(
            "/product-listings",
            headers={
                "Authorization": "Bearer " + ValueStorageProductListingCRUD.access_token
            },
        )
        assert response.status_code == 200
        assert len(response.json()) >= 2

    def test_get_product_listing_by_id(self):
        response = client.get(
            "/product-listings/testID",
            headers={
                "Authorization": "Bearer " + ValueStorageProductListingCRUD.access_token
            },
        )
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert (
            response.json()["seller"]["id"]
            == ValueStorageProductListingCRUD.user_ids[1]
        )
        assert response.json()["product"]["name"] == "Surface Pro 7"
        assert response.json()["product"]["brand"] == "Surface"
        assert response.json()["product"]["category"] == "REFURBISHED_PRODUCT"
        assert response.json()["product"]["sub_category"] == "LAPTOP"
        assert response.json()["listed_price"] == 319.99

    def test_get_product_listing_by_id_not_found(self):
        response = client.get(
            f"/product-listings/notFoundID",
            headers={
                "Authorization": "Bearer " + ValueStorageProductListingCRUD.access_token
            },
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Product listing not found"}

    # def test_update_product_listing_by_id(self):
    #     response = client.patch(
    #         "/product-listings/testID",
    #         json={"listed_price": 349.99},
    #         headers={
    #             "Authorization": "Bearer " + ValueStorageProductListingCRUD.access_token
    #         },
    #     )
    #     assert response.status_code == 200
    #     assert response.json()["id"] == "testID"
    #     assert (
    #         response.json()["seller"]["id"]
    #         == ValueStorageProductListingCRUD.user_ids[0]
    #     )
    #     assert response.json()["product"]["name"] == "Surface Pro 7"
    #     assert response.json()["product"]["brand"] == "Surface"
    #     assert response.json()["product"]["category"] == "REFURBISHED_PRODUCT"
    #     assert response.json()["product"]["sub_category"] == "LAPTOP"
    #     assert response.json()["listed_price"] == 349.99

    def test_delete_product_listing_by_id(self):
        for id in ValueStorageProductListingCRUD.product_listing_ids:
            response = client.delete(
                f"/product-listings/{id}",
                headers={
                    "Authorization": "Bearer "
                    + ValueStorageProductListingCRUD.access_token
                },
            )
            assert response.status_code == 200
            assert response.json() == {"id": id}

    def test_delete_user(self):
        # Delete users starting from the last one because the first one has the access token
        for user_id in ValueStorageProductListingCRUD.user_ids[::-1]:
            user_response = requests.delete(
                os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/users/" + user_id,
                headers={
                    "Authorization": "Bearer "
                    + ValueStorageProductListingCRUD.access_token_admin
                },
            )

            assert user_response.status_code == 200
            assert "id" in user_response.json()
