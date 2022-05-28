import json

from django.db.models.expressions import F
from django.http.response import JsonResponse
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from rest_framework import viewsets, status
from rest_framework.views import APIView
from tablib.core import Dataset

from .models import Product, ProductAvailability, Store, Category
from .resources import ProductResource
from .serializer import ProductSerializer, StoreSerializer, CategorySerializer


class ProductsListView(ListView):
    template_name = 'home.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context["availability"] = json.dumps(dict(ProductAvailability.choices))
        context["stores"] = json.dumps(dict(Store.objects.all().values_list('id', 'name')))
        context["categories"] = json.dumps(dict(Category.objects.all().values_list('id', 'name')))
        return context


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsUpdateView(APIView):
    serializer_class = ProductSerializer

    def post(self, request, **kwargs):
        product = Product.objects.get(id=kwargs.get("pk"))
        serializer = self.serializer_class(product, data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return JsonResponse({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return JsonResponse({"success": True}, status=200)


class ProductsBuyView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, **kwargs):
        Product.objects.filter(id=kwargs.get("pk")).update(quantity=F('quantity') - 1)
        return JsonResponse({"success": True}, status=200)


class ProductCreateView(APIView):
    serializer_class = ProductSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return JsonResponse({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return JsonResponse({"success": True}, status=200)


class ProductView(TemplateView):
    template_name = "products.html"

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context["products"] = Product.objects.filter(availability=ProductAvailability.AVAILABLE, quantity__gt=0)
        print(context["products"])
        return context


def product_import(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == "POST":
        product_resource = ProductResource()
        dataset = Dataset()
        new_products = request.FILES['file']
        imported_data = dataset.load(new_products.read())
        result = product_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            product_resource.import_data(dataset, dry_run=False)
            return JsonResponse({"success": True}, status=200)
    return JsonResponse({"error": ""}, status=400)


def store_create(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == "POST":
        create_store_data = json.loads(request.POST.get("create_store_data"))
        serializer = StoreSerializer(data=create_store_data)
        if not serializer.is_valid():
            print(serializer.errors)
            return JsonResponse({"error": serializer.errors}, status=400)
        serializer.save()
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"error": ""}, status=400)


def category_create(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == "POST":
        create_category_data = json.loads(request.POST.get("create_category_data"))
        serializer = CategorySerializer(data=create_category_data)
        if not serializer.is_valid():
            print(serializer.errors)
            return JsonResponse({"error": serializer.errors}, status=400)
        serializer.save()
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"error": ""}, status=400)
