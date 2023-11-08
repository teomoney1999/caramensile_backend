from ..models.authentication import Role, User
from . import add_info_into_obj as setobj

def load_roles_data(db): 
    roles = [
        {"name": "admin"}, {"name": "manager"}, 
        {"name": "employee"}, {"name": "customer"}
    ]
    for role in roles: 
        duplicate = Role.query.filter_by(name=role["name"]).first()
        if duplicate: 
            print(f'Role {role} is duplicated. Please choose an another name!')
            continue 
        new = Role()
        new = setobj(new, role) 
        
        db.session.add(new) 
        print(f"Create role {role['name']} successfully!")
    db.session.commit()

def load_users_data(db): 
    role_admin_id = "eaa52529-7ab1-4ca0-b155-9a2dd581d8e5" 
    role_manager_id = "b8f5a59c-1190-45c8-8e2b-223106f7f4bd"
    
    infos = {
        "email": "teomoney1999@gmail.com", 
        "password": "123456abcA"
        # "role_id":
    }
    
    personal_information = {
        "first_name": "Quoc Anh", 
        "last_name": "Truong", 
        "date_birth": 919884359, 
        "gender": 0, 
        "phone": "0394521885", 
        "facebook": "https://www.facebook.com/quocanh.truong.1999/", 
        "zalo": "https://zalo.me/0394521885", 
        "bank_number": "0080114555006", 
        "bank_name": "MB Bank", 
    }
    
    user = User() 
    setobj(user, infos) 
    
    db.session.add(user) 
    db.session.commit()
    print("======= _id", getattr(user, "id"))
    