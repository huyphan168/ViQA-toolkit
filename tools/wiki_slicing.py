import json
import argparse
from tools.wiki_utils import preprocess_slicing

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, default="datasets/wikipedia.jsonl")
    parser.add_argument("--output-path", type=str, default="datasets/wikicorpus/wiki.jsonl")
    parser.add_argument("--test-mode", type=bool, default=False)
    return parser.parse_args()

def main():
    args = parse_arguments()
    data_path = args.data_path
    with open(args.output_path, "w") as g:
        # control variable to produce small length sliced corpus, in purpose of examining the results
        # control = 0 
        with open(data_path) as f:
            id = 0
            for line in f:
                # control += 1
                # if(control > 10):
                #     break
                # Parse document
                doc = json.loads(line)
                if "định hướng" in doc['title']:
                    continue
                doc['text'] = preprocess_slicing(doc['text'])
                lstpos = 0
                cnt = 0
                for pos, c in enumerate(doc['text']):
                  if c == "#":
                    cnt += 1
                    if cnt > 2:
                        temp = {
                            "id": str(id),
                            "title": doc['title'],
                            "text": doc['title'] + " " + doc["text"][lstpos:pos].replace("#", " ")
                        }
                        json.dump(temp, g, ensure_ascii=False)
                        g.write("\n")
                        id += 1
                        cnt = 0
                        lstpos = pos + 1
                    else:
                        # c = ''
                        pass
                if id % 100000 == 0:
                    print("Created {} documents".format(id+1))
                temp = {
                    "id": str(id),
                    "title": doc['title'],
                    "text": doc["text"][lstpos:]
                }
                json.dump(temp, g, ensure_ascii=False)
                g.write("\n")
                id += 1
                # print(id)
            print("Genrated {} docuements".format(id+1))              
if __name__ == "__main__":
    main()