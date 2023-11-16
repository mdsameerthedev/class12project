import mysql.connector as mysql
import _datetime

class DataBase:
    def __init__(self, host, usname, psswd):
        self.host = host
        self.usname = usname
        self.psswd = psswd
        self.conn = mysql.connect(host=self.host, username=self.usname, password=self.psswd)
        self.cursor = self.conn.cursor()
        self.cursor.execute('use chat')

    def is_connected(self):
        if self.conn.is_connected():
            print('Connected Successfully!')
        else:
            print('Connection Unsuccessful!')

    def user_register(self, us1):
        query = 'insert into users (name,username,email,password) values(%s,%s,%s,%s)'
        check = 'select * from users'
        res = self.cursor.execute(check)
        print(res)
        got = self.cursor.fetchall()
        print(got)
        if us1 not in got:
            self.cursor.execute(query, us1)
            self.conn.commit()
            print('Registered Successfully!')
            return True
        else:
            raise 'Registration failed!'
            return False

    def get_user(self, username):
        query = 'select * from users where username = %s'
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchall()
        print(user)
        self.conn.commit()
        return user[0][2], user[0][4]

#..............................customer.....................................................................
class customers:
    def __init__(self):
        self.con=mysql.connect(host='localhost',username='root',password='root@123',database='my_hotel')
        #whenever the program executed created IF NOT EXISTS. So if the table exists it will show the db table.
        query='CREATE TABLE if not exists customer(name varchar(20),aadhar int(10) primary key,age int(2),phone_number int,room_no int(3),checkin varchar(20) )'
        #creating cursor. This will execute queries.
        self.cur=self.con.cursor()
        self.cur.execute(query)
        #print("Table created successfully")
        self.cur.execute("commit")
    
    #insert
    def add_customer(self):
        while True:
            n=input("Do you want to add customer information(y/n):")
            if n in ('Y','y'):
                name=input("enter the name:")
                aadhar_no=int(input("enter the aadhar no :"))
                age=int(input("enter the age: "))
                phone_number=input("enter the phone number:")
                room_no= int(input("enter the room no:"))
                print("TO GET CHECK IN DATE")
                a= input("enter the year:")
                b= input("enter the month:")
                c=input("enter the date :")
                checkin = a+"/"+b+"/"+c
                query="INSERT INTO customer VALUES('{}',{},{},{},{},'{}')".format(name,aadhar_no,age,phone_number,room_no,checkin)
                cur=self.con.cursor()
                cur.execute(query)        
                self.con.commit()
                print('customer information is added')
            elif n in ('N','n'):
                break
            else:
                print("invalid code")

    #Fetch ALL
    def show_all(self):
        query='SELECT * FROM customer'
        cur=self.con.cursor()
        cur.execute(query)
        print("customer details available:")
        for row in cur:
            print(row)
            print()

    def search_by_aadhar(self):
        aadhar=int(input("enter the aadhar to search "))
        query='SELECT * FROM customer WHERE aadhar={}'.format(aadhar)
        cur=self.con.cursor()
        cur.execute(query)
        for row in  cur:  
            print('name',row[0])
            print('age:',row[2])
            print('phone_number:',row[3])
    #Update
    def update_customer(self):
        name=input("enter the  customer name:")
        room_no=int(input("enter the room number to be changed: "))
        query="UPDATE customer set room_no='{}' WHERE name='{}'".format(room_no,name)
        cur=self.con.cursor()
        cur.execute(query)
        #Commit means it will Update the record in database physically or really.
        self.con.commit()
        print('the customer room no is updated')
        
    #delete
    def delete_cust(self):
        cust_name=input("enter the customer name to delete details:")
        query="DELETE FROM customer WHERE name='{}'".format(cust_name)
        cur=self.con.cursor()
        cur.execute(query)
        #Commit means it will delete the record in database physically or really.
        self.con.commit()
        print("customer detail is sucessfully deleted.")
        





