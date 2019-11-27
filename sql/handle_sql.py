import pymysql
from sql.Handle_Sql_Conf import *
from common.Tools import *
from module.user import user

class Handle_Sql:

    def __init__(self):
        # 连接数据库
        self.db = self.connect_database()
        # 创建游标
        self.cur = self.db.cursor()

    # 连接数据库
    def connect_database(self):

        return pymysql.connect(host=HOST,
                             port=PORT,
                             user=USER,
                             password=PASSWORD,
                             database=DATABASE,
                             charset=CHARSET
                             )

    def check(self,obj):
        """

        :param obj: 需要操作数据库的对象
        :return:boolean(查看数据库是否匹配该对象)
        """
        table_name = get_table_name(obj)
        colunm_name, colunm_lis, res_value = get_colunm(obj)
        sql = "select 1 from "
        sql += table_name
        for i in range(len(colunm_lis)):
            if i == 0:
                sql += " where " + colunm_name[0] + " = "
            else:
                sql += " and " + colunm_name[i] + " = "
            if res_value[i] == "%s":
                sql += "'" + colunm_lis[i] + "'"
            else:
                sql += colunm_lis[i]
        print(sql)
        return self.cur.execute(sql)



    # 新增数据
    def insert_one(self,obj):
        """

        :param obj: 需要操作数据库的对象
        :return: none(插入一条数据)
        """
        if not obj:
            return
        try:
            table_name = get_table_name(obj)
            colunm_name,colunm_val,res_value = get_colunm(obj)
            sql = "insert into "
            sql += table_name
            sql += "("+",".join(colunm_name)+")"
            sql += "values"
            sql += "("+",".join(res_value)+")"
            print(sql)
            self.cur.execute(sql, colunm_val)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            print(e)



    def close(self):
        # 关闭游标/数据库
        self.cur.close()
        self.db.close()
