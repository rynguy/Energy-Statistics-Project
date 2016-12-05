﻿/*#Ryan Nguyen & Cheoljun Hwang*/

SELECT TDATE,CAST((TOTAL_HHV_CO2_EMIT*30.4 / (VALUE * 1000000) * 100) AS DECIMAL(5,3)) AS PERCENT
FROM 
(
	(
		SELECT D.TDATE,COUNT(DISTINCT D.HID), SUM(D.TMILES / D.EPATMPG) * 0.008887 / COUNT(DISTINCT D.HID) * 117538000 AS TOTAL_HHV_CO2_EMIT
		/* COUNT(DISTINCT D.HID) = TOTAL NUMBER OF HOUSEHOLDS FOR EACH MONTH, SUM(D.TMILES / D.EPATMPG) = TOTAL GASOLIN CONSUMED FOR EACH MONTH. WE MULTIPLY BY 30.4 TO APPROZIMATE MONTH */
		FROM
		(
			
			SELECT TDATE, HID, VID, TMILES, STIME, EPATMPG 
			FROM
			(
				
				(SELECT HOUSEID AS HID, VEHID AS VID,TRPMILES AS TMILES,TDAYDATE AS TDATE, STRTTIME AS STIME
				FROM DAY
				GROUP BY HOUSEID,VEHID,TRPMILES,TDAYDATE,STRTTIME
				HAVING cast(VEHID as integer) >= 1
				) A 
				/* A : GET A RESULT FOR EACH TRIP WHICH BELONGS TO HOUSEHOLD VEHICLES */
				INNER JOIN VEHICLE B
				ON A.HID = B.HOUSEID AND A.VID = B.VEHID
			)C /* C : ADD MATCHED EPATMPG TO THE TABLE A*/
			GROUP BY C.HID, C.VID, C.TMILES, C.TDATE, C.STIME, C.EPATMPG
			ORDER BY C.TDATE, C.STIME, C.HID, C.VID, C.TMILES
		) D /* A + EPATMPG*/
		GROUP BY D.TDATE
		ORDER BY D.TDATE
	
	) E /* MODIFED D SORTED ACCORDING TO D.TDATE */
	
	INNER JOIN 

	(	 
		select yyyymm, value from eia_trans
		where cast(yyyymm as integer) >= 200803 AND cast(yyyymm as integer) <= 200904
		AND MSN = 'TEACEUS'
	) F
	
	ON E.TDATE = F.YYYYMM 
) G /* ADD A TOTAL CO2 EMISSION FROM ALL SOURCES OF TRANSPORATION(= VALUE) FOR EACH MONTH TO E */