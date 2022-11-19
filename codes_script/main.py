import pandas as pd
import requests

ds =  pd.read_excel("complete.xlsx")

def get_code_description (code,code_sys,cm_bool=True):
    if cm_bool:
        code_sys = code_sys + "CM"
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/current/source/'+code_sys+'/' + code + '?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        print("Got description for " + code_sys +" code '"+code+"'")
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

def get_parents_ui (code,code_sys,cm_bool=True):
    if cm_bool:
        code_sys = code_sys + "CM"
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/2022AB/source/'+code_sys+'/' + code + '/parents?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        print("Got parent ui for " + code_sys +" code '"+code+"'")
        return x["result"][0]["ui"]
    except:
        return "ERROR"

# get_parents_ui ("J13","ICD10")

def get_parents_name (code,code_sys,cm_bool=True):
    if cm_bool:
        code_sys = code_sys + "CM"
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/2022AB/source/'+code_sys+'/' + code + '/parents?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        print("Got parent name for " + code_sys +" code '"+code+"'")
        print(x["result"][0]["name"])
        return x["result"][0]["name"]
    except:
        return "ERROR"

# get_parents_name ("J13","ICD10")

ds["code_description"] = ds.apply(lambda row: get_code_description(row['code'],row['original_code_system']), axis=1)
ds["level1_code_description"] = ds.apply(lambda row: get_code_description(row['nearest_level1_code'],row['original_code_system']), axis=1)
ds["umls_cui"] = ds.apply(lambda row: get_umls_cui(row['code'],row['original_code_system']), axis=1)
ds["level1_umls_cui"] = ds.apply(lambda row: get_umls_cui(row['nearest_level1_code'],row['original_code_system']), axis=1)
ds["parent_ui"] = ds.apply(lambda row: get_parents_ui(row['nearest_level1_code'],row['original_code_system']), axis=1)
ds["parent_name"] = ds.apply(lambda row: get_parents_name(row['nearest_level1_code'],row['original_code_system']), axis=1)

# Codes no CM
# ds["code_description_woCM"] = ds.apply(lambda row: get_code_description(row['code'],row['original_code_system'],False), axis=1)
# ds["level1_code_description_woCM"] = ds.apply(lambda row: get_code_description(row['nearest_level1_code'],row['original_code_system'],False), axis=1)
# ds["umls_cui_woCM"] = ds.apply(lambda row: get_umls_cui(row['code'],row['original_code_system'],False), axis=1)
# ds["level1_umls_cui_woCM"] = ds.apply(lambda row: get_umls_cui(row['nearest_level1_code'],row['original_code_system'],False), axis=1)

ds.to_csv('test.csv')
ds.to_json('test.json',orient='records')
ds.to_html('test.html')
