from ...models.warehouse.warehouse import *
from application.extensions import apimanager

apimanager.create_api(model=Warehouse, collection_name="warehouses") 

apimanager.create_api(model=Ingredient, collection_name="ingredients") 

apimanager.create_api(model=Supplier, collection_name="suppliers") 
