import mysql.connector as my

connection = my.connect(host='localhost', user='root', password='1234')
cursor = connection.cursor(buffered=True)

cursor.execute("SHOW DATABASES;")

cursor.execute("SHOW DATABASES;")
if ('mke',) not in cursor: 
    print("->Database mke not found, creating new database")
    command = "Create database Mke"
    cursor.execute(command)
    print("->New database (mke) created")
else:
    print("->Database found")

cursor.execute("use mke")
cursor.execute("SHOW TABLES;")

cursor.execute("SHOW TABLES;")
if ('inventory',) not in cursor:
    print("->Table not found, creating new table")
    command = "CREATE TABLE INVENTORY (\
        ITEM_NAME VARCHAR(100) PRIMARY KEY,\
        PRICE FLOAT(5,2),\
        CATEGORY VARCHAR(50))"
    print("->New Table (inventory) created")
    cursor.execute(command)
else:
    print("->Table found")


def add_item(item_name, price, category):
    return_data = {'success': False,'rowcount':0, 'data':{}, 'remark':'', 'code':0}
    try:
        command = "INSERT INTO INVENTORY VALUES(%s, %s, %s)"
        val = (item_name, price, category)
        cursor.execute(command, val)
        connection.commit()
        return_data['success'] = True
        return_data['remark'] = "Item added"
        return_data['code'] = 200
    
    except my.errors.IntegrityError:
        return_data['remark'] = f"Item with name \"{item_name}\" already exists in database"
        return_data['code'] = 409
    except Exception as e:
        return_data['remark'] = e
        return_data['code'] = 500
    
    return return_data

def item_info_byname(item_name):
    return_data = {'success': False,'rowcount':0, 'data':{}, 'code' : 0}
    if item_name == "all":
        command = "SELECT * FROM INVENTORY"
        cursor.execute(command)
        if cursor.rowcount != 0:
            return_data['success'],return_data['rowcount'],return_data['remark'],return_data['code'] = True, cursor.rowcount,'Data found',200
            for info in cursor:
                if info[2] not in return_data['data'].keys():
                    return_data['data'][info[2]] = {}
                return_data['data'][info[2]][info[0]]=info[1]
        else:
            return_data['remark'] = 'No item in database'
            return_data['code'] = 204
    
    else:
        command = "SELECT * FROM INVENTORY WHERE ITEM_NAME = %s"
        val = (item_name,)
        cursor.execute(command, val)
        if cursor.rowcount != 0:
            return_data['success'],return_data['rowcount'],return_data['remark'],return_data['code'] = True, cursor.rowcount, "Item found",200
            for info in cursor:
                if info[2] not in return_data['data'].keys():
                    return_data['data'][info[2]] = {}
                return_data['data'][info[2]][info[0]]=info[1]
        else:
            return_data['remark'] = f'{item_name} not found in database'
            return_data['code'] = 204
    
    return return_data

def item_info_bycategory(item_category):
    return_data = {'success': False,'rowcount':0, 'data':{}, 'code':0}
    command = "SELECT * FROM INVENTORY WHERE CATEGORY = %s"
    val = (item_category,)
    cursor.execute(command, val)
    if cursor.rowcount != 0:
        return_data['success'],return_data['rowcount'],return_data['remark'],return_data['code'] = True, cursor.rowcount, f"{item_category} category found",200
        for info in cursor:
            if info[2] not in return_data['data'].keys():
                return_data['data'][info[2]] = {}
            return_data['data'][info[2]][info[0]]=info[1]
    else:
        return_data['remark'] = f'{item_category} category not found in database'
        return_data['code'] = 204
    
    return return_data

def modify_item_price(item_name, price):
    return_data = {'success': False,'rowcount':0, 'data':{}, 'remark': '', 'code':0}
    try:
        command = f"UPDATE INVENTORY SET PRICE = {price} WHERE ITEM_NAME = '{item_name}'"
        cursor.execute(command)
        connection.commit()
        return_data['remark'] = 'Item modified'
        return_data['success'] = True
        return_data['code'] = 200

    except my.errors.ProgrammingError as e:
        return_data['remark'] = f"{item_name} not found in database"
        return_data['code'] = 204
    
    except Exception as e:
        return_data['remark'] = e
        return_data['code'] = 500

    return return_data

def modify_item_category(item_name, category):
    return_data = {'success': False,'rowcount':0, 'data':{}, 'remark': ''}
    try:
        command = f"UPDATE INVENTORY SET CATEGORY = '{category}' WHERE ITEM_NAME = '{item_name}'"
        cursor.execute(command)
        connection.commit()
        return_data['remark'] = 'Item modified'
        return_data['success'] = True
        return_data['code'] = 200

    except my.errors.ProgrammingError:
        return_data['remark'] = f"{item_name} not found in database"
        return_data['code'] = 204
    
    except Exception as e:
        return_data['remark'] = e
        return_data['code'] = 500
    return return_data

