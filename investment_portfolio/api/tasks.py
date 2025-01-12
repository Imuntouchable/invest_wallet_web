from celery import shared_task
import redis
import json
from .models import User, Asset
from .serializers import UserSerializer, AssetSerializer

r = redis.StrictRedis(host='localhost', port=6379, db=0)
CACHE_TTL = 10


@shared_task
def update_user_cache():
    users = User.objects.all()
    serialized_users = UserSerializer(users, many=True).data
    r.setex('user_list', CACHE_TTL, json.dumps(serialized_users))


@shared_task
def update_asset_cache():
    assets = Asset.objects.all()
    serialized_assets = AssetSerializer(assets, many=True).data
    r.setex('asset_list', CACHE_TTL, json.dumps(serialized_assets))
