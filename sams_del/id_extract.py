import json
f = open("/home/msl/ys/cute/data/sams2/clean/dup_number12.json")
data = json.load(f)
for d in data["data"]:
    for p in d["paragraphs"]:
        for q in p["qas"]:
            q_id = q["id"]
            print (q_id)
f.close()
