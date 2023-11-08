from ...models.customer.transaction import *
from application.extensions import apimanager

apimanager.create_api(model=Order, collection_name="orders")

apimanager.create_api(model=OrderDetail, collection_name="order_details")

apimanager.create_api(model=Delivery, collection_name="deliveries")