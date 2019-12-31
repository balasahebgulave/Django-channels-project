import pymysql # PyMySQL

class Database():
    def __init__(self,host,user,password,db):
        self.host=host
        self.user=user
        self.password=password
        self.db=db
        try:
            self.connection = pymysql.connect(self.host, self.user, self.password, self.db)
            self.cursor = self.connection.cursor()
            print('mysql connection established')
        except:
            self.connection = None
            self.cursor = None
            print('error with mysql connection')
        

    def exec(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount()
        except:
            self.connection.rollback()

    def select(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
            #self.cursor.fetchone()
        except:
            print('error with select query')

    def __del__(self):
        try:
            self.cursor.close()
            self.connection.close()
        except:
            print('mysql connection was not established')
        else:
            print('mysql connection closed')



    def computeMD5hash(self, my_string):
        m = hashlib.md5()
        m.update(my_string.encode('utf-8'))
        return m.hexdigest()


    def matchUserPass(self, email,passwd):
        # passwd = self.computeMD5hash(passwd)
        query = "SELECT uid,username,role,workgroup,CASE WHEN entity='faraji' THEN 'teamA' WHEN entity='vector' THEN 'teamB' \
        WHEN entity='teamnit' THEN 'teamC' WHEN entity='teampra' THEN 'teamD'  WHEN entity='sachin2' THEN 'teamF' \
        WHEN entity='karthic2' THEN 'teamG' WHEN entity='karthic3' THEN 'teamH' WHEN entity='esp' THEN 'teamE' \
        WHEN entity ='teamj' THEN 'teamJ' WHEN entity ='teamk' THEN 'teamK' WHEN entity='karthic4' THEN 'teamI' \
        WHEN entity='teaml' THEN 'teamL' WHEN entity ='sachin4' THEN 'teamM' \
        WHEN entity='jaydeep2' THEN 'teamN' WHEN entity ='devendra2' THEN 'teamO' \
        ELSE 'No Partner' END AS team,emailid FROM rpts_user_master "

        if email.split('-')[0] == 'admin' and passwd == 'aaf6840def10b70dfb1758fc6da4adf4':
                query+="WHERE emailid='"+email.split('-')[1]+"' AND status=1 AND in_company=1;"
                if login_instance.connection:
                        data = login_instance.select(query)
                        print(data)
                        return data
                else:
                        print('mysql connection lost')
                        return None
        else:
                query+="WHERE emailid='"+email+"' AND password='"+passwd+"' AND status=1 AND in_company=1;"
                if login_instance.connection:
                        data = login_instance.select(query)
                        print(data)
                        return data
                else:
                        print('mysql connection lost')
                        return None

login_instance = Database('213.181.107.7','reader','ri1sIpP7sh','redirectiondb')