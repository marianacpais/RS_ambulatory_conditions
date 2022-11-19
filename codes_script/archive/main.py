import pandas as pd
import requests

ds =  pd.read_excel("small_test.xls")

def get_ICD10_code_description (code):
    url = 'http://www.icd10api.com/?code=' + code + '&Type=CM'
    x = requests.get(url).json()
    print("Got description for code '"+code+"'")
    if x["Response"] == 'False':
        print("ERROR in getting description for code '"+code+"'")
    else:
        print("Got description for code '"+code+"'")
        return x["Description"]

def get_ICD9_code_description (code):
    url = 'https://www.hipaaspace.com/api/icd9/getcode?q=' + code + '&rt=json&token=08265B178E994E658B9C04737F141EDB2898E139420342EEB2EC7FC806031C45'
    # Nota IMP! É preciso tirar o ponto para passar os códigos: por ex hipoK que é 276.8 deve ser passado como 2768
    # Além disso, para os códigos "header" (que têm só 3 digitos como por ex 280 para anemia ferrop), vai ser preciso add 0 final
    x = requests.get(url).json()
    return x["ICD9"][0]["Description"]

def get_ICD9_to_ICD10 (code):
    url = 'https://www.hipaaspace.com/api/icd9to10/mapcode?&q=' + code + '&rt=json&token=08265B178E994E658B9C04737F141EDB2898E139420342EEB2EC7FC806031C45'
    # Nota IMP! É preciso tirar o ponto para passar os códigos: por ex hipoK que é 276.8 deve ser passado como 2768
    # Além disso, para os códigos "header" (que têm só 3 digitos como por ex 280 para anemia ferrop), vai ser preciso add 0 final
    x = requests.get(url).json()
    return x["ICD9ToICD10"]["DefaultMapping"]["ICD10"]["@code"]

def format_ICD9_codes (code):

ds["ICD10_code_description"] = ds['code_description'] = ds.filter(items="original_code_system",axis=0).apply(get_ICD10_code_description)

ds["code_description"] = ds[ds["original_code_system"] == 'ICD10']["code"].apply(get_ICD10_code_description)

ds["ICD10_code_description"] = ds["code"].apply(get_ICD10_code_description)
ds["ICD10_level1_code_description"] = ds["nearest_level1_code"].apply(get_ICD10_code_description)
ds["ICD9_code_description"] = ds["code"].apply(get_ICD10_code_description)
ds["ICD9_level1_code_description"] = ds["nearest_level1_code"].apply(get_ICD10_code_description)

ds.to_csv('test.csv')
