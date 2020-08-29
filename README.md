# hershey dataset

Tool to extract svg's from hershey's font definition, dataset of already extracted fonts in svg format is available in compressed to font_svgs zip file.

actual datset is not uploaded in this repository because of the size 4.2GB ! dataset can be created by simply following below steps.

```
$./extract_hershey_font.py
$./remove_invalid_svg.py  #removes invalid files ex:  empty svg files
$mkdir global_dataset
$./create_globaldataset.py
$mkdir local_dataset
$./create_localdataset.py
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

./create_localdataset.py    create local dataset in /local_dataset directory

This dataset was inspired from paper :

### Teaching Robots To Draw

Atsunobu Kotani and Stefanie Tellex

Department of Computer Science

Brown University

### NOTE !

Original paper was based on japanese characters, you can also extract the same using the script in this repository, get the japaneses and roman jhf file from http://paulbourke.net/dataformats/hershey/ (UPDATE : both files are now available in this repository )

### TODO :

- [x] create global dataset

- [x] create local dataset

- [x] create a pickled form of global dataset

- [ ] create guide and script to get global and local dataset

- [x] added japanese characters

- [ ] make user friendly scrpts  

- [ ] write script to visualise local dataset
