import requests

apikey = args.apikey
version = args.version
outputfile = args.outputfile
inputfile = args.inputfile
sabs = args.sabs

base_uri = 'https://uts-ws.nlm.nih.gov'
apikey = "731f8791-8540-486f-bd3d-0289bc13b2f3"
code = "B18"
sabs = "ICD10CM"


code_list = []

path = '/rest/content/current/source/ICD10CM'

test = base_uri + path + code + '?apiKey=' + apikey

test2 = "https://uts-ws.nlm.nih.gov/rest/content/current/source/ICD10CM/B18?apiKey=731f8791-8540-486f-bd3d-0289bc13b2f3"

query = {'apiKey':apikey, 'string':code, 'sabs':sabs, 'inputType':'code', "searchType":"exact"} # inputType try sourceUI


output = requests.get(base_uri+path, params=query)
output.encoding = 'utf-8'
print(output.url)
outputJson = output.json()
results = (([outputJson['result']])[0])['results']

with open(inputfile, encoding='utf-8') as f:
    for line in f:
        if line.isspace() is False: 
            codes = line.strip()
            code_list.append(codes)
        else:
            continue

with open(outputfile, 'w', encoding='utf-8') as o:
    for code in code_list:
        page = 0
        
        o.write('SEARCH CODE: ' + code + '\n' + '\n')
        
        while True:
            page += 1
            path = '/search/'+version
            query = {'apiKey':apikey, 'string':code, 'rootSource':sabs, 'inputType':'sourceUI', 'pageNumber':page}
            output = requests.get(base_uri+path, params=query)
            output.encoding = 'utf-8'
            #print(output.url)
        
            outputJson = output.json()
            results = (([outputJson['result']])[0])['results']
            
            if len(results) == 0:
                if page == 1:
                    print('No results found for ' + code +'\n')
                    o.write('No results found.' + '\n' + '\n')
                    break
                else:
                    break
            
            for item in results:
                o.write('CUI: ' + item['ui'] + '\n' + 'Name: ' + item['name'] + '\n'  + 'URI: ' + item['uri'] + '\n' + 'Source Vocabulary: ' + item['rootSource'] + '\n' + 'Code: '+ code + '\n' + '\n')
                
        o.write('***' + '\n' + '\n')