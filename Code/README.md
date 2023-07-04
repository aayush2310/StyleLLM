<h1 align="center">StyleLLM</h1>


<p align="center" width="100%">
    <img width="25%" src="logo.png">
</p>

Guide Large Language Models to provide responses in a particular style / tone. Make your LLM sarcastic, melodramatic, or make it speak in Old English. All this with the power of pre-trained LLMs combined with effective prompts. 

Our work currently supports following styles - 
- Formal-Mode
- Indirect-Mode
- Melodramatic-Mode
- Metaphor-Mode
- Old-English
- Optimistic-Mode
- Sarcasm-Mode
- Self-Deprecating-Mode
- Witty-Mode

Inference can be made using [IBM-Generative-AI](https://github.com/IBM/ibm-generative-ai) and Huggingface Models. We have tested with [falcon-7b-instruct model](https://huggingface.co/tiiuae/falcon-7b-instruct).

## Setup
- Setup Conda env and activate : 
```
conda env create -f env_CCC.yml
conda activate stylebam
```

- Create BAM API keys from [BAM portal](https://bam.res.ibm.com/)
- Copy BAM Key and store it in `.env` file by adding the following line (.env file is in .gitignore, will not be pushed to repo. )
  `BAM_KEY=<your-key>`
- To launch Streamlit app : `streamlit run streamlit-frontend.py`

- To use Huggingface models for inference run the job on CCC with a GPU interactive job : 
```
jbsub -q x86_6h -cores 2+1  -mem 100g  -interactive bash

#Your virtual environment needs to have transformers, pytorch, streamlit, ibm-generative-ai libraries
#Use conda env yaml file to install stylebam conda env : conda env create --prefix <path> -f env_CCC.yml
conda activate <env-name> 

streamlit run streamlit-frontend.py

#open the CCCnode:port_number in the browser - you can find hostname of the node using the command hostname -f 
#if hostname is cccxc426.pok.ibm.com and streamlit uses port 8501 (default streamlit port) then the URL is : http://cccxc426.pok.ibm.com:8501/. OPen the URL in browser. 
```

- Front end is a [Streamlit](https://github.com/streamlit/streamlit) app. 


## Notebook for prototyping prompts :
- Getting to the correct prompt needs lots of iterations. For prompt engineering you can use [this notebook](./prompt-notebook/PromptTests.ipynb) to run jupyter notebook on CCC. Load any Huggingface model and try out different prompts. 





## Example Styles and Reaponses

- Metaphor as a response : 
  - Q: Do you like her?
  - A as metaphor : She is like cream in my coffee.
  - A Normal : Yes. I like her a lot.

## Related References and Datasets:

- SemEval-2022 Task 6: iSarcasmEval, Intended Sarcasm Detection in English and Arabic - [Paper](https://aclanthology.org/2022.semeval-1.111/); [Link to Original Dataset Downloa](https://github.com/iabufarha/iSarcasmEval) ; [Data Folder](./data/iSarcasmEval/)
- Creating and Characterizing a Diverse Corpus of Sarcasm in Dialogue - [Paper](https://aclanthology.org/W16-3604/) ; [Link to Original Dataset Download](https://nlds.soe.ucsc.edu/sarcasm2) ; [Data Folder](./data/sarcasm_v2/)


