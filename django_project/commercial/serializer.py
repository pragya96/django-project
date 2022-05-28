from rest_framework import serializers
from .models import Product, Store, Category


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'store', 'availability', 'name', 'quantity', 'price', 'description', 'category')

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['name'].required = False
        self.fields['availability'].required = False
        self.fields['store'].required = False

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret["availability"] = obj.get_availability_display()
        ret["category"] = obj.category.name if obj.category else ""
        ret["store"] = obj.store.name if obj.store else ""
        return ret


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
