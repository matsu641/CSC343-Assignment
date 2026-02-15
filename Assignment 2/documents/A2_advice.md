# A2 advice
## Miscellaneous
Have the psql and psycopg2 documentation bookmarked and expect to use it.

In case you didn’t read it at the time, take a look at the week 6 material. It shows how to extract values from a cursor by column name rather than column number. This is easier and less error prone.

## Coordinating between SQL and python
Remember that you have one database, no matter how many windows you have open running psql or embedded SQL code. They are all accessing the same database.

If you are confused about this, please read Demo-coordinating.txt on the Lectures page (week 6).

## Connection
Connection is an instance variable of class Recommender. It starts out as None when an instance of Recommender is initialized, and gets set up as a connection to your database when method connect is called. It continues to exist and can be used by any method in class Recommender. Your methods will use this same connection to the database over and over.

The connection to your database is closed when the method disconnect is called. This means that an error will be raised if we attempt to say connection.xxx for any method xxx.

## How does a2.py use connect and disconnect?
Notice that you do not need to (and you should not) call connect and disconnect in your methods. We can call connect once at the beginning of the program and disconnect once at the end, and all of the methods in class Recommender use that connection instance variable. None of the methods you are writing should call connect or disconnect. Just leave the connection intact for subsequent method calls to use.

We have also provided some sample tests in test_preliminary.py that call our sample test functions. Each of these functions creates an instance of Recommender called a2 and asks a2 to connect to your database before calling the method being tested several times and using assert statements to check the return value. (Using assert to check a value is much easier and less error prone than printing the value and using your probably-tired eyeballs to check it – over and over, every time you run the test.) At the end of the function, we use a2.disconnect() to close its connection to the database.

You’ll notice that the testing functions call a helper function, setup, to refresh the database. Because we want these two functions to be separate from the Recommender class, they don’t use the instance variable connection. So we pass the necessary information to setup that allows it to make its own connection. (It is possible to have multiple connections to a single database open during the execution of a Python program, just like it’s possible to have multiple psql command-line connections open in different terminal windows.) The setup functions connects to the database at the beginning and disconnects at the end, after asking the database to read in the schema and datafile. Notice that it stores its own connection to the database in a variable that also happens to be called connection, the same name we used for the instance attribute in class Recommender. But this is a local variable that is on the call stack and disappears when a call to setup ends.

In your testing, you might create a new function whose purpose is to test one of your methods on a specific scenario that you created in a data file. Notice that the setup function is passed the name of the data file to read. This means that, in that test function, you can call setup with that particular data file. You can see an example of how to do that in test_repopulate_basic.

## Using a cursor
As you know, a cursor holds on to the results of a query. You can reuse a single cursor multiple times within a method to hold the results of a sequence of queries. If you need to hold on to the results of several queries at once, create a separate cursor for each.

## Within your methods
You may need to execute multiple SQL statements in one method. You may want to create views. But you only need one try-except-finally (since all our methods have an all or nothing effect).

A nice way to organize a method is to define all the SQL strings at the beginning, saving each in a well-named variable. You can use them later on in your calls to execute.

Here’s a suggestion: write pseudo-code first before turning it into code. 

Some of these methods are big; feel free to use helpers methods!

If you update the DB, don’t forget that you need a commit, otherwise the database will roll back to how it was before.