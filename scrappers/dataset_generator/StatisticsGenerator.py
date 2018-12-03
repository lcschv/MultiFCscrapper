from scrappers.ClaimSchema import *
import ast
def get_claim_objects(schemas_filepath="data/claims_schema_separator_tab"):
    dict_claim_objects = {}
    with open(schemas_filepath, encoding="utf8") as f:
        content = f.readlines()
    content = [x.rstrip() for x in content]
    for line in content[1:]:
        claim_schema = ClaimSchema(line)
        parts = line.split("\t")
        seed = parts[0].split("-")[0]
        if seed not in dict_claim_objects:
            dict_claim_objects[seed] = []
        dict_claim_objects[seed] += [claim_schema]

    return dict_claim_objects

def summarize_statistics(dict_objects, seed, dict_summary):
    keys = list(vars(dict_objects[0]).keys())
    dict_summary[seed] = {}
    for key in keys:
        dict_summary[seed][key] = {"collected":0, "missed":0}
    for object in dict_objects:
        attrs = vars(object)
        for key, value in attrs.items():
            if value == "None":
                dict_summary[seed][key]["missed"] +=1
            elif value == "":
                print(key, "HUE")
            else:
                dict_summary[seed][key]["collected"] += 1


def print_stats(dict_summary):
    for seed, keys in dict_summary.items():
        for key, stats in keys.items():
            # print(seed,key, stats)
            if stats["collected"] == 0:
               dict_summary[seed][key] = {"collected":"-", "missed":"-"}


    with open("stats_summary.txt", "w") as file_out:
        for seed, keys in dict_summary.items():
            print(seed+" "+' '.join("{} {}".format(item[1]["collected"], item[1]["missed"]) for item in keys.items()), file=file_out)
        # for key, stats in keys.items():
        #     print (key, stats)

    # for id, object in dict_objects.items():
    #     attrs = vars(object)
    #     for key, value in attrs.items():
    #         if value is None:
    #             dict_summary[key]["missed"] +=1
    #         else:
    #             dict_summary[key]["collected"] += 1
    # print('\t'.join("%s" % item[1]["missed"] for item in dict_summary.items()))
    # with open(file_out ,"w") as f:
    #     f.write("Information " +"\t " +'\t'.join("%s" % item[0] for item in dict_summary.items()) + "\n")
    #     f.write("Total" + "\t" + '\t'.join
    #         ("%s" % str(item[1]["missed" ]+ item[1]["collected"]) for item in dict_summary.items() ) +"\n")
    #     f.write("Collected " +"\t " +'\t'.join("%s" % item[1]["collected"] for item in dict_summary.items() ) +"\n")
    #     f.write("Missed " +"\t " +'\t'.join("%s" % item[1]["missed"] for item in dict_summary.items()))


def fix_hoaxslayer_theguardian():
    files = ["C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\schemastestCopy\\verafiles.txt",
             "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\schemastestCopy\crikey.txt",
             "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\schemastestCopy\\boomlive.txt",
             "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\schemastestCopy\politifact_story.txt"]
    for file in files:
        with open(file, encoding="utf8") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        with open(file, "w", encoding="utf8") as fout:
            fout.write(content[0] + "\n")
            for line in content[1:]:
                parts = line.split("\t")
                if parts[7] == "":
                    parts[7] = "None"
                if parts[4] == "":
                    parts[4] = "None"
                fout.write("\t".join(parts)+"\n")

def main():
    # fix_hoaxslayer_theguardian()
    dict_summary = {}
    dict_claims_objects = get_claim_objects()
    # print(len(dict_claims_objects))
    for seed, objects in dict_claims_objects.items():
        # print(seed, objects)
        summarize_statistics(objects, seed, dict_summary)
    print_stats(dict_summary)

    # for seed, valores in dict_summary.items():
    #     for val in list(valores.values()):
    #         print(val)
        # print(seed, "\t".join(list(valores.values())))
        # print(seed, "\t".join(list(valores.values())))
        # for key, value in values.items():
        #     print(key, value)

if __name__ == '__main__':
    main()