# Open History LLM Framework

### Features

The are 3 main parts to operating this framework, each of which is described in the corresponding subdirectory:

- Part 1: Preprocessing - flexible raw data handling and filtering of source documents
- Part 2: Processing - streamlined text conversion from PDFs to text files
- Part 3: Model - integration of an open-source LLM


### Getting Started
#### Prerequisites

For parts 1 and 2:
- Python 3.11, Conda, Jupyter Notebook
- Required packages are shown within each of the separated parts: look for requirement files (e.g. `part1_requirements.yml`)

For part 3:
- [Singularity](https://docs.sylabs.io/guides/main/user-guide/)

#### Setting up repo
```bash
git clone https://github.com/yourrepo/open-history ## needs to be adapted
cd open-history-llm-framework
```


### Open Data Source
- [IRRI Staff Publications](https://scientific-output.irri.org/)

### Third-Party Components
- H2O GPT (Apache2.0): [https://github.com/h2oai/h2ogpt](https://github.com/h2oai/h2ogpt)
- key libraries from conda-forge

### License
This project is licensed under the Apache 2 License.
