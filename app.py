import threading
from mysql import mysqlPy
import os
import time 


def get_csv_list(csv_file_path):
    # Get csv file list
    csv_file_list = []
    current_path = os.getcwd()
    os.chdir(csv_file_path)
    file_list = os.listdir(os.getcwd())
    print(file_list)
    for file_name in file_list:
        if file_name.endswith('csv') :
            csv_file_list.append(file_name)
    os.chdir(current_path)
    return csv_file_list


def run(csv_file,csv_file_path,mysql_obj,user,password,database):
    print(csv_file," bagin")
    table_name = csv_file.split(".")[0]
    conn,cursor = mysql_obj.conn_mysql(user,password,database)

    with open(csv_file_path + csv_file,"r") as f :
        # 一个文件新建一个表
        file_title = f.readline().split(",")
        title_id = file_title[0]
        title_name = file_title[1]
        title_age = file_title[2]
        title_gender = file_title[3]
        title_updated = file_title[4]            
        sql_create = """create table {}(
            {} int primary key,
            {} char(10),
            {} int,
            {} int,
            {} datetime(3)
            )""".format(table_name,title_id,title_name,title_age,title_gender,title_updated)
        mysql_obj.operate_table(cursor,sql_create)

        while True :
            line = f.readline().split(",")
            if not line or len(line) < 5:
                break
            id = line[0]
            name = line[1]
            age = line[2]
            gender = line[3]
            updated = line[4]
            sql_insert = "insert into {} values({},'{}',{},{},'{}')".format(table_name,id,name,age,gender,updated)
            res = mysql_obj.update_db(conn,cursor,sql_insert)
    # 操作完毕，关闭连接
    mysql_obj.conn_close(cursor,conn)
    print(csv_file," ok")


def main():
    user = "root"
    password = "2436"
    database = "thread"
    csv_file_path = ".\\csvFiles\\"
    mysql_obj = mysqlPy()
    
    csv_list = get_csv_list(csv_file_path)
    print(csv_list)
    thread_list = []
    for csv_file in csv_list:
        t = threading.Thread(target=run,args=(csv_file,csv_file_path,mysql_obj,user,password,database))
        thread_list.append(t)


    for t in thread_list:
        t.setDaemon(True) # 设置为守护线程，不会因主线程结束而中断
        t.start()
        # t.join() 
    for t in thread_list:
        t.join()  # 子线程全部加入，主线程等所有子线程运行完毕


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("all spent: ",end_time - start_time)


# 问题 ： 当有多个thread 同时执行sql 时，会引发错误，一个连接能执行的请求有限 --> 为每一个线程创建一个连接 
# 多个线程要去操作同一个table 时，添加锁
# 线程池 固定最大线程数量
# 装饰器 避免修改已经完成封装的源代码