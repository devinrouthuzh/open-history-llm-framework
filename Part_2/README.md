# Part 2: Data processing

## Description
This part of the repository deals with processing PDF files in order to extract text for model input. It continues on the work of previous part and creation of the folder **dataset**.  

Three additional parts have been taken out of this notebook, as they were run on the high performance computing (HPC) cluster: tesseract, doctr and realness. For each of them:  
- input data: previously created folder dataset 
- output data: found in each of their representative folders  
- specific scripts to run on our HPC cluster (respectively for each part): submission script (.sh), python script (.py) and requirements file (.yml)


Part2
- Notebook2_processing.iypn  
- part2_requirements.yml
- tesseract (part)  
  ─ tesseract/  
  ─ tesseract.sh  
  ─ tesseract.py  
  ─ tesseract_requirements.yml  
- doctr (part)  
  ─ doctr/  
  ─ doctr.sh  
  ─ doctr.py  
  ─ doctr_requirements.yml  
- realness (part)  
  ─ realness/  
  ─ realness.sh  
  ─ realness.py  
  ─ realness_requirements.yml  


## Getting Started
### Prerequisites
- Required packages: part2_requirements.yml


### Installation 
```bash
cd open-history-llm-framework/part2
conda env create -f part2_requirements.yml
conda activate part2_env
```
