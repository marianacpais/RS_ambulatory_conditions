import pandas as pd
import numpy as np

table =  pd.read_excel("TABLE1_updated.xlsx")
table.to_html('finalTable.html')
table.to_json('finalTable.json',orient='records')

# Filtrar por major_grouping_variable
# Agrupar por artigo
# Juntar códigos

ds =  pd.read_excel("table_generator/finalTable.xlsx")

majors = table.major_grouping_variable.unique()
articles = table.article.unique()

table = pd.DataFrame(
    columns = articles,
    index = majors
)

def format_code_list (codes):
    formatted_codes = ""
    for code in codes[:-1]:
        formatted_codes = formatted_codes + str(code) + ", "
    formatted_codes = formatted_codes + str(codes.iloc[-1])
    return(formatted_codes)

article = articles[10]
major = majors[6]
codes = ds[(ds.major_grouping_variable == major) & (ds.article == article)].code

for major in majors:
    print(major)
    for article in articles:
        codes = ds[(ds.major_grouping_variable == major) & (ds.article == article)].code
        print(article)
        if (len(codes) > 0):
            formatted_codes = format_code_list (codes)
            table.at[major, article] = formatted_codes
        else:
            table.at[major, article] = "-"

table["Unnamed: 0"] = table["Unnamed: 0"].apply(lambda row: "<strong>"+str(row)+"</strong>")

table.to_html('Table1FINAL.html', escape = False)
table.to_csv('Table1FINAL.csv')
