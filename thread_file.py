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


def run(csv_file,csv_file_path,results):
    print(csv_file," bagin")
    with open(csv_file_path + csv_file,"r") as f :
        csv_title = csv_file.split(".")[0]
        line = f.readline()
        line_title = line.strip().split(",")
        
        id = line_title[0]
        name = line_title[1]
        age = line_title[2]
        gender = line_title[3]
        updated = line_title[4]

        results[csv_title] = {}
        results[csv_title][id] = []
        results[csv_title][name] = []
        results[csv_title][age] = []
        results[csv_title][gender] = []
        results[csv_title][updated] = []
        while True :
            line = f.readline()
            line_body = line.strip().split(",")
            if not line_body or len(line_body) < 5:
                break
            results[csv_title][id].append(line_body[0])
            results[csv_title][name].append(line_body[1])
            results[csv_title][age].append(line_body[2])
            results[csv_title][gender].append(line_body[3])
            results[csv_title][updated].append(line_body[4])
            
    print(csv_file," ok")

def main():
    csv_file_path = ".\\csvFiles\\"
    results = {}
    csv_list = get_csv_list(csv_file_path)
    thread_list = []
    for csv_file in csv_list:
        t = threading.Thread(target=run,args=(csv_file,csv_file_path,results))
        thread_list.append(t)


    for t in thread_list:
        t.setDaemon(True) # 设置为守护线程，不会因主线程结束而中断
        t.start()
        # t.join() 
    for t in thread_list:
        t.join()  # 子线程全部加入，主线程等所有子线程运行完毕

    print(results)


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("all spent: ",end_time - start_time)

# 功能：将csv中的数据存储到字典中

