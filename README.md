# Databases Project


Description of files: 
DATABASE INITIALIZATION:
* InitDatabaseAll: creates csv file that contains anonymized student records; coordinates are added afterwards

FRONT END:
* 

BACK END: The backend implements the api defined in the spec using a Flask Server.
* loader.py: script to read from data csv and upload rows into database 
* project.py: runs the flask server and sets up routes on port 5000 
* data.csv: anonymized data used 
* database 
	* dao 
		* crud: directory containing data access objects for each table 
    	* base_dao: base class for data access objects which creates a wrapper over mysqlquerybuilder 
    	* application_dao: implements higher level database operations which need multiple tables 
  * models: directory containing data objects defining their properties 
  * serializers: directory containing serializers which take data objects and output objects ready for json dumping 
  * .env: configuration file for database 
  * connection_manager: responsible for connecting to database and returning connection 
  
