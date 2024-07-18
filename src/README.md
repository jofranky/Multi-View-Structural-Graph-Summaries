# Multi-View Structural Graph Summaries

## Preprocessing (Graphs)
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

## Preprocessing (Summaries)
Run:
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

## Analyzing datasets
Run:
```console
python analyze.py
```
Output: Terminal output and figures.<br />
Figures will be added to the analysis folder.

## Preprocessing (Summary Sets for Experiments)
Run:
```console
python summarySet.py
```

## Experiment (Pairwise Merging)
Run:
```console
python mergeSummaries.py
```

## Experiment (Merging BTC 2019)
Run:
```console
all.sh
```

## Evaluation
Run:
```console
python evaluate.py
```
Output: Terminal output and figures.<br />
Figures will be added to the evaluation folder, and everything related to linear regression will be added to the regression folder.
