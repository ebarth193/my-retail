import os


def get_property(env, name):
    props = {
        "local": {
            "REDSKY_URL": os.environ.get('REDSKY_URL'),
            "MONGO_URL": os.environ.get('MONGO_URL'),
            "MONGO_DB_NAME": "my_retail",
            "MONGO_DB_PRICE_TABLE": "itemPrices",
            "MONGO_DB_USER": os.environ.get('MONGO_DB_USER'),
            "MONGO_DB_PASS": os.environ.get('MONGO_DB_PASS'),
        }
    }
    return props.get(env, {}).get(name)
