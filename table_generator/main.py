import pandas as pd

table =  pd.read_excel("table.xlsx")
table.to_html('test.html')