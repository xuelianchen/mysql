import random
import time
import os



csv_path = ".\csvFiles\\"
if not os.path.exists(csv_path):
    os.makedirs(csv_path)
ages = [i for i in range(18,58)]
genders = [1,2]
start_time = time.time()

# 文件数量
for i in range (1,1001):
    csv_name = "file{}.csv".format(i)
    with open(csv_path + csv_name ,"w") as f :
        title = "{},{},{},{},{}\n".format("id","name","age","gender","updated")
        f.write(title)
        # 文件中的行数
        for j in range(1,101):
            id = j 
            name = "name{}".format(j)
            age = ages[random.randint(0,39)]
            gender = genders[random.randint(0,1)]
            # updated = time.time()
            updated = time.strftime("%Y-%m-%d %H:%M:%S.000")
            body = "{},{},{},{},{}\n".format(id,name,age,gender,updated)
            f.write(body)

end_time = time.time()
print("all spent: " ,end_time - start_time)
