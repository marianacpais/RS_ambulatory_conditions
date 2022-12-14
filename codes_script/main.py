import pandas as pd
import requests

ds =  pd.read_excel("codes_script/table1_it2.xlsx")

def get_code_description (id,code,code_sys,cm_bool=True):
    if cm_bool:
        code_sys = code_sys + "CM"
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/current/source/'+code_sys+'/' + code + '?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    try:
        x = requests.get(url).json()
        print(str(id),": Got description for " + code_sys +" code '"+code+"'")
        return x["result"]["name"]
    except:
        return "ERROR"

# get_code_description ("B18","ICD10CM")

def get_umls_cui (code,code_sys,cm_bool=True):
    if cm_bool:
        code_sys = code_sys + "CM"
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/current/source/'+code_sys+'/' + code + '?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        atom = x["result"]["concepts"]
    except:
        print("ERROR - atom for " + code_sys +" code '"+code+"'")
        return "ERROR - atom"
    url = atom + '&apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        if x['result']['recCount'] == 1:
            print("WARNING: code may not be 'MTH'")
            print("Got UMLS CUI for " + code_sys +" code '"+code+"'")
            return x['result']['results'][0]['ui']
        else:
            for result in x['result']['results']:
                if result["rootSource"] == "MTH":
                    print("Got UMLS CUI for " + code_sys +" code '"+code+"'")
                    return result["ui"]
    except:
        print("ERROR - concept for " + code_sys +" code '"+code+"'")
        return "ERROR - concept"

# get_umls_cui ("J13","ICD10CM")

def get_parents_ui (id,code,code_sys,cm_bool=True):
    if cm_bool:
        code_sys = code_sys + "CM"
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/2022AB/source/'+code_sys+'/' + code + '/parents?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    try:
        x = requests.get(url).json()
        print(str(id)+": Got parent ui for " + code_sys +" code '"+code+"'")
        return x["result"][0]["ui"]
    except:
        return "ERROR"

# get_parents_ui (1,"J13","ICD10")

def get_parents_name (id,code,code_sys,cm_bool=True):
    if cm_bool:
        code_sys = code_sys + "CM"
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/2022AB/source/'+code_sys+'/' + code + '/parents?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    try:
        x = requests.get(url).json()
        print(str(id)+": Got parent name for " + code_sys +" code '"+code+"'")
        print(x["result"][0]["name"])
        return x["result"][0]["name"]
    except:
        return "ERROR"

# get_parents_name ("J13","ICD10")

ds["code_description"] = ds.apply(lambda row: get_code_description(row['id'],row['code'],row['original_code_system']), axis=1)
ds["level1_code_description"] = ds.apply(lambda row: get_code_description(row['id'],row['nearest_level1_code'],row['original_code_system']), axis=1)
ds["umls_cui"] = ds.apply(lambda row: get_umls_cui(row['code'],row['original_code_system']), axis=1)
ds["level1_umls_cui"] = ds.apply(lambda row: get_umls_cui(row['nearest_level1_code'],row['original_code_system']), axis=1)
ds["parent_ui"] = ds.apply(lambda row: get_parents_ui(row['id'],row['nearest_level1_code'],row['original_code_system']), axis=1)
ds["parent_name"] = ds.apply(lambda row: get_parents_name(row['id'],row['nearest_level1_code'],row['original_code_system']), axis=1)

# Codes no CM
# ds["code_description_woCM"] = ds.apply(lambda row: get_code_description(row['code'],row['original_code_system'],False), axis=1)
# ds["level1_code_description_woCM"] = ds.apply(lambda row: get_code_description(row['nearest_level1_code'],row['original_code_system'],False), axis=1)
# ds["umls_cui_woCM"] = ds.apply(lambda row: get_umls_cui(row['code'],row['original_code_system'],False), axis=1)
# ds["level1_umls_cui_woCM"] = ds.apply(lambda row: get_umls_cui(row['nearest_level1_code'],row['original_code_system'],False), axis=1)

ds.to_csv('FINAL_parent_name.csv')
ds.to_json('test.json',orient='records')
ds.to_html('test.html')

code="A08.3"
code_sys="ICD10"

get_code_description (code,code_sys)
get_umls_cui (code,code_sys)
get_parents_ui (code,code_sys)
get_parents_name (code,code_sys)