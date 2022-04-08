# Python
This is the third practical for CS2006.
It contains a code directory with all the code for refining the data (clean_data.py) which can be run with the argument containing the filepath to the raw CSV data as well as for getting all images from a Jupyter notebook (getnb_images.py) which should br run with the arguments for the notebook filepath and the output path (image directory) and finally a unit testing file (cleanTest.py - discussed in Test section).
It also contains an image directory for storing gathered images, a data directory for storing all the data and a notebooks directory containing 2 Jupyter notebooks, 1 with analysis on the raw data and another with analysis on the refined data.

## Requirements
The following modules must be installed via the python module installer of your choice (pip, anaconda etc.)

    wordcloud
    matplotlib
    pandas

## Additional Custom Requirement
The file get_image_links.py contains code for extracting links to images from tweets and saves them to the images directory - this code can be run from the code directory, we have checked that this code works, however, it should be noted that running it will download a very large number of images from twitters database and as such will also take a long time to do so.
You may also wish to note that, once this starts running Ctrl+C will not interrupt the program, instead you must use Ctrl+Pause.

## Test
To run the tests, cd to the code folder and run the following file
    
    cleanTest.py
    
