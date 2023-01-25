name = "Electronics"
recall_predict_path = "../data/{}_recall_predict_res.txt".format(name)

recall_dict = {}
with open(recall_predict_path, "r") as f:
    for line in f.readlines():
        struct = line.split(",")
        reviewerID = int(struct[0])
        hist = [int(val) for val in struct[1].split(";") if int(val) != 0]
        candidates = [int(val) for val in struct[2].split(";")]
        target = [int(val) for val in struct[3].split(";")]
        recall_dict[reviewerID] = [candidates, target]

rank_dict = {}
rank_predict_path = "../data/{}_rank_from_recall_predict_res.txt".format(name)
with open(rank_predict_path, "r") as f:
    for line in f.readlines():
        struct = line.split(";")
        reviewerID = int(struct[0])
        candidate = int(struct[1])
        score = int(struct[2])
        if reviewerID not in rank_dict:
            rank_dict[reviewerID] = []
        rank_dict[reviewerID].append([candidate, score])

all_hitrate = 0
for key, value in recall_dict.items():`
    struct = recall_dict[key]
    candidates = struct[0]
    target_list = struct[1]
    candidate_list = rank_dict[key]
    candidate_list.sort(key=lambda candidate_list:candidate_list[1], reverse=True)
    candidate_list_topk = [val[0] for val in candidate_list[:50]]
    candidate_list_topk = [val for val in candidates[:50]]

    for item_id in target_list:
        if item_id in candidate_list_topk:
            all_hitrate += 1
            break

print(all_hitrate)
print(len(rank_dict))
