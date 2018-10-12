import os
import numpy as np
import re
class SchemaGenerator(object):
    def __init__(self):
        self.self = self
        # self.fix_abc()
        self.read_all_schemas()
    def get_listoffiles(self, schema_path="seeds/schemas/"):
        onlyfiles = [os.path.join(schema_path, f) for f in os.listdir(schema_path)]
        return onlyfiles

    def read_all_schemas(self):
        i = 1
        with open("claims_schema_tab_nocleaning","w", encoding="utf8") as f2:
            f2.write("ClaimID\tClaim\tLabel\tClaimURL\tReason\tCategories\tSpeaker\tChecker\tTags\tArticleTitle\tPublishDate\tClaimDate\n")
            # f2.write("ClaimID<<::>>Claim<<::>>Label<<::>>ClaimURL<<::>>Reason<<::>>Categories<<::>>Speaker<<::>>Checker<<::>>Tags<<::>>ArticleTitle<<::>>PublishDate<<::>>ClaimDate\n")
            for file in self.get_listoffiles():
                with open(file, encoding="utf8") as f:
                    content = f.readlines()
                content = [x.rstrip() for x in content]
                a = np.zeros(12, int)
                # print(a)
                for line in content[1:]:
                    parts = line.split("   ")
                    if parts[1] != "None":
                        parts[1] = parts[1].replace("											See Example( s )","")
                        # parts[1] = parts[1].replace("											See Example( s )","").replace("“","").replace("”","").replace("'","").replace("’","").replace("\"","")
                        # print(parts[1])
                        if "											See Example( s )" in parts[1]:
                            print ("AHSEUHSAUESA")
                        f2.write(str(i)+"\t"+re.sub(' +',' ',"\t".join(parts[1:]))+"\n")
                        # f2.write(str(i)+"<<::>>"+re.sub(' +',' ',"<<::>>".join(parts[1:]))+"\n")
                        # print(i, "\t".join(parts[1:]))
                        i+=1

if __name__ == '__main__':
    schemagenerator = SchemaGenerator()


