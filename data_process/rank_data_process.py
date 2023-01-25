import os
import random
import pickle

random.seed(1234)
name = "Electronics"
prefix = "../data"

def load_map(path):
    kv_dict = {}
    line_num = 0
    with open(path, "r") as f:
        for line in f.readlines():
            line_num += 1
            struct = line.strip().rsplit(",", 1)
            if struct[0] in kv_dict:
                print(line)
            kv_dict[struct[0]] = struct[1]
    return kv_dict

cate_map = load_map(os.path.join(prefix, "{}_cate_kv.txt".format(name)))
item_map = load_map(os.path.join(prefix, "{}_item_kv.txt".format(name)))
user_map = load_map(os.path.join(prefix, "{}_user_kv.txt".format(name)))
item_count = len(item_map) + 1
cate_count = len(cate_map) + 1
user_count = len(user_map) + 1

cate_list = []
with open(os.path.join(prefix, "{}_item_cate_kv.txt".format(name)), "r") as f:
    for line in f.readlines():
        struct = line.split(",")
        cate_list.append(int(struct[1]))

print("item_count:{},cate_count:{},user_count:{},cate_list_len:{}".format(item_count, cate_count, user_count, len(cate_list))) 

train_set = []
valid_set = []
test_set = []
user_count = 0
with open(os.path.join(prefix, "{}_mapped_data.txt".format(name)), "r") as f:
    for line in f.readlines():
        user_count += 1
        record = line.strip().split(",")
        reviewerID = int(record[0])
        pos_list = [int(item_id) for item_id in record[1].split(";")]
        def gen_neg():
            neg = pos_list[0]
            while neg in pos_list:
                neg = random.randint(0, item_count-1)
            return neg
        neg_list = [gen_neg() for i in range(len(pos_list))]

        for i in range(1, len(pos_list)):
            hist = pos_list[:i]
            if i < len(pos_list) - 2:
                train_set.append((reviewerID, hist, pos_list[i], 1))
                train_set.append((reviewerID, hist, neg_list[i], 0))
            elif i == len(pos_list) - 2:
                label = (pos_list[i], neg_list[i])
                valid_set.append((reviewerID, hist, label))
            else:
                label = (pos_list[i], neg_list[i])
                test_set.append((reviewerID, hist, label))

random.shuffle(train_set)
random.shuffle(valid_set)
random.shuffle(test_set)

assert len(test_set) == user_count
# assert(len(test_set) + len(train_set) // 2 == reviews_df.shape[0])

with open(os.path.join(prefix, '{}_rank_dataset.pkl'.format(name)), 'wb') as f:
  pickle.dump(train_set, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(valid_set, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(test_set, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump((user_count, item_count, cate_count), f, pickle.HIGHEST_PROTOCOL)