#..................................employees....................................................................        
class employees:
    def __init__(self):
        self.con=mysql.connect(host='localhost',username='root',password='Root@123',database='my_hotel')
        #whenever the program executed created IF NOT EXISTS. So if the table exists it will show the db table.
        query='CREATE TABLE if not exists employees_info(empl_id int(4),name varchar(20),age int(2),designation varchar(10),phoneno int(10),salary int(5))'
        cur=self.con.cursor()
        cur.execute(query)
        print("Table created successfully")
        cur.execute("commit")
        
    #insert
    def add_employee(self):
        while True:
            n=input("Do you want to add employee_detail(y/n):")
            if n in ('Y','y'):
                empl_id=int(input("enter the empoyee id:"))
                name=input("enter the empyoee name:")
                age=int(input("enter the employee's age: "))
                designation=input("enter the designation:")
                phoneno= int(input("enter employee phone no:"))
                salary= int(input("enter employee salary:"))
                query="INSERT INTO employees_info VALUES({},'{}',{},'{}',{},{})".format(empl_id,name,age,designation,phoneno,salary)
                cur = self.con.cursor()
                cur.execute(query)        
                self.con.commit()
                print('employee details is added')
            elif n in ('N','n'):
                break
            else:
                print("invalid code")
        
    #update
    def update_employee(self):
        empl_id=int(input("enter the employee id:"))
        salary=int(input("enter the employee's salary to be updated: "))
        query="UPDATE employees_info set salary='{}' WHERE empl_id={}".format(salary,empl_id)
        cur=self.con.cursor()
        cur.execute(query)
        #Commit means it will Update the record in database physically or really.
        self.con.commit()
        print('the employee salary is updated')
        
    #fetchall
    def showall_employee(self):
        query='SELECT * FROM employees_info'
        cur = self.con.cursor()
        cur.execute(query)
        print("the employees of our hotel are :")
        for row in  cur:
            print(row)
            print()
            
    #fetchone
    def search_empl(self):
        empid=int(input("enter the employee's id: "))
        query='SELECT * FROM employees_info WHERE empl_id={}'.format(empid)
        cur=self.con.cursor()
        cur.execute(query)
        for row in  cur:  
            print('employee Id:',row[0])
            print('employee Name:',row[1])
            print('phone no:',row[4])
            
    #delete
    def delete_empl(self):
        empl_id=int(input("enter the emlpoyee id to delete details:"))
        query='DELETE FROM employees_info WHERE empl_id={}'.format(empl_id)
        cur=self.con.cursor()
        cur.execute(query)
        #Commit means it will delete the record in database physically or really.
        self.con.commit()
        print("employee is sucessfully deleted.")

#............................food and room...................................................
class food_and_rooms:
    def __init__(self):
        self.con=mysql.connect(host='localhost',username='root',password='root@123',database='my_hotel')
        #whenever the program executed created IF NOT EXISTS. So if the table exists it will show the db table.
        query='CREATE TABLE if not exists food_rooms(customer_name varchar(11),room_no int,foodtype varchar(20),qty int,cost int,room_type varchar(20))'
        #creating cursor. This will execute queries.
        cur=self.con.cursor()
        cur.execute(query)
        #cur.execute(query1)
        #print("Table created successfully")
        cur.execute("commit")
        #show all(input)
    def add_needs(self):
        while True:
            n=input("Do you want to add customer purchases(y/n):")
            if n in ('Y','y'):
                customer_name=input("enter the customer name :")
                room_no= int(input("enter the room_no:"))
                foodtype=input("enter the food type(veg/non-veg): ")
                qty=int(input("enter the qty:"))
                cost= int(input("enter cost of the food:"))
                room_type=input("enter the type of the room(simple/deluxe/super_deluxe):")
                query="INSERT INTO food_rooms VALUES('{}',{},'{}',{},{},'{}')".format(customer_name,room_no,foodtype,qty,cost,room_type)
                cur = self.con.cursor()
                cur.execute(query)        
                self.con.commit()
                print('food and room needed by customer is added')
            elif n in ('N','n'):
                break
            else:
                print("invalid code")
       
    def show_cust_needs(self):
        custname=input("Enter the customer name to see all his/her purchase:")
        query2="select * from food_rooms where customer_name='{}'" .format(custname)
        cur=self.con.cursor()
        cur.execute(query2)
        for row in cur:
            print(row)

    

#############################main program########################################
print("################################################################################")
print()
print('########################## Friends Hotel ###################################')
print()
print('################################################################################')
print()


