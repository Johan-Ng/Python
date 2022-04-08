import pandas as pd
import re
import urllib.request
df = pd.read_csv("../data/CometLandingRefined.csv")

inp=input("Running this will download a very large number of images\nDo you wish to proceed? (ctrl+pause must be used to exit after beginning) [y/n]:")
if(inp != 'y'):
    exit()



df=df.reset_index()
urls = []
for index, row in df.iterrows():
    results = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg)', str(row['entities_str']))
    for x in results:
        if not x.startswith('http:'):
            x = 'http:' + x
        urls.append(x)

clean = []
for i in urls:
    x = i.split("\"")
    for st in x:
        clean.append(st)
count = 1

clean = list(dict.fromkeys(clean))

for i in clean:
    if(str(i).startswith("http:") and str(i).endswith(".jpg")):
        print(i)
        imgURL = str(i)
        try:
            urllib.request.urlretrieve(imgURL, "../images/test" + str(count) + ".jpg")
        except:
            print("")
        count = count + 1
    elif(str(i).startswith("http:") and str(i).endswith(".png")):
        print(i)
        imgURL = str(i)
        try:
            urllib.request.urlretrieve(imgURL, "../images/test" + str(count) + ".png")
        except:
            print("")
        count = count + 1
    elif(str(i).startswith("http:") and str(i).endswith(".gif")):
        print(i)
        imgURL = str(i)
        try:
            urllib.request.urlretrieve(imgURL, "../images/test" + str(count) + ".gif")
        except:
            print("")
        count = count + 1
