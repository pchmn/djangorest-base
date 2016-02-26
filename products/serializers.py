from rest_framework import serializers

from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer pour la classe Category
    on affiche le nom et les produits (liens) de la catégorie
    """
    products = serializers.HyperlinkedIdentityField(view_name='product_list')

    class Meta:
        model = Category
        fields = ('name', 'products')


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer pour la classe Product
    on affiche le nom, la description, le prix et l'image du produit
    """
    url = serializers.HyperlinkedIdentityField(view_name='product_details')

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price', 'image', 'url')
