# Huggingface Docs Offline Search

Description: This project is to build a lightweight search engine with the huggingface documentation for possible use in RAG applications later on. Huggingface publically maintains its documentation in a repository in their datasets library.


### Setup

 - 


### Notes

 - Unfortunately, just having the HTML files is not enough. The actual article data that is rendered is spread out across different files in the `huggingface_docs/MODULE/main/en/` folder. This means that tools like beautiful soup are not sufficient for loading and parsing the data but automated browsers like playwright or selenium will be required, which may cause a drop in performance.


### References

 - huggingface
     - [huggingface docs](https://huggingface.co/datasets/hf-doc-build/doc-build) on huggingface datasets.
     - [huggingface docs](https://huggingface.co/docs) main page.
     - [huggingface doc-builder](https://github.com/huggingface/doc-builder) GitHub repository.
