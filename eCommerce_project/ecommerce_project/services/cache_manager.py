import redis
import json
import os
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

class CacheManager:
    def __init__(self):
        self.redis = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            password=os.getenv('REDIS_PASSWORD'),
            db=0,
            decode_responses=True
        )
        try:
            self.redis.ping()
            print("Connected to redis")
        except:
            print("Not connected to redis.")
            self.redis = None
    
    def get(self, key: str):
        if not self.redis:
            return None
        
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value, seconds: int = 300):
        if not self.redis:
            return
        
        self.redis.setex(key, seconds, json.dumps(value))
    
    def delete_pattern(self, pattern: str):
        if not self.redis:
            return
        
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)
            print(f"Cache deleted.")
    
    def cache_get(self, key_prefix: str, ttl: int = 300):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{key_prefix}:{func.__name__}"
                
                cached = self.get(cache_key)
                if cached:
                    print(f"Retrieved from cache")
                    return cached
                
                print(f"Retrieved from db")
                result = func(*args, **kwargs)
                
                self.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator
    
    def cache_get_one(self, key_prefix: str, ttl: int = 300):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                item_id = args[0] if args else kwargs.get('id')
                
                cache_key = f"{key_prefix}:{func.__name__}:{item_id}"
                
                cached = self.get(cache_key)
                if cached:
                    print(f"Retrieved from cache")
                    return cached
                
                print(f"Retrieved from db")
                result = func(*args, **kwargs)
                
                self.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator
    
    def invalidate_cache(self, pattern: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                
                self.delete_pattern(pattern)
                return result
            return wrapper
        return decorator