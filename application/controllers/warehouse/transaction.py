from ...models.warehouse.transaction import *
from application.extensions import apimanager

apimanager.create_api(model=GoodReceipt, collection_name="goodreceipts")

apimanager.create_api(model=GoodReceiptDetail, collection_name="goodreceipt_details")

apimanager.create_api(model=GoodIssued, collection_name="goodissueds")

apimanager.create_api(model=GoodIssuedDetail, collection_name="goodissued_details")