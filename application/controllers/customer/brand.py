from ...models.customer.customer import *
from application.extensions import apimanager

apimanager.create_api(model=Brand, collection_name="brands") 

