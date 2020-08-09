import pymysql
from logging.handlers import RotatingFileHandler
import traceback
import logging
import os 

# 只供本模块调用
class logProcessor():
    def log_process(self):
        log_path=os.getcwd() + "\\log.log"
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.DEBUG)
        handler = RotatingFileHandler(log_path, maxBytes=15 * 1024 * 1024, backupCount=1)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


class mysqlPy():
    def __init__(self):
        logger_processor = logProcessor()
        self.logger = logger_processor.log_process()

    # 连接database
    def conn_mysql(self,user,password,database,host="localhost",port=3306):
        conn_flag ,try_time = True,0
        while conn_flag:
            try:
                conn = pymysql.connect(
                    host=host,
                    port=port,
                    user=user,password=password,
                    database=database,
                    charset='utf8')
                # # 通过cursor创建游标
                cursor = conn.cursor() 
                self.logger.info("connect sucessfully!")
                conn_flag = False
                return conn,cursor
            except:
                if try_time == 1:
                    self.logger.error(traceback.format_exc())
                    exit(1)
                try_time += 1
                    

    def conn_close(self,cursor,conn):
        try:
            cursor.close() #关闭游标连接
            conn.close() # 关闭数据库连接
            self.logger.info("close connection sucessfully!")
        except:
            self.logger.error("fatal error occurred while closing the connection. The program exited abnormally")
            self.logger.error(traceback.format_exc())
            exit(1)


    # 包括insert 和 update即写操作  
    def update_db(self,conn,cursor,sql):
        try:
            # 执行
            result = cursor.execute(sql) 
            # 提交
            conn.commit()
            if result == 0:
                self.logger.warning("update failed - 0 rows affected ")
                return False
            row = "row" if result == 1 else "rows"
            message = "update sucessfully! - {} {} affected".format(result,row)
            self.logger.info(message)
            return True
        except Exception :
            self.logger.error("an error occured during doing a writing operation")
            self.logger.error(traceback.format_exc())
            # 错误回滚
            conn.rollback()
            return False


    # 查询 只有读操作
    def select_db(self,cursor,sql):
        try :
            cursor.execute(sql)
            data=cursor.fetchall()
            self.logger.info("finish a query sucessfully! ")
            return data
        except Exception as e:
            self.logger.error("an error occured during doing a query operation")
            self.logger.error(traceback.format_exc())
            return ""


    # 新建表，删除表
    def operate_table(self,cursor,sql):
        try:
            cursor.execute(sql)
            self.logger.info("create a table sucessfully!")
        except Exception as e:
            self.logger.error("an error occured during creating a table")
            self.logger.error(traceback.format_exc())
