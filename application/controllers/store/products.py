from ...models.store.store import *
from application.extensions import apimanager

apimanager.create_api(model=Product, collection_name="products")

apimanager.create_api(model=Store, collection_name="stores")