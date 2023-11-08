import sqlalchemy 
def test(): 
    #********** SQL to Python: one to one **********
    type_sql2py_dict = {}
    # print(dir(sqlalchemy.types.__dict__['__all__']))
    # print("=======", sqlalchemy.types.__dict__)
    print("=====", getattr(sqlalchemy.types, 'VARCHAR'))
    string = getattr(sqlalchemy.types, 'VARCHAR')
    sql_type = string()
    print(sql_type.python_type)
    
    
    
    for key in sqlalchemy.types.__dict__:
        # print("===== KEY", key)
        sqltype = getattr(sqlalchemy.types, key)
        if 'python_type' in dir(sqltype):
        # if 'python_type' in dir(sqltype) and not sqltype.__class__.__name__.startswith('type'):
            # print("====== sqltype", sqltype().python_type, type(sqltype))
            
            try:
                typeinst = sqltype()
            except TypeError as e: #List/array wants inner-type
                # print("None type", sqltype)
                typeinst = sqltype(None)

            try:
                type_sql2py_dict[sqltype] = typeinst.python_type
            except NotImplementedError:
                pass
        # print("OUT OF IF CLAUSE")
    # print(" ====== type_sql2py", type_sql2py_dict)
    return type_sql2py_dict

def type_sql2py(): 
    pass