from ...models.store.transaction import *
from application.extensions import apimanager

apimanager.create_api(model=StoreImported, collection_name="storeimporteds")

apimanager.create_api(model=StoreImportedDetail, collection_name="storeimported_details")