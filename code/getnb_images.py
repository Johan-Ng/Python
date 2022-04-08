import base64
import json
import sys
import os


def get_figures(notebook_filepath, output_path):
    
    notebook = open(notebook_filepath, "r")
    notebookCont = notebook.read()
    notebook.close()
    jsonNB = json.loads(notebookCont)

    counter = 1

    for cellid, cell in enumerate(jsonNB['cells']):
        if "outputs" not in cell:
            continue
        for i in range(len(cell['outputs'])):
            if "data" not in cell['outputs'][i]:
                continue
            if "image/png" not in cell['outputs'][i]['data']:
                continue
            img_data = base64.b64decode(cell['outputs'][i]['data']['image/png'])
            img_file = open((output_path + "/fig" + str(counter) + ".png"), 'wb')
            img_file.write(img_data)
            counter = counter + 1

def main():

    if(len(sys.argv) != 3):
        print("Please run with the arguments for notebook directory (first) and output images directory (second)")
        exit()

    if((not os.path.isfile(sys.argv[1])) or (not sys.argv[1].endswith(".ipynb"))):
        print("Please enter valid notebook filepath")
        exit()

    if(not os.path.isdir(sys.argv[2])):
        print("Please enter valid output directory")
        exit()
    nbfp = sys.argv[1]
    outfp = sys.argv[2]

    get_figures(nbfp, outfp)


main()
