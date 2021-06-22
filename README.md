# TIC-Pipeline

TIC-Pipeline is a suite that processes FASTQ files to create ASVs based on the latest golden standards,
and then performs a diversity analysis of the ASVs.

## Introduction:
The importance of 16S rRNA gene amplicon profiles for understanding the influence of microbes in a variety of environments coupled with the steep reduction in sequencing costs led to a surge of microbial sequencing projects. The expanding crowd of scientists and clinicians wanting to make use of sequencing datasets can choose among a range of multipurpose software platforms, the use of which can be intimidating for non-expert users. Here we present the TIC-Pipeline, a mix of python, R, and bash tools 
that encode a series of well-documented choices for the downstream analysis of whole microbial studies, including the 
creation of ASVs, taxonomic assignments based on both known and novel taxonomic paths, a novel clustering method based on the taxonomic assignment and elementary graphing options.
TIC-Pipeline is primarily a straightforward starting point for beginners, but can also be a framework for advanced users who can modify and expand the tool. As the community standards evolve, TIC-Pipeline will adapt to always represent the current state-of-the-art in microbial profiles analysis in the clear and comprehensive way allowed by the python language.


## Description:

### Organization
TIC-Pipeline is composed of 4 steps that can be run independently or as a set.

    1.ASV-Creation
    2.Taxonomy-Classification
    3.Taxonomy-Informed-Clustering
    4.Results_Processing

Running them in the given order simplifies the process as the outputs of each step are often the inputs of the next. There is also an extra folder where the original data is recommended to be placed to keep the analysis of one study in a compact and organized structure. Inside the Original-Data folder are contained the template files that served as basis for the TIC-Pipeline presentation that can be used for training purposes. Before running any script, please make sure you have read and fully understood the corresponding ReadMe file that can be found in each folder.

## Requirements:
TIC-Pipeline is a mix of bash, Python and R scripts. Due to relience on bash tools we propose the usage of a Linux system for simplifying running the scripts.

## Installation:
In the folder: 0.Setup_and_Testing we provide a script called setup.sh that downloads and installs all required tools
for the pipeline.
To run the script execute the following commands:
```
cd 0.Setup_and_Testing
chmod +x setup.sh
./setup.sh
```

## Testing:
Before running the pipeline with your data, we propose to check if all programs are correctly installed.
To do this change the TESTING_MODE in config_options.txt to YES
and run:
```
python3 TIC-Pipeline.py
```
Based on the output of this command, you can verify that the pipeline will find the necessary tools.


## Citation: