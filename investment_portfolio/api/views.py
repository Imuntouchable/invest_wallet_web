import redis
import json
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Asset
from .serializers import UserSerializer, AssetSerializer
from .tasks import update_user_cache, update_asset_cache
from confluent_kafka import Producer


r = redis.StrictRedis(host='localhost', port=6379, db=0)
kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'django-service'
}
producer = Producer(kafka_config)


def send_kafka_message(topic, message):
    producer.produce(topic, value=json.dumps(message))
    producer.flush()


def get_cached_user_list():
    cached_data = r.get('user_list')
    if cached_data:
        return json.loads(cached_data)
    return None


def get_cached_asset_list():
    cached_data = r.get('asset_list')
    if cached_data:
        return json.loads(cached_data)
    return None


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        cached_data = get_cached_user_list()
        if cached_data:
            return Response(cached_data)
        update_user_cache.delay()
        users = self.get_queryset()
        serialized_data = UserSerializer(users, many=True).data
        send_kafka_message(
            'user_cache_update',
            {'event': 'cache_miss', 'users': serialized_data}
        )
        return Response(serialized_data)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def list(self, request, *args, **kwargs):
        cached_data = get_cached_asset_list()
        if cached_data:
            return Response(cached_data)
        update_asset_cache.delay()
        assets = self.get_queryset()
        serialized_data = AssetSerializer(assets, many=True).data
        send_kafka_message(
            'asset_cache_update',
            {'event': 'cache_miss', 'assets': serialized_data}
        )
        return Response(serialized_data)
