
def init_controllers(app):
    import application.controllers.auth.users
    import application.controllers.auth.roles
    
    import application.controllers.customer.brand
    import application.controllers.customer.customer
    import application.controllers.customer.order
    
    import application.controllers.store.products
    import application.controllers.store.stores
    
    import application.controllers.warehouse.warehouse
    import application.controllers.warehouse.transaction
    
    @app.route("/") 
    def home(): 
        return "Welcome, Teomoney!!!"
    
    