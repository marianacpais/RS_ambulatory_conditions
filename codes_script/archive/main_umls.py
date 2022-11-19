import pandas as pd
import requests

ds =  pd.read_excel("small_test.xls")

def get_ICD10_code_description (code):
    url = 'https://uts-ws.nlm.nih.gov/rest/content/current/source/ICD10CM/' + code + '?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        print("Got description for code '"+code+"'")
        return x["result"]["name"]
    except:
        return "ERROR"

get_ICD10_code_description ("B18")

def get_ICD9_code_description (code):
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/current/source/ICD9CM/' + code + '?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        print("Got description for code '"+code+"'")
        return x["result"]["name"]
    except:
        return "ERROR"

get_ICD9_code_description ("533")

def get_ICD10_umls_cui (code):
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/current/source/ICD10CM/' + code + '?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        atom = x["result"]["concepts"]
    except:
        return "ERROR - atom"
    url = atom + '&apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        if x['result']['recCount'] == 1:
            return x["result"]["results"][0]["ui"]
        else:
            for result in x['result']['results']:
                if result["rootSource"] == "MTH":
                    print("Got UMLS CUI for ICD10 code '"+code+"'")
                    return result["ui"]
    except:
        return "ERROR - concept"

get_ICD10_umls_cui ("J13")

def get_ICD9_umls_cui (code):
    code = str(code)
    url = 'https://uts-ws.nlm.nih.gov/rest/content/current/source/ICD9CM/' + code + '?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        atom = x["result"]["concepts"]
    except:
        return "ERROR - atom"
    url = atom + '&apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3'
    x = requests.get(url).json()
    try:
        if x['result']['recCount'] == 1:
            return x["result"]["results"][0]["ui"]
        else:
            for result in x['result']['results']:
                if result["rootSource"] == "MTH":
                    print("Got UMLS CUI for ICD9 code '"+code+"'")
                    return result["ui"]
    except:
        return "ERROR - concept"

get_ICD9_umls_cui("481")

code = "A17800855"



ds["code_description"] = ds.apply(lambda row: get_ICD10_code_description(row["nearest_level1_code"]) if row['original_code_system']=="ICD10" else get_ICD9_code_description(row["code"]), axis=1)
ds["level1_code_description"] = ds.apply(lambda row: get_ICD10_code_description(row["nearest_level1_code"]) if row['original_code_system']=="ICD10" else get_ICD9_code_description(row["nearest_level1_code"]), axis=1)
ds["umls_cui"] = ds.apply(lambda row: get_ICD10_umls_cui(row["code"]) if row['original_code_system']=="ICD10" else get_ICD9_umls_cui(row["code"]), axis=1)
ds["umls_cui_for_level_1"] = ds.apply(lambda row: get_ICD10_umls_cui(row["nearest_level1_code"]) if row['original_code_system']=="ICD10" else get_ICD9_umls_cui(row["nearest_level1_code"]), axis=1)

ds.to_csv('test.csv')