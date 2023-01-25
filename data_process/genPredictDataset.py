import pickle

name = "Electronics"
path = "../data/{}_recall_predict_res.txt".format(name)

records = []
with open(path, "r") as f:
    for line in f.readlines():
        struct = line.split(",")
        reviewerID = int(struct[0])
        hist = [int(val) for val in struct[1].split(";") if int(val) != 0]
        candidates = [int(val) for val in struct[2].split(";")]
        target = [int(val) for val in struct[3].split(";")]
        for cand_item in candidates:
            records.append([reviewerID, hist, [cand_item, 0]])
            
cate_list = []
with open("../data/{}_item_cate_kv.txt".format(name), "r") as f:
    for line in f.readlines():
        struct = line.split(",")
        cate_list.append(int(struct[1]))

with open("../data/{}_rank_from_recall_predict_data.pkl".format(name), "wb") as f:
    pickle.dump(records, f, pickle.HIGHEST_PROTOCOL)
    pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)
