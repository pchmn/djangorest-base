from rest_framework import generics
from rest_framework.decorators import permission_classes

from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer
from products.permissions import IsAdminOrReadOnly


@permission_classes((IsAdminOrReadOnly,))
class CategoryList(generics.ListCreateAPIView):
    """
    Permet de :
        • récupérer la liste des catégories
        • créer une nouvelle catégorie si admin
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@permission_classes((IsAdminOrReadOnly,))
class ProductList(generics.ListCreateAPIView):
    """
    Permet de :
        • récupérer la liste des produits d'une catégorie
        • créer un nouveau produit si admin
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = self.kwargs['pk']
        return Product.objects.filter(category=category)


@permission_classes((IsAdminOrReadOnly,))
class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Permet de :
        • récupérer le détails d'un produit
        • modifier, supprimer un produit si admin
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
