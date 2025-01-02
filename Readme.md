# eqsl_saver

The **eqsl_saver** is a Python3-script, that save the eQSLs from eqsl.cc's Archive folder.

## Prerequisites
- Python 3.x
- [requests](https://docs.python-requests.org/en/latest/index.html) module
- [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/) module

## Usage
1. Clone the repository or download the sdrangel_ft8_2_adif.py file.
2. Open a terminal or command prompt and navigate to the directory, where the file is located.
3. Run the following command to start the program - in Linux:
    ```
    pip3 install -r requirements.txt
    python3 eqsl_saver.py username
    ```
    in Windows:
    ```
    pip install -r requirements.txt
    python eqsl_saver.py username
    ```
    the *username* is the callsign.