#Ryan Nguyen & Cheoljun Hwang
import csv
import psycopg2

DBPASSWORD='postgrespass1' #put your DB password here
USERNAME='postgres' #put your username here
DBNAME='hw4DB' #DB name goes here
TABLE_NAME='day'#choose relation you want to insert into;
CSV_NAME = 'DAYV2PUB.csv'#choose .csv file to import from
EIA=False #EIA = True if cvs is from EIA
HEADER_VALUES = '%s, %s,%s,%s, %s,%s,%s, %s,%s'#%s for each included column
INCLUDED_COLS = [0,1,57, 83,91,93,94,96,109]
#for EIA files:[0,1,2] '%s, %s,%s'
#for vehicle: [0,2,14,30,32,51,52,55,56,57,58]  '%s, %s,%s,%s, %s,%s,%s, %s,%s,%s,%s' 
#for day: [0,1,57, 83,91,93,94,96,109]    '%s,%s, %s,%s,%s, %s,%s,%s, %s'
TEST=False#TEST= True if you want to create a smaller test table (not using the whole csv)
TEST_SIZE=10000
def main():
    conn = psycopg2.connect('dbname='+DBNAME+ ' user='+ USERNAME + ' password='+ DBPASSWORD)
    cur = conn.cursor()
    #create table first, using this format:
    #cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")#######
    with open(CSV_NAME, 'r') as csvfile:
        row_list = csv.reader(csvfile, delimiter=',', quotechar="'")
        for i, row in enumerate(row_list):
            flag=0
            content = list(row[j] for j in INCLUDED_COLS)          
            if (i == 0):
                headers = content
                #uncomment the next 2 lines to print headers for creating table
                #print(', '.join(headers)) ##############
                #break #################
                continue
            #makes sure day ignores negative values
            if CSV_NAME=='DAYV2PUB.csv':
                for x,y  in enumerate(content):#iterate through tuples
                    if (x==6 and float(y) < 0):
                        flag = 1
                        break               
                if flag == 1:
                    continue



            if EIA == True:
                for x,y  in enumerate(content):#iterate through tuples
                    if (x==2 and y == 'Not Available'):
                        content[x]=None
                        break
            cur.execute('INSERT INTO '+TABLE_NAME+" ( "+', '.join(headers) + ") VALUES ("+HEADER_VALUES+")", tuple(content))
            #for smaller test tables:

            if i == TEST_SIZE and TEST== True:
                break
        conn.commit()
        cur.close()
        conn.close()
if __name__ == '__main__': main()
