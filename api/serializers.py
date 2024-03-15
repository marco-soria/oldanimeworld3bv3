from rest_framework import serializers

from .models import (
    Category, Product, Client, Order, OrderDetail
)
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
                
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['product_image'] = instance.product_image.url
        representation['category_name'] = instance.category_id.category_name
        return representation
    
class CategoryProductSerializer(serializers.ModelSerializer):
    Products = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['category_id','category_name','Products']
        
##### serializers para pedidos
class OrderProductSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product_id','orderdetail_quantity']
        
class OrderSerializerPOST(serializers.ModelSerializer):
    orderproducts = OrderProductSerializerPOST(many=True)
    
    class Meta:
        model = Order
        fields = ['order_registerdate','order_state','client_id',
                  'orderproducts']
        
    def create(self,validated_data):
        lista_pedido_plato = validated_data.pop('pedidoplatos')
        order = Product.objects.create(**validated_data)
        for obj_pedido_plato in lista_pedido_plato:
            OrderDetail.objects.create(order_id=order,**obj_pedido_plato)
        return order
    
#### serializers para pedido GET
class PedidoPlatoSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = PedidoPlato
        fields = ['pedidoplato_id','pedidoplato_cant','plato_id']
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['plato_nom'] = instance.plato_id.plato_nom
        representation['plato_img'] = instance.plato_id.plato_img.url
        return representation
        
class PedidoSerializerGET(serializers.ModelSerializer):
    pedidoplatos = PedidoPlatoSerializerGET(many=True,read_only=True)
    
    class Meta:
        model = Pedido
        fields = ['pedido_id','pedido_fecha','pedido_estado',
                  'usu_id','mesa_id','pedidoplatos']
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['usu_name'] = instance.usu_id.username
        return representation
            
        