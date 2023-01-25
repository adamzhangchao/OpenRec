import os

name = "Electronics"
file_list = []
prefix = "../data"
with open(os.path.join(prefix, "{}_mapped_data.txt".format(name)), "r") as f:
    for line in f.readlines():
        file_list.append(line)
num_users = len(file_list)
split_1 = int(num_users * 0.8)
split_2 = int(num_users * 0.9)
train_list = file_list[:split_1]
valid_list = file_list[split_1:split_2]
test_list = file_list[split_2:]

def export_data(path, data_list):
    with open(path, "w") as f:
        for line in data_list:
            f.write(line)

export_data(os.path.join(prefix, "{}_recall_train.txt".format(name)), train_list)
export_data(os.path.join(prefix, "{}_recall_valid.txt".format(name)), valid_list)
export_data(os.path.join(prefix, "{}_recall_test.txt".format(name)), test_list)
print("train num:{}, valid num:{}, test num:{}".format(len(train_list), len(valid_list), len(test_list)))
