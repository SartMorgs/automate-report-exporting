# Automate Report Exporting - XLSX Generation from ERP Report Export

This repository has a python code to download reports from ERP used by Ótica Nany and use this data to generate a XLSX report. This report is used by the store to track the client's requests.
The content of this abstract are:

- How to run it by yourself
- How it works
- How to report bugs and errors
- How to contribute

## How to run it by yourself

1. Set the following environment variables in a .env file:
- URL
- W_USERNAME
- W_PASSWORD

2. Install requirements
´pip install -r requirements.txt´

3. Run main.py or generate .exe file
- ´python main.py´
- ´pyinstaller --onefile --add-data ".env;." --windowed main.py´

## How it works

It first uses selenium to navigate over ERP pages to report page, set filters, download the file and save it in a specific folder. Right after, it uses the data generated and build a XLSX report in a specific folder.
![alt text](img/image.png)

## How to report bugs and errors

In case of bugs and problems with the execution, there can be opened a github's issue in this repository describing clarery the situation. You can find some advices to open a good issue.