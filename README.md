# DB loader #

DB loader is a simple project to test loading data into an Azure SQL database using Azure functions. This document serves as documentation and collects the learning steps involved in the process. Data is produced by a random number generator in an Azure function running on a timer and added to the database. The randomness of the random number generator is then monitored in powerBI.


## Database setup ##

We use the simplest/cheapest available option for the database with the following settings:
* Basic, DTU based with 5 DTUs (up to 2GB storage, $4.9/month)
* Server in Sweden Central
* Locally reduntant backup
* SQL authentication (no Azure AD on free accounts)
* No access by default (This allows no outside connections to the server)

Access can at a later point be controlled at the db-server settings -> Networking. To access the DB from a local computer, we allow public access from selected networks and add specific client IPs (our own) as firewall exception rules. We can then for example use Azure data studio to work with the database.

Additional users for the database server can for example be created from within Azure data studio by querying the master database:

    CREATE LOGIN <login_name> WITH password='<password>';

Then, within each database by running T-SQL queries, we can create a user from the login:

    CREATE USER <user_name> FROM LOGIN <login_name>;

We then give permissions to the user by assigning a database role:

    EXEC sp_addrolemember '<database_role>', '<user_name>'

For a list of available roles, see [here](https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/database-level-roles?view=sql-server-ver16). Common useful roles may be 'db_datawriter' and 'db_datareader'.

Note: To remove a login, we can use

    DROP LOGIN <login_name>;


## Read and write operations to DB from python ##

Basic read and write operations from python using pandas in connection with the Azure SQL db are found in example_df_operations.py. We use the pyodbc library in combiantion with SQLalchemy.


## Database preparation: Table setup ##

Next, we prepare the database for our azure function. We want to only supply credentials with write, not create permissions to the function. Thus, we need to prepare a table beforehand. The table should contain a counting id for each random number generation process (primary key) as well as the associated random number. We use TSQL to create the table:

    CREATE TABLE randomNumbers (
    process_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    random_number INT NOT NULL,
    );

The table can be dropped to createa  clean instance of the database by

    DROP TABLE IF EXISTS randomNumbers;


## Azure functions: Setup local development environment ##

Developing azure functions locally on a M1/M2 Macbook can come with various challenges. It should be noted that running the function locally requires the use of Rosetta2 to emulate an intel architecture. We assume that VScode including the Azure extension, Azurite and the Azure CLI are installed and running.

We first prepare the system further by creating  zsh commands to activate/deactivate a Rosetta2 emulation for the console following [this](http://issamben.com/running-python-azure-function-locally-on-an-m1-m2/) tutorial. 

Next, we create a virtual python environment in the folder in which we want to develop out azure function. We therefore switch to "intel", deactivate any existing python environment via

    $ conda deactivate

and create and activate a new virtual environment

    $ python3.9 -m venv .venv
    $ source .venv/bin/activate

As a next step, to be able to interact with databases, we install pyodbc by following [this](https://whodeenie.medium.com/installing-pyodbc-and-unixodbc-for-apple-silicon-8e238ed7f216) tutorial. Next, we install ODBC drivers. Here, we follow [a guide provided by microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15) but replace brew with brew86 to ultilize our rosetta2 emulation.

Next, we can use the VS code Azure functions extension to create a local azute function project. 


## Azure functions: Development and deployment ##

First, we create a new fucntions app in the Azure portal, following [this guide](https://github.com/James-Leslie/azure-functions). Note that a nice explanation of how to access Key Vault secrets can be found [here](https://servian.dev/accessing-azure-key-vault-from-python-functions-44d548b49b37).

To develop and test the function app locally, we have to start Azurite (f1 in VS code, type Azurite: Start). We further need to modify local.settings.json:

    "AzureWebJobsStorage": "UseDevelopmentStorage=true"

to make use of Azurite. Finally, to run our app, use

    $ func start


### Deployment ###

There exist a variety of methods to deploy a fucntion to a function app.