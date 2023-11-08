def add_info_into_obj(obj, data): 
    for key in data: 
        if hasattr(obj, key): 
            setattr(obj, key, data.get(key)) 
    return obj