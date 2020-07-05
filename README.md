# hershey dataset

Tool to extract svg's from hershey's font definition, dataset of already extracted fonts in svg format is available in compressed to font_svgs zip file.

actual datset is not uploaded in this repository because of the size 4.2GB ! dataset can be created by simply running the script create_globaldataset.py

```
$mkdir global_dataset
$./create_globaldataset.py
```

### Dependencies

```
matplotlib
opencv
numpy
```

## Files

./extract_hershey_font.py   python script to read hershey.jhf and output font in .svg format

./hershey.jhf               original file by Dr. Hershey contains all characters

./visualise_dataset.py 	    visualise pickled dataset

./create_globaldataset.py   creates global dataset in /global_dataset directory

This dataset was inspired from paper :

### Teaching Robots To Draw

Atsunobu Kotani and Stefanie Tellex

Department of Computer Science

Brown University

### NOTE !

Original paper was based on japanese characters, you can also extract the same using the script in this repository

### TODO :

[ ] create a complete dataset of action lines and other information for training both global and local model

[ ] create a pickled form of dataset
