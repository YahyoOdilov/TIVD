import psycopg2 as db
from psycopg2._psycopg import connection
import os
from inspect import getfile

class Database:
    '''
    work with database(connect, execute, fetch)
    '''
    __db = "tivd"
    db_user = 'postgres'
    __db_password = 'yo020408'
    db_host = 'localhost'

    @classmethod
    def __connect(self, func, sql, **kvarg):
        with db.connect(database = self.__db, 
                        user = self.db_user, 
                        password = self.__db_password, 
                        host = self.db_host) as conn:
            return func(conn, sql, **kvarg)
        
    @classmethod    
    def execute(self,sql):
        return self.__connect(lambda conn, sql: conn.cursor().execute(sql), sql)
    
    @staticmethod
    def select(conn: connection, sql, all = True):
            cur = conn.cursor()
            cur.execute(sql)
            if all: return cur.fetchall()
            return cur.fetchone()
    
    @classmethod
    def fetchall(self, sql):
        return self.__connect(self.select, sql)
    
    @classmethod
    def fetchone(self,sql):
        return self.__connect(self.select, sql, all = False)
    
# classes for rows 
class Atribute:
    '''
    overal values of rows
    '''
    def __init__(self, null = True, unique = False, primary = False):
        self.unique = unique
        self.null = null
        self.primary = primary
        
    def creation(self):
        sql = f'{self.val}'
        if not self.null: sql += ' NOT NULL'
        if self.unique: sql += ' UNIQUE'
        if self.primary: sql += ' PRIMARY KEY'
        return sql
    
class BigAuto(Atribute):
    '''
    auto filled in row
    '''
    def __init__(self, null = True, unique = False, primary = False):
        super().__init__(null = null, unique= unique, primary = primary)
        self.val = 'BIGSERIAL'

class BigInt(Atribute):
    '''
    big integer row
    '''
    def __init__(self, null = True, unique = False, primary = False):
        super().__init__(null= null, unique= unique, primary= primary)
        self.val = 'BIGINT'
        
class VarChar(Atribute):
    '''
    string row
    '''
    def __init__(self, max_length, null = True, unique = False, primary= False):
        super().__init__(null= null, unique= unique, primary= primary)
        self.max_length = max_length
        self.val = f'VARCHAR({self.max_length})'
 
#  database table class      
class Model(Database):
    '''
    based class for all table which contained tools (create, insert, select)
    '''
    @classmethod
    def find_table(self):
        file = getfile(self)
        file = os.path.basename(file)[:-3]
        name = f'{file.lower()}_{self.__name__.lower()}'
        return name
        
    @classmethod
    def create(self):
        t_name = self.find_table()
        sql = ''
        atrs = self.__dict__
        atr_sql = ''
        for atr, val in atrs.items():
            if val.__class__.__base__ == Atribute:
                    atr_sql += f'{atr} {val.creation()},\n\t'
        sql = f'''CREATE TABLE IF NOT EXISTS {t_name}(
        {atr_sql[:-3]}
        )
        '''     
        return self.execute(sql)
    
    @staticmethod
    def last_item(t_name):
        sql = f'''SELECT * FROM {t_name} OFFSET ((SELECT COUNT(*) FROM {t_name})-1)
        '''
        return sql
                
    @classmethod  
    def insert(self, **kvarg):
        t_name = self.find_table()
        atrs = kvarg
        atr_sql = ''
        val_sql = ''
        for atr, val in atrs.items():
            if val:
                atr_sql += f'{atr},\n'
                if type(val) == str:
                    val = f'\'{val}\''
                val_sql += f'{val},\n'
        atr_sql = atr_sql[:-2]
        val_sql = val_sql[:-2]
        sql = f'''INSERT INTO {t_name}(
        {atr_sql}
        )
        VALUES(
        {val_sql}
        )
        '''
        self.execute(sql)
        return self.fetchone(self.last_item(t_name))
    
    @classmethod
    def select_sql(self, rows, **kvarg):
        t_name = self.find_table()
        rows = ', '.join(rows)
        conditions = ''
        for key, val in kvarg.items(): 
            if type(val) == str:
                val = f'\'{val}\''
            conditions += f'{key} = {val} and '
        if conditions:
            conditions = f'WHERE {conditions[:-4]}'
        sql = f'''SELECT {rows} FROM {t_name}\
        \n {conditions}
        '''
        return sql

    @classmethod
    def filter(self, rows: list = ['*'], **kvarg):
        sql = self.select_sql(rows, **kvarg)
        return self.fetchall(sql)
    
    @classmethod
    def get(self, rows = ['*'], **kvarg):
        sql = self.select_sql(rows, **kvarg)
        return self.fetchone(sql)