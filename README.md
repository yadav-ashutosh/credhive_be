
# Credhive backend project

This project is submission for credhive backend evaluation assignment

## 1.) Required installations
Below are the requirements before running the application

1.) python > 3.11 

2.) Postgres 

## 2.) Running the project

1.) Do a ```pip install -r requirements.txt ``` 

2.) Modify the postgres database url in the ```.env``` file with your username and credentials and the name of the database

3.) run 
```uvicorn main:app --reload```

4.) go to http://127.0.0.1:8000/docs to access docs and test api 

## 3.) Populating data and testing 

To populate data, you can run ```populate.py``` to populate loans, annual turnover, and company data it uses faker. For testing, I have created a tests directory with a test for the PUT API for credits. Additional tests should be written to build a more robust testing suite. The ```test_json``` file contains JSON data that can be used to test APIs via the FastAPI documentation page.




## Project structure

1.) ```/Models```: Contains all 4 database table models used in project 

2.) ```/Routers```: Contains api controllers and buisness logic

3.) ```/Schemas```: Contain all the request models and pydantic validations for those models

4.) ```/Tests```: Contain data for testing the project

## Database design

I have added additional Database to store credit info for any company instead of storing it in company database itself this seperates getting, updating and deleting credit info of a company from companyDB. 

### Credits update
 
Credits are updated and created when put request is sent with loans and annual turnover for any existing company.



## Validations

Pydantic validations are added for api inputs. 

## Future extensions

1.) Exhaustive testing can be added for all apis

2.) Authentication can be added to secure apis

3.)If more data about usage of apis is available then appropirately caching can be applied to further speed up the efficiency of the application overall 
