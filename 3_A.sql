/*#Ryan Nguyen & Cheoljun Hwang*/

select cast(cast((select count(*) from (select HOUSEID, PERSONID, SUM(TRPMILES) AS SUM_T FROM DAY_test
GROUP BY HOUSEID, PERSONID having sum(trpmiles) < 5)A) as float)/ ((select count(*) from (select HOUSEID, PERSONID, SUM(TRPMILES) AS SUM_T FROM DAY_test
GROUP BY HOUSEID, PERSONID)B)) *100 as Decimal(6,2)) as answer