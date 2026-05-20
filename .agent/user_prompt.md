## Requirement

- Markdown is used by default when writing documents, unless the user specifies a document type.
- The chart drawing in Markdown documents is not allowed to use text construction, but rather the format of Mermaid.
- The user's questions and responses need to be saved in the "user_QA.md" document under the current directory, and the question-and-answer record should be appended to the document. Please read the content of the document first if it exists.

###  Document `user_QA.md` additional format

```markdown
## User Q&A Records

> **Question**: 今天是什么日期?  
> **Answer**: 今天是 2026-05-18  

> **Question**: 今天星期几?  
> **Answer**: 今天是星期一  

...

> **Question**: 最近的周六在哪一天?  
> **Answer**: 2026-05-16(星期六)最近, 下一个周六在 2026-05-23  

```

## Habit

- Front-end development is commonly carried out using the vue+vite approach
- Backend development is typically carried out using Java and Spring Boot, with Maven used for building
- Machine learning, neural networks, large models, and AI-related development are conducted using Python. Before development, a virtual environment is created and relevant dependencies are installed within it



## The operation of files needs to follow the following process

### Copy File
1. First, check whether the target file exists. If it does not exist, proceed to step 2; if it exists, proceed to step 4
2. Create the target file and proceed to step 3
3. Write (overwrite) the content of the source file that has been re-read into the target file, and execute step 5
4. Prompt the user whether to overwrite the existing file, confirm to execute 3, or cancel to execute 5
5. End of file copying

### Copy Folder
1. First, check whether the target folder exists. If it does not exist, proceed to step 2; if it exists, proceed to step 3
2. Create the target folder and proceed to step 3
3. Perform the "Copy File" operation on the files in the source folder, finish proceed to step 4
4. Check whether the source folder contains subfolders. If it does, perform the "Copy Folder" operation on the subfolders. After completion, proceed to step 5
5. End of folder copying

### Move File
1. First, check whether the target file exists. If it does not exist, proceed to step 2; if it exists, proceed to step 4
2. Create the target file and proceed to step 3
3. Write (overwrite) the content of the source file that has been re-read into the target file, and execute step 5
4. Prompt the user whether to overwrite the existing file, confirm to execute 3, or cancel to execute 6
5. Remove source file, and execute step 6
6. End of file copying


## Requirement

- Before the first run, it is necessary to understand all the files and subdirectories in the current directory to avoid ambiguity in describing user behavior. 