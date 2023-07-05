# miniWMS
miniWMS is a minimalistic WMS system with support for a barcode reader and a label creation function.
It's currently developed as a website based app using Flask.
## How to use

### There are 3 types of users: <b>Admin, Manager and Worker</b>
<br>
-<b>Admin</b> has a right to create new categories of goods, types of goods, warehouses, add new customers/suppliers and create new users.
<br>
-<b>Manager</b> has a right to create a new receipt and issue of goods, and to create a move action. While creating this actions a manager has an option of choosing
a specific user to handle a task he creates or he can let users assign themselves.
<br>
-<b>Worker</b> and every aforementioned type of user has a right to lookup and handle tasks created by managers.


### How to read barcodes created by this system
#### This software supports the use of USB Barcode Scanners but their not neccesary for the program to function.
Every barcode consists of 3 letter prefix and then variable size id.
<br>
For example <b>rec-213</b> would mean a record with a id of 213

### list of prefixes used.

-rec for record
<br>
-rei for receipt of goods
<br>
-iss for issue of goods
<br>
-mov for move action
<br>
-pos for position in the warehouse
<br>
-typ for good type

## Running for the first time
After logging using an account with administrator privlages you should create your first <b>categories, good types and warehouses</b> using the <b>other actions tab</b>.
<br>
Then you can start using your system by creating a <b>receipt of goods</b> to insert your first records into the system.
<br>
Then you can go into the index by clicking <b>miniWMS</b> to handle the receipt of goods or any other action a manager has created previously.
While handling the receipt you should print out both the records and action labels to use them later.
<br>
To move your products from the arrival gate to the position their going to stay in you should create a <b>move</b> action.
<br>
Finally you can create a stock issue to create a inhouse CI. Note that the records will still be available in the system even after the issue.
## How to install 
To run to this app you need to deploy it any of the supported servers https://flask.palletsprojects.com/en/2.2.x/deploying/
and also install mysql server and add the miniwms.sql schema to it.
<br>
After setting up the db server you need to export your username(as DB_USER_MWS) and password (as DB_PASS_MWS).
<br>
If your db server is not running as localhost or the schema your using is not named miniwms then you are welcome to change the code in lines 26-33.
<br>
When all of the install requierments are met then you can login using a default user with username: admin and password: admin
that you can delete manually from the database after creating your own admin user.
<br>
<b>
DO NOT DELETE ROWS FROM OPERATION_TYPE THIS WILL RESULT IN APPLICATION RAISING ERRORS.</b>