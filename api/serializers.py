from rest_framework import serializers
from api.models import Products,Reviews,Carts
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields="__all__"

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model=Reviews
        fields=['review','rating']
    def create(self,validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Reviews.objects.create(user=user,product=product,**validated_data)
    

class CartSerializer(serializers.ModelSerializer):
    product=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model=Carts
        fields=['product','user','date']
    
    def create(self,validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Carts.objects.create(user=user,product=product,**validated_data)
    

# class UserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=[
#             "username","password","first_name","last_name","email"
#         ]

#     def create(self,validated_data):
#         return User.objects.create_user(**validated_data)