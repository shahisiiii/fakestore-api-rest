from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.serializers import ProductModelSerializer,ReviewSerializers,CartSerializer
from api.models import Products,Reviews
from rest_framework.decorators import action
from rest_framework import authentication,permissions
# Create your views here.

class ProductsView(ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=ProductModelSerializer
    queryset=Products.objects.all()

    # def list(self,request,*args,**kwargs):
    #     qs=Products.objects.all()
    #     serializer=ProductModelSerializer(qs,many=True)
    #     return Response(data=serializer.data)
    
    # def create(self, request, *args, **kwargs):
    #     serializer=ProductModelSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         # Products.objects.create(**serializer.validated_data)
    #         return Response(data=serializer.data)
    # def retrieve(self, request, *args, **kwargs):
    #     id=kwargs.get("pk")
    #     qs=Products.objects.get(id=id)
    #     serializer=ProductModelSerializer(qs)
    #     return Response(data=serializer.data)
    # def destroy(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     Products.objects.get(id=id).delete()
    #     return Response({"msg":"deleted"})
    
    # def update(self, request, *args, **kwargs):
    #     id=kwargs.get("pk")
    #     obj=Products.objects.get(id=id)
    #     serializer=ProductModelSerializer(data=request.data,instance=obj)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #:8000/products/categories/
    @action(methods=['get'],detail=False)
    def categories(self,request,*args,**kwargs):
        qs=Products.objects.values_list('category',flat=True)
        categories=Products.objects.values_list('category',flat=True).distinct()
        return Response(data=categories)
    #:8000/products/1/add_review/
    @action(methods=['post'],detail=True)
    def add_review(self,request,*args,**kwargs):
        user=request.user
        product=self.get_object()
        serializer=ReviewSerializers(data=request.data,context={"user":user,"product":product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
    #:8000/products/1/list_reviews/
    @action(methods=['get'],detail=True)
    def list_reviews(self,request,*args,**kwargs):
        product=self.get_object()
        qs=Reviews.objects.filter(product=product)
        serializer=ReviewSerializers(qs,many=True)
        return Response(data=serializer.data)
    #:8000/products/1/add_to_cart/
    @action(methods=['post'],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        product=self.get_object()
        user=request.user
        serializer=CartSerializer(data=request.data,context={"user":user,"product":product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)



