#Ryan Nguyen & Cheoljun Hwang
# python database querying interface for a class assignment 
import psycopg2



def main():
    conn = psycopg2.connect("dbname=hw4DB user=postgres password=postgrespass1")
    cur = conn.cursor()
    while (True):
        problem= input('\nEnter problem part for problem3 (a, b, c, or d) or enter q to quit: ')
        #####Problem3a vvvvvvvvvv
        if problem == 'a':
            print('querying, please wait....')
            for i in range(5,101,5):
                cur.execute('select cast(cast((select count(*) from (select HOUSEID, PERSONID, SUM(TRPMILES) AS SUM_T FROM DAY GROUP BY HOUSEID, PERSONID having sum(trpmiles) < '+ repr(i) +')A) as float)/ ((select count(*) from (select HOUSEID, PERSONID, SUM(TRPMILES) AS SUM_T FROM DAY GROUP BY HOUSEID, PERSONID)B)) *100 as Decimal(6,2)) as answer')
                answer1 = cur.fetchone()
                number=float(answer1[0])
                print(repr(number) + "% of individuals travel less than " +repr(i)+ " miles a day\n")
        #####Problem3a  ^^^^^^^   
        #####Problem3b  vvvvvvv
        if problem == 'b':
            print('querying, please wait....')
            for j in range(5,101,5):
                cur.execute('SELECT CAST((SUM(C.TRPMILES) / SUM(C.TRPMILES / C.EPATMPG)) AS DECIMAL(6,2)) AS AVG_FUEL_ECO FROM ((SELECT HOUSEID,VEHID,TRPMILES,STRTTIME FROM DAY GROUP BY HOUSEID,VEHID,TRPMILES,STRTTIME HAVING cast(VEHID as integer) >= 1 AND TRPMILES < '+ repr(j) +') A  INNER JOIN VEHICLE B ON A.HOUSEID = B.HOUSEID AND A.VEHID = B.VEHID)C')
                answer2 = cur.fetchone()
                print("The average fuel economy is "+ repr(float(answer2[0])) + " mpg for individuals driving less than " +repr(j)+ " miles a day\n")
        #####Problem3b   ^^^^^^^
        #####Problem3c     vvvvvv
        if problem == 'c':    
            print("Percent of transportation CO2 emissions attributed to household vehicles: ")
            print('querying, please wait....')
            cur.execute("SELECT TDATE,CAST((TOTAL_HHV_CO2_EMIT *30.4 / (VALUE * 1000000) * 100) AS DECIMAL(5,3)) AS PERCENT FROM ((SELECT D.TDATE,COUNT(DISTINCT D.HID), SUM(D.TMILES / D.EPATMPG) * 0.008887 / COUNT(DISTINCT D.HID) * 117538000 AS TOTAL_HHV_CO2_EMIT FROM(SELECT TDATE, HID, VID, TMILES, STIME, EPATMPG FROM((SELECT HOUSEID AS HID, VEHID AS VID,TRPMILES AS TMILES,TDAYDATE AS TDATE, STRTTIME AS STIME FROM DAY GROUP BY HOUSEID,VEHID,TRPMILES,TDAYDATE,STRTTIME HAVING cast(VEHID as integer) >= 1) A INNER JOIN VEHICLE B ON A.HID = B.HOUSEID AND A.VID = B.VEHID)C GROUP BY C.HID, C.VID, C.TMILES, C.TDATE, C.STIME, C.EPATMPG ORDER BY C.TDATE, C.STIME, C.HID, C.VID, C.TMILES) D GROUP BY D.TDATE ORDER BY D.TDATE) E INNER JOIN (select yyyymm, value from eia_trans where cast(yyyymm as integer) >= 200803 AND cast(yyyymm as integer) <= 200904 AND MSN = 'TEACEUS' ) F ON E.TDATE = F.YYYYMM ) G ")
            answer3 = cur.fetchall()
            for k in range(len(answer3)):
                print(answer3[k][0] + ' : ' + repr(float(answer3[k][1])) + '%')

            #for month in ['03/2008','04/2008', '05/2008','06/2008','07/2008','08/2008','09/2008','10/2008','11/2008','12/2008', '01/2009','02/2009','03/2009','04/2009'] 
             #   print(month+':'+answer)

        #####Problem3c   ^^^^^^^^
        ####Problem3d     vvvvvvv
        if problem == 'd':
            for x in [20,40,60]:
                print('querying, please wait....')                
                cur.execute("SELECT TDATE, SUM(CHANGE_OF_CO2) FROM(SELECT TDATE, HID, VID, TMILES, EPATMPG, TMILES/EPATMPG * 0.00887 AS GAS_CO2, CASE    WHEN TMILES <= "+repr(x) +"THEN TMILES/EPATMPG * 33.1/3.0 * D.CO2_KWH  WHEN TMILES > "+repr(x)+" THEN "+repr(x) +"/EPATMPG * 33.1/3.0 * D.CO2_KWH END AS ELE_CO2, CASE    WHEN TMILES <= "+repr(x)+" THEN TMILES/EPATMPG * 33.1/3.0 * D.CO2_KWH - TMILES/EPATMPG * 0.00887 WHEN TMILES >"+repr(x) +" THEN "+repr(x)+"/EPATMPG * 33.1/3.0 * D.CO2_KWH - "+repr(x)+"/EPATMPG * 0.00887 END AS CHANGE_OF_CO2 FROM (((SELECT HOUSEID AS HID, VEHID AS VID,TRPMILES AS TMILES,TDAYDATE AS TDATE, STRTTIME AS STIME FROM DAY GROUP BY HOUSEID,VEHID,TRPMILES,TDAYDATE, STRTTIME HAVING cast(VEHID as integer) >= 1) A INNER JOIN VEHICLE B ON A.HID = B.HOUSEID AND A.VID = B.VEHID)C INNER JOIN(SELECT A.YYYYMM, A.VALUE / B.VALUE AS CO2_KWH FROM EIA_ELECTRIC A, EIA_MKWH B WHERE A.MSN = 'TXEIEUS' AND B.MSN = 'ELETPUS' AND A.YYYYMM = B.YYYYMM) D ON C.TDATE = D.YYYYMM )GROUP BY C.HID, C.VID, C.TMILES, C.TDATE, C.EPATMPG, D.CO2_KWH, C.STIME ORDER BY C.TDATE, C.STIME, C.HID, C.VID, C.TMILES ) E GROUP BY TDATE ORDER BY TDATE")
                answer4 = cur.fetchall()
                print('\nChange of CO2 with '+ repr(x) +' miles of electric range: ')
                for y in range(len(answer4)):
                    print(answer4[y][0] + ' : ' + repr(float(answer4[y][1])) + ' metric tons of CO2')
                    
        ####Problem3d     ^^^^^^^
        if problem == 'q':
            print('Goodbye')
            break
    cur.close()
    conn.close()
if __name__ == '__main__': main()
