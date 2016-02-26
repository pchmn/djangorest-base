import os
import re

from django.core.files import File
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from products.models import Product, Category


class CategoryTest(APITestCase):

    url_list = reverse("category_list")

    def setUp(self):
        # création de l'admin
        admin = User.objects.create_user('admin', password='adminpassword')
        admin.is_staff = True
        admin.save()
        # création des catégories
        c1 = Category(name="Catégorie test 1")
        c1.save()
        c2 = Category(name="Catégorie test 2")
        c2.save()

    def test_create_category_no_admin(self):
        """
        Vérifier qu'un utilisateur lambda ne peut créer de catégorie
        """
        data = {'name': 'Catégorie test create'}
        force_authenticate(self.client)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 2)

    def test_create_category_admin(self):
        """
        Vérifier qu'un admin peut créer une catégorie
        """
        data = {'name': 'Catégorie test create'}
        self.client.login(username="admin", password="adminpassword")
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.get(name=data['name']).name, data['name'])
        # suppression de la catégorie enregistrée
        Category.objects.get(name=data['name']).delete()

    def test_get_category(self):
        """
        Vérifier qu'on récupère bien la liste des catégories dans un bon format
        """
        response = self.client.get(self.url_list)
        right_response = [
            {'name': 'Catégorie test 1', 'products': 'http://testserver/products/category/1/'},
            {'name': 'Catégorie test 2', 'products': 'http://testserver/products/category/2/'}
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, right_response)


class ProductTest(APITestCase):

    url_list = reverse("product_list", args=[1])
    url_details = reverse("product_details", args=[1])
    dir_product_image = "media/product_image/"

    def setUp(self):
        # création de l'admin
        admin = User.objects.create_user('admin', password='adminpassword')
        admin.is_staff = True
        admin.save()
        # création d'une catégorie
        c1 = Category(name="Catégorie test 1")
        c1.save()
        # création des produits
        f1 = File(open("media/tests/icon-test1.png", "rb"))
        with f1:
            p1 = Product(name="Prod1", description="desc", image=f1, category=c1)
            p1.save()
        f2 = File(open("media/tests/icon-test2.png", "rb"))
        with f2:
            p2 = Product(name="Prod2", description="desc", image=f2, category=c1)
            p2.save()

    def test_create_product_no_admin(self):
        """
        Vérifier qu'un utilisateur lambda ne peut créer de produit
        """
        data = {'name': 'Prod test create', 'description': 'desc', 'image': 'http://url/', 'category': 1}
        force_authenticate(self.client)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_admin(self):
        """
        Vérifier qu'un admin peut créer une catégorie
        """
        f = File(open("media/tests/icon-test3.png", "rb"))
        with f:
            data = {'name': 'Prod test create', 'description': 'desc', 'image': f, 'category': 1}
            self.client.login(username="admin", password="adminpassword")
            response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.get(name=data['name']).name, data['name'])
        # suppression de la catégorie enregistrée
        Product.objects.get(name=data['name']).delete()

    def test_get_product_list(self):
        """
        Vérifier qu'on récupère bien la liste des catégories dans un bon format
        """
        response = self.client.get(self.url_list)
        print(response.data[0])
        right_response = [
            {'name': 'Prod1', 'description': 'desc', 'image': r'^http://', 'category': 1, 'price': 0, 'url' : r'^http://'},
            {'name': 'Prod2', 'description': 'desc', 'image': r'^http://', 'category': 1, 'price': 0, 'url' : r'^http://'},
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_details(self):
        """
        Vérifier qu'on récupère bien le détails d'un produit
        """
        response = self.client.get(self.url_details)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_purge(self):
        """
        Supprimer toutes les photos uploadées pour les tests
        """
        for f in os.listdir(self.dir_product_image):
            if re.search(r'^icon-test', f):
                os.remove(os.path.join(self.dir_product_image, f))











