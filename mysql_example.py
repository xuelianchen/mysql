from mysql import mysqlPy



def main():
    user = "root"
    password = "2436"
    database = "test"

    mysql_obj = mysqlPy()
    conn,cursor = mysql_obj.conn_mysql(user,password,database)

    #  需要做的改进 ：用字典存要修改的数据 -->  增删改 格式不统一
    # 增
    sql1 = "insert into {} values({},{},{})".format("grades","'Xiaoming'",99,89,33)
    # # 删
    # sql1 = "delete from {} where name='{}'".format("grades",'Xiaoming')
    # # 改
    # sql1 = "update {} set {}={} where {}".format("grades","English",19,"name='Xiaoming'")

    res = mysql_obj.update_db(conn,cursor,sql1)
    print(res)


    # 新建 table
    # sql2 = "create table file1(name char(15),age int)"
    # 删除 table
    # sql2 = "drop table {}".format("test_py1")
    # mysql_obj.operate_table(cursor,sql2)
    
    # 查
    # sql3 = "select * from {}".format("grades")

    # results = mysql_obj.select_db(cursor,sql3)
    # for result in results:
    #     print(result)

    # 操作完毕，关闭连接
    mysql_obj.conn_close(cursor,conn)




if __name__ == "__main__":
    main()

