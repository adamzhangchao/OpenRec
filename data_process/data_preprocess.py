import os
import sys
import json
import random
from collections import defaultdict

random.seed(1230)

name = "Electronics"
input_file_name = "reviews_{}_5.json".format(name)
meta_file_name = "meta_{}.json".format(name)
prefix = "../data"

filter_size = 5
if len(sys.argv) > 1:
    name = sys.argv[1]
if len(sys.argv) > 2:
    filter_size = int(sys.argv[2])

users = defaultdict(list)
item_count = defaultdict(int)

def read_from_amazon(source):
    with open(source, "r") as f:
        for line in f:
            r = json.loads(line.strip())
            uid = r['reviewerID']
            iid = r['asin']
            item_count[iid] += 1
            ts = float(r['unixReviewTime'])
            users[uid].append((iid, ts))

file_path = os.path.join(prefix, input_file_name)
read_from_amazon(file_path)

items = list(item_count.items())
items.sort(key=lambda x:x[1], reverse=True)


item_total = 0
for index, (iid, num) in enumerate(items): 
    if num >= filter_size:
        item_total = index + 1
    else:
        break

item_map = dict(zip([items[i][0] for i in range(item_total)], list(range(1, item_total+1))))

user_ids = list(users.keys())
filter_user_ids = []
for user in user_ids:
    item_list = users[user]
    index = 0
    for item, timestamp in item_list:
        if item in item_map:
            index += 1
    if index >= filter_size:
        filter_user_ids.append(user)
user_ids = filter_user_ids 

random.shuffle(user_ids)
num_users = len(user_ids)
user_map = dict(zip(user_ids, list(range(1, num_users+1))))

item_cate = {}
cate_map = {}
with open(os.path.join(prefix, meta_file_name), "r") as f:
    for line in f:
        r = eval(line.strip())
        iid = r['asin']
        cates = r['categories']
        if iid not in item_map:
            continue
        cate = cates[0][-1]
        if cate not in cate_map:
            cate_map[cate] = len(cate_map) + 1
        item_cate[item_map[iid]] = cate_map[cate]

sorted_item_cate = {}
sorted_item_cate_key = [0]
sorted_item_cate_value = [0]
for key in range(1, item_total+1):
    sorted_item_cate_key.append(key)
    sorted_item_cate_value.append(item_cate[key])
item_cate = dict(zip(sorted_item_cate_key, sorted_item_cate_value))

def export_map(name, map_dict):
    with open(name, "w") as f:
        for key, value in map_dict.items():
            f.write("{},{}\n".format(key, value))

def export_data(name, user_list):
    with open(name, "w") as f:
        for user in user_list:
            if user not in user_map:
                continue
            item_list = users[user]
            item_list.sort(key=lambda x:x[1])
            item_list_str = ";".join([str(item_map[item[0]]) for item in item_list])
            time_list_str = ";".join([str(int(item[1])) for item in item_list])
            f.write("{},{},{}\n".format(user_map[user], item_list_str, time_list_str))

export_map(os.path.join(prefix, "{}_item_kv.txt".format(name)), item_map)
export_map(os.path.join(prefix, "{}_user_kv.txt".format(name)), user_map)
export_map(os.path.join(prefix, "{}_cate_kv.txt".format(name)), cate_map)
export_map(os.path.join(prefix, "{}_item_cate_kv.txt".format(name)), item_cate)
export_data(os.path.join(prefix, "{}_mapped_data.txt".format(name)), user_ids)

