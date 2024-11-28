# Multi-View Structural Graph Summaries

## Structure
The data folder only contains the INC 2023 dataset. CSS3V and BTC2019 must be downloaded and added by hand. The BTC2019 dataset is splitted into wikidata and the rest. 
The code is in src.
## Download
The BTC2019 data can be downloaded from https://zenodo.org/records/2634588 and has to be put into the folder data/BTC2019.
<br />
The wikidata data can be downloaded from https://zenodo.org/records/14234154 and has to be unzipped and put into the folder data/wikidata.
One has to unzip all files in data/wikidata:
```console
gunzip -r `find . -type f -name "*.gz"
```
<br />
The CSS3V dataset can be downloaded from https://zenodo.org/records/12752416 and has to be unzipped and put into the folder data.

# Preprocessing 
## Graphs
To prepare the datasets for the experiments, each dataset's graphs must be converted into a graph object.
Therefore, one has to run createGraph.py in src for each dataset/part.
Run:
```console
python createGraph.py [number of dataset] [part] 
```
Dataset: <br />
1: News-Knowledge-Graphs, 2: Data flow graphs, 3: Control flow graphs, 4: AST, 5: Wikidata, 6: BTC 2019 without Wikidata<br />
<br />
Part (only for Wikidata):<br />
0 to 66<br /><br />
Part (only for Source Code Graphs):<br />
0 to 13<br /><br />
Part is ignored for BTC 2019.

## Summaries
In the next step, the summaries for the graph objects are created using  createSummary.py in src.
One can create three different summaries: Attribute Collection (AC), Class Collection (CC), and Attribute Class Collection (ACC).
To get all summaries, one has to execute the code for each combination of parameters.
```console
python createSummary.py [number of dataset] [number summary model] [part]
```
Dataset: <br />
1: News-Knowledge-Graphs, 2: Data flow graphs, 3: Control flow graphs, 4: AST, 5: Wikidata, 6: BTC 2019 without Wikidata<br />
<br />
Summary Models:<br />
1: AC, 2: CC, 3: ACC
<br />
<br />
Part (only for Source Code Graphs):<br />
0 to 13<br /><br />
Part is ignored for the other graphs.

## Summary Sets for Experiments
To merge the summaries, the summaries are converted into objects suitable for merging.
Run:
```console
python summarySet.py
```

## Analyzing datasets
To get information about the different datasets, run:
```console
python analyze.py
```
Output: Terminal output and figures.<br />
Figures will be added to the analysis folder.

# Experiments 
## Pairwise Merging
The pairwise merging experiment is executed for each dataset by
```console
python mergeSummaries.py
```
The results/measured times are save in Times.
## Merging BTC 2019
The second experiment is executed by
Run:
```console
all.sh
```
The  second experiment investigates the best merge strategy for multiple summaries by merging all summaries of BTC 2019.
The results/measured times are saved in Times.
## Evaluation
To evaluate the experiments, run:
Run:
```console
python evaluate.py
```
Output: Terminal output and figures.<br />
Figures will be added to the evaluation folder, and everything related to linear regression will be added to the regression folder.
