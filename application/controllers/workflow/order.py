"""
CREATING ORDER WORKFLOW

1. CUSTOMER want to ORDER    
2. Manager (USER) create an ORDER
3. Add PRODUCT to ORDERDETAILS
4. Create a DELIVERY record, with state 0 (received order)
5. Packing, change DELIVERY record's state to 1
6. Subtracting inventory in STORE
7. Start delivering, change DELIVERY record's state to 2
8. Arrived, change DELIVERY record's state to 3.
If customer not receive the package still change DELIVERY record's state to 3
9. Change ORDER delivery_status to 1. If customer not receive the package delivery_status is 2

"""