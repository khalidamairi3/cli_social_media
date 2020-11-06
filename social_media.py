def logIn(conn,cursor,trial):
    if trial == 3 :
        print("your 3 tries expired")
        return False 
    alias = input("Enter your username: ")
    password = input("Enter your password: ")
    try : 
        cursor.execute("SELECT * FROM hackers WHERE alias = ? ",[alias,])
        user = cursor.fetchone()
    except :
        print("Something went Wrong")
        return False
    if not user :
        print("this user doesn't exist try again")
        return logIn(conn,cursor,trial+1)  
    if password == user[2]:
        hacker = { "id":user[0], "alias" : user[1]}
        print("You logged in succesfully, Welcome "+ user[1])
        return hacker
    elif trial < 3:
        print("the password is wrong try again")
        return logIn(conn,cursor,trial+1)
    else:
        return False
    
def signup(conn,cursor):
    alias = input("Enter your username: ")
    password = input("Enter your password: ")
    try:
        cursor.execute("INSERT INTO hackers (alias,password) VALUES (?,?) ",[alias,password])
        conn.commit()
        print("hacker account is created succesfully")
        print("You can use yyour username and password to login")
    except mariadb.IntegrityError:
        print("this username already exists, try another one")
        signup(conn,cursor)
    except:
        print("unknown error occured")


def addExploit(conn,cursor,userId):
    exploit = input("Enter the content of your exploit: ")

    try:
        cursor.execute("INSERT INTO exploits (content,user_id) VALUES (?,?)",[exploit,userId])
        conn.commit()
        print("your exploit is posted successfully")
    except mariadb.IntegrityError:
        print("this user doesn't exist anymore") 
    except:
        print("unknown error occured")
   

def viewUserExploits(conn,cursor,userId):
    try:
        cursor.execute("SELECT * FROM exploits WHERE user_id = ?",[str(userId),])
        result = cursor.fetchall()
        if len(result)==0:
            print("there is no exploits to show")
        for ex in result : 
            print("exploit: " + str(ex[0]))
            print("content: " +ex[1])
            print("-----------------------------------------------------")
    except:
        print("Somthing Went wrong ")

def viewotherUsersExploits(conn,cursor,userId):
    try:
        cursor.execute("SELECT * FROM exploits e INNER JOIN hackers h ON e.user_id = h.id  WHERE e.user_id!=?",[str(userId),])
        result = cursor.fetchall()
        if len(result)==0:
            print("there is no exploits to show")
        for ex in result : 
            print("username: " + ex[4])
            print("content: " +ex[1])
            print("-----------------------------------------------------")
    except:
        print("Somthing Went wrong ")
def editExploit(conn,cursor,userId):
    viewUserExploits(conn,cursor,userId)
    exploit_id = input("type the exploit number you want to modify: ")
    content = input("Enter new content: ")
    try:
        cursor.execute("UPDATE exploits SET content = ? WHERE id=? AND user_id=?",[content,exploit_id,userId])
        if cursor.rowcount==0:
            print("this exploit doesn't exist in the list")
            return
        conn.commit()
        print("exploit updated successfully")
    except:
        print("Something went Wrong")
def social_media(conn,cursor):
    print("Welcome to cli Social Media")
    print("choose from the following options: ")
    print("1) Login as an existing user ")
    print("2) Sign up ")

    user_choice = input("Enter your choice: ")
    while user_choice not in ["1","2"]:
        print("invalid entry ")
        print("choose from the following options: ")
        print("1) Login as an existing user: ")
        print("2) Sign up ")
        user_choice = input("Enter your choice: ")
    if user_choice =="1":
        user=logIn(conn,cursor,0)
    elif user_choice=="2":
        signup(conn,cursor)
        user=logIn(conn,cursor,0)
    option=0
    while user and option != "5":
        print("Choose from the following options: ")
        print("1)Add a new exploit ")
        print("2)See my exploits") 
        print("3)See others' exploits")
        print("4)Modify one of my exploits")
        print("5)Exit")      
        option=input("Enter you choice: ")
        if option== "1":
            addExploit(conn,cursor,user["id"])
        elif option == "2":
            viewUserExploits(conn,cursor,user["id"])
        elif option == "3":
            viewotherUsersExploits(conn,cursor,user["id"])
        elif option == "4":
            editExploit(conn,cursor,user["id"])
        else:
            print("invalid entry")
        print("-----------------------------------------------------")    

    print("goodbye")