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

Then, within each database by running T_SQL queries, we can create a user from the login:

    CREATE USER <user_name> FROM LOGIN <login_name>;

We then give permissions to the user by assigning a database role:

    EXEC sp_addrolemember '<database_role>', '<user_name>'

For a list of available roles, see [here](https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/database-level-roles?view=sql-server-ver16). Common useful roles may be 'db_datawriter' and 'db_datareader'.

Note: To remove a login, we can use

    DROP LOGIN <login_name>;


## Read and write operations to DB from python ##

Basic read and write operations from python using pandas in connection with the Azure SQL db are found in example_df_operations.py. We use the pyodbc library in combiantion with SQLalchemy.