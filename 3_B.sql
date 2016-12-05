﻿/*#Ryan Nguyen & Cheoljun Hwang*/

SELECT CAST((SUM(C.TRPMILES) / SUM(C.TRPMILES / C.EPATMPG)) AS DECIMAL(6,2)) AS AVG_FUEL_ECO
/* SUM(C.TRPMILES) = TOTAL TRAVELLED MILES, SUM(C.TRPMILES / C.EPATMPG) = TOTAL CONSUMED GASOLINE */
FROM
(
	(SELECT HOUSEID,VEHID,TRPMILES,STRTTIME FROM DAY
	GROUP BY HOUSEID,VEHID,TRPMILES,STRTTIME
	HAVING cast(VEHID as integer) >= 1 AND TRPMILES < 5) A 
	/* A : GET A RESULT FOR EACH TRIP WHICH HAS LESS THAN X MILES AND ALSO HOUSE VEHICLES */
	INNER JOIN VEHICLE B
	ON A.HOUSEID = B.HOUSEID AND A.VEHID = B.VEHID
)C /* C : ADD MATCHED EPATMPG TO THE TABLE A */