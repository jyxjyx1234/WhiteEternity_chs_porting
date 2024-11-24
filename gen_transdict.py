from Lib import *

chs_file = "snow_chs.txt"
ori_file = "snow.txt"

chs_file = open(chs_file, "r", encoding="936").read().split("\n")
ori_file = open(ori_file, "r", encoding="932").read().split("\n")
transdict = {}
cache = None

for i in range(len(chs_file)):
    if re.match(r"@.*pushstring .*", chs_file[i]):
        chs = re.match(r"@.*pushstring (.*)", chs_file[i]).group(1)
        ori = re.match(r"@.*pushstring (.*)", ori_file[i]).group(1)
        if re.match("[a-zA-Z_]", ori):
            continue
        #if ori in transdict and transdict[ori] != chs:
        #    print(f"{ori} has different translations: {transdict[ori]} and {chs}")
        if chs.encode("936") != ori.encode("932"):
            transdict[ori] = chs
save_json("transdict.json", transdict)