#Ryan Nguyen & Cheoljun Hwang
HW4 Program explainations

hw4query.py is straightforward. It asks you what part of problem 3 you want to solve and then uses hard coded queries to solve it. The queries that we used are included in the submission as 3_[A,B,C,D].sql


hw4parse_insert.py parses and inserts the .csv contents into a database that you created. You want to create your relations ahead of time. Then inside the program file, you change certain parameters such as the specific columns from the csv that that relation has, or the name of the .csv file to read from, etc. It automatically accesses your database, based on your inputted parameters and commits for you when it is finished. INTERNAL COMMENTS WILL LEAD THE WAY.


