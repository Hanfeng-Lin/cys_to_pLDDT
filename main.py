import pandas as pd
import os


df = pd.read_csv("test.csv")
cys_id = df.iloc[:, 1].tolist()
cys_dict = {}
for item in cys_id:
    key, value = item.split("_C")
    if key in cys_dict:
        cys_dict[key].append(int(value))
    else:
        cys_dict[key] = [int(value)]

print(cys_dict)

pdb_dir = "./af2pdb/"
pdb_files = []
for filename in os.listdir(pdb_dir):
    if filename.endswith(".pdb"):
        pdb_files.append(os.path.join(pdb_dir, filename))

print(pdb_files)

cys_pLDDT_dict = {}
for key in cys_dict:
    for pdb in pdb_files:
        if key in pdb:
            cys_list = cys_dict[key]
            with open(pdb, "r") as f:
                for line in f:
                    if line.startswith("ATOM"):
                        resi = int(line[22:26])
                        if resi in cys_list:
                            if line[17:20] == "CYS":
                                bfactor = float(line[60:66])
                                cys_pLDDT_dict[key+"_C"+str(resi)] = bfactor

print(cys_pLDDT_dict)

output_df = pd.DataFrame.from_dict(cys_pLDDT_dict, orient="index", columns=["pLDDT"])
output_df = output_df.reset_index().rename(columns={"index": "cys_ID"})
output_df.to_csv("output.csv", index=False)
