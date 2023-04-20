# ParkingTicketForecasting
## Description:
This project contains one main python application, app.py, that runs a dash server to generate our web application. The json files included are different formatted versions of our final dataset (one for each model we use) that makes it much easier and quicker to load the UI. The 3 csv files, "arima.csv", "gradient.csv", and "VAR.csv" are the files containing the forcasted predictions for each of the respective models. These are also pre-generated to save time and load the data vizualization faster.

The actual dataset for our project is too large to include so we are sharing the link below. However, this dataset is not needed to run our application.

https://www.kaggle.com/code/mfaisalqureshi/us-parking-data-analysis/data

## Installation/Execution:

1. Change directory to the src folder via the command
```
cd src
```
2. Activate virtual environment via the first command for Linux/Mac or the second command for Windows
```
source env/bin/activate
.\env\Scripts\activate
```
3. Install all the required modules via one of the following commands
```
pip install -r requirements.txt
pip3 install -r requirements.txt
```
4. Start the application via the command
```
python app.py
```
5. Open the web application on your browser at the following link:

http://127.0.0.1:8050/
