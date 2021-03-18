import psycopg2
from psycopg2 import Error
#TEST123
def connect():
    """This function is the connection with the postgres db"""

    global connection
    connection = psycopg2.connect(
        host='localhost',
        database='huwebshop1',
        user='postgres',
        password='Martinr43',
        port=1964)
    return connection

def disconnect():
    """This function disconnects the program with the postgres db"""

    con = connect()
    return con.close()

def sql_execute(sql,value):
    """This function executes a query on the Postgres db.
    NOTE: Dont forget you always have to manually use a commit after using this function. This is because you maybe want
    to do multiple executes and commiting it every time will slow the program down."""

    cur = connection.cursor()
    cur.execute(sql,value)
    return

def sql_execute_fetch(sql):
    """This function executes a select query on the Postgres db"""
    cur = connection.cursor()
    cur.execute(sql)
    fetched = cur.fetchall()
    return fetched

def createCollabTable():
    """This function creates a new table for the recommended products based on a collaborative rule.
    If the table already exists, it will be cleared"""

    connection = connect()
    sql_execute("DROP TABLE IF EXISTS most_viewed_products CASCADE; CREATE TABLE most_viewed_products( mv_id VARCHAR(255), product_name VARCHAR (255), views VARCHAR(255), PRIMARY KEY (mv_id));",0)
    connection.commit()
    disconnect()
    return print("Table clear")

def createContentTable1():
    """This function creates a new table for the recommended products based on a content rule.
    If the table already exists, it will be cleared"""

    connection = connect()
    sql_execute("DROP TABLE IF EXISTS target_man CASCADE; CREATE TABLE target_man( product_id VARCHAR(255), product_name VARCHAR (255), target VARCHAR(255),cat VARCHAR(255), PRIMARY KEY (product_id));",0)
    connection.commit()
    disconnect()
    return print("Table MAN clear")

def createContentTable2():
    """This function creates a new table for the recommended products based on a content rule.
    If the table already exists, it will be cleared"""

    connection = connect()
    sql_execute("DROP TABLE IF EXISTS target_woman CASCADE; CREATE TABLE target_woman( product_id VARCHAR(255), product_name VARCHAR (255), target VARCHAR(255),cat VARCHAR(255), PRIMARY KEY (product_id));",0)
    connection.commit()
    disconnect()
    return print("Table WOMAN clear")

def createContentTable4():
    """This function creates a new table for the recommended products based on a content rule.
    If the table already exists, it will be cleared"""

    connection = connect()
    sql_execute("DROP TABLE IF EXISTS target_babys CASCADE; CREATE TABLE target_babys( product_id VARCHAR(255), product_name VARCHAR (255), target VARCHAR(255),cat VARCHAR(255), PRIMARY KEY (product_id));",0)
    connection.commit()
    disconnect()
    return print("Table BABYS clear")

def createContentTable5():
    """This function creates a new table for the recommended products based on a content rule.
    If the table already exists, it will be cleared"""

    connection = connect()
    sql_execute("DROP TABLE IF EXISTS target_adults CASCADE; CREATE TABLE target_adults( product_id VARCHAR(255), product_name VARCHAR (255), target VARCHAR(255),cat VARCHAR(255), PRIMARY KEY (product_id));",0)
    connection.commit()
    disconnect()
    return print("Table ADULTS clear")

def collabInsert():
    """This function, filters the most viewed product in de db. (with a minimum of 5000 views). After that it inmediately
    sends it to the table; most_viewed_products. These products will be the recommended products, based on a collaborative rule"""

    connection = connect()

    #This query counts the number of times a specific product has been viewed
    products = sql_execute_fetch("SELECT prodid, COUNT (prodid) FROM profiles_previously_viewed GROUP BY prodid HAVING COUNT (prodid) > 5000;")

    for i in products:
        #Here the product id and the number of views will be sent to the new table (most_viewed_products)
        sql_execute("INSERT INTO most_viewed_products(mv_id,views) VALUES(%s,%s);",(i[0],i[1]))
    connection.commit()

    #And finally the names are fetched and will be updated in the most_viewed_products table
    names = sql_execute_fetch("SELECT name,id FROM products INNER JOIN most_viewed_products ON products.id = most_viewed_products.mv_id;")
    for name in names:
        sql_execute("UPDATE most_viewed_products SET product_name = %s WHERE mv_id = %s", (name[0], name[1]))
    connection.commit()

    disconnect()

def collabPrint():
    """This function prints out all of the recommended products based of the most viewed products"""

    connection = connect()

    products = sql_execute_fetch("SELECT product_name FROM most_viewed_products")

    print("\nMOST VIEWED PRODUCTS:")
    for i in products:
        print(i[0])

    disconnect()

def contentInsert():
    """This function puts the usable data, for the content recommendations, in different tables"""

    connection = connect()

    products = sql_execute_fetch("SELECT targetaudience,name,id,category FROM products WHERE targetaudience IS NOT NULL")

    for item in products:
        if item[0] == "Vrouwen".capitalize():
            sql_execute("INSERT INTO target_woman(product_id, product_name, target,cat) VALUES(%s,%s,%s,%s);",(item[2], item[1], item[0],item[3]))
        elif item[0] == "Mannen".capitalize():
            sql_execute("INSERT INTO target_man(product_id, product_name, target, cat) VALUES(%s,%s,%s,%s);",(item[2], item[1], item[0],item[3]))
        elif item[0] == "Baby's".capitalize():
            sql_execute("INSERT INTO target_babys(product_id, product_name, target,cat) VALUES(%s,%s,%s,%s);",(item[2], item[1], item[0],item[3]))
        elif item[0] == "Volwassenen".capitalize():
            sql_execute("INSERT INTO target_adults(product_id, product_name, target,cat) VALUES(%s,%s,%s,%s);",(item[2], item[1], item[0],item[3]))

    connection.commit()

    disconnect()

def contentPrint():
    """This function prints out all of the recommended products for every targetaudience"""

    connection = connect()

    woman = sql_execute_fetch("SELECT product_name FROM target_woman BY LIMIT 5;")
    print("\nWOMAN PRODUCTS:")
    for i in woman:
        print(i[0])

    man = sql_execute_fetch("SELECT product_name FROM target_man BY LIMIT 5;")
    print("\nMAN PRODUCTS:")
    for i in man:
        print(i[0])

    adult = sql_execute_fetch("SELECT product_name FROM target_adults BY LIMIT 5;")
    print("\nADULT PRODUCTS:")
    for i in adult:
        print(i[0])

    baby = sql_execute_fetch("SELECT product_name FROM target_babys BY LIMIT 5;")
    print("\nBABY PRODUCTS:")
    for i in baby:
        print(i[0])



#All of the content functions
createContentTable1()
createContentTable2()
createContentTable4()
createContentTable5()
contentInsert()
contentPrint()

#All of the collaborative tables
createCollabTable()
collabInsert()
collabPrint()