employeenew=employees()
customernew=customers()
food_room_new=food_and_rooms()
#Admin sign in
while True:
    print("Press 1 to signin as admin")
    print("Press 2 to signin as employee")
    print("Press 3 to exit")
    login=int(input("enter your choice:"))
    print()
    if login==1:
        print("##### SIGNING IN #####")
        name=input("enter username:")
        password=input("enter password:")
        if name in ('Aravind','Nadeem','Moinudeen') and password in ("hotel"):
            print("***login successfully***")
            while True:
                print()
                print("=====================================")
                print('$$$$$$$$ ADMIN SECTION OPENS $$$$$$$$')
                print("=====================================")
                print("1.EMPLOYEE DETAILS")
                print("2.CUSTOMER DETAILS")
                print("3.FOOD AND ROOM DETAILS")
                print("4.EXIT")
                print()
                login1=int(input("ENTER YOUR CHOICE:"))        
                if login1==1:
                    while True:
                        print("   ===============   ")
                        print('### EMPLOYEE DETAILS ###')
                        print("   ===============   ")
                        print()
                        print("1.ADD EMPLOYEE DETAILS")
                        print("2.SEE EMPLOYEE DETAILS")
                        print("3.SEE ONE EMPLOYEE DETAILS USING EMPLOYEE ID:")
                        print("4.UPDATE EMPLOYEE'S SALARY USING EMPL_ID :")
                        print('5.DELETE EMPLOYEE DETAILS')
                        print('6.EXIT')
                        print()
                        log=int(input("enter your choice:"))
                        if log==1:
                            employeenew.add_employee()
                            #add employee detail program
                        elif log==2:
                            employeenew.showall_employee()
                            #see employee detail program
                        elif log==3:
                            employeenew.search_empl()
                            #employee using phone nocode search
                        elif log==4:
                            employeenew.update_employee()
                            #update code
                        elif log==5:
                            employeenew.delete_empl()
                            # delete program
                        elif log==6:
                            break
                        else:
                            print("Invalid value entered")

                elif login1==2:
                    while True:
                        print("   ================   ")
                        print("###CUSTOMER DETAILS###")
                        print("   ================   ")
                        print()
                        print('1.ADD CUSTOMER DETAILS')
                        print('2.UPDATE CUSTOMER DETAILS')
                        print('3.SEE CUSTOMER DETAILS')
                        print('4.SEE CUSTOMER INFO USING AADHAR NO ')
                        print('5.DELETE CUSTOMER DETAILS USING CUSTOMER NAME')  
                        print('6.EXIT')
                        print()
                        log1=int(input("enter your choice:"))
                        if log1==1:
                            customernew.add_customer()
                            #add customer program
                        elif log1==2:
                            customernew.update_customer()
                            #update customer program
                        elif log1==3:
                            customernew.show_all()
                            #display code
                        elif log1==4:
                            customernew.search_by_aadhar()
                            #search by aadhar code
                        elif log1==5:
                            customernew.delete_cust()
                            #delete code
                        elif log1==6:
                            break
                        else:
                            print("invalid value entered")

                elif login1==3:
                    while True:
                        print("   ================   ")
                        print("###FOOD AND ROOMS DETAILS###")
                        print("   ================   ")
                        print("1.ADD PURCHASE DETAILS")
                        print("2.SEE PURCHASE DETAILS")
                        print('3.EXIT')
                        print()
                        log2=int(input("enter your choice: "))
                        if log2==1:
                            food_room_new.add_needs()
                        elif log2==2:
                            food_room_new.show_cust_needs()
                        elif log2==3:
                            break

                elif login1==4:
                    break
                else:
                    print("invalid value entered")
        else:
            print("invalid user-id or password")

    #empl sign in
    elif login == 2:
        print("##### SIGNING IN AS EMPLOYEE#####")
        name1 = input("enter username:")
        password1 = input("enter password:")
        if name1 in ('Aravind', 'Nadeem', 'Moinudeen') and password1 in ("empl"):
            print("***login successfully***")
            while True:
                    print()
                    print("=====================================")
                    print('$$$$$$$$ EMPLOYEE SECTION OPENS $$$$$$$$')
                    print("=====================================")
                    print("1.CUSTOMER DETAILS")
                    print("2.FOOD AND ROOM DETAILS")
                    print("3.EXIT")
                    print()
                    login2=int(input("ENTER YOUR CHOICE:"))
                    if login2==1:
                        while True:
                            print("   ================   ")
                            print("###CUSTOMER DETAILS###")
                            print("   ================   ")
                            print()
                            print('1.ADD CUSTOMER DETAILS')
                            print('2.UPDATE CUSTOMER DETAILS')
                            print('3.SEE CUSTOMER DETAILS')
                            print('4.SEE CUSTOMER INFO USING AADHAR NO ')
                            print('5.DELETE CUSTOMER DETAILS USING CUSTOMER NAME')
                            print('6.EXIT')
                            print()
                            bog1 = int(input("enter your choice:"))
                            if bog1 == 1:
                                customernew.add_customer()
                                # add customer program
                            elif bog1 == 2:
                                customernew.update_customer()
                                # update customer program
                            elif bog1 == 3:
                                customernew.show_all()
                                # display code
                            elif bog1 == 4:
                                customernew.search_by_aadhar()
                                # search by aadhar code
                            elif bog1 == 5:
                                customernew.delete_cust()
                                # delete code
                            elif bog1 == 6:
                                break
                            else:
                                print("invalid value entered")

                    elif login2 == 2:
                        while True:
                            print("   ================   ")
                            print("###FOOD AND ROOMS DETAILS###")
                            print("   ================   ")
                            print("1.ADD PURCHASE DETAILS")
                            print("2.SEE PURCHASE DETAILS")
                            print('3.EXIT')
                            print()
                            bog2 = int(input("enter your choice: "))
                            if bog2 == 1:
                                food_room_new.add_needs()
                            elif bog2 == 2:
                                food_room_new.show_cust_needs()
                            elif bog2 == 3:
                                break

                    elif login2 == 3:
                        break
                    else:
                        print("invalid value entered")

        else:
            print("invalid user-id or password")
    elif login==3:
        break
    else:
        print("invalid value entered")
        print()
