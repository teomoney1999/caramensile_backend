from ...models.customer.customer import *
from application.extensions import apimanager

apimanager.create_api(model=Customer, collection_name="customers")