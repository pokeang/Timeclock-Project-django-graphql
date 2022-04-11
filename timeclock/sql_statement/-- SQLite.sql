-- SQLite


SELECT ((julianday(clock_out) - julianday(clock_in)) * 24) as today
FROM timetable where user_id=3 AND strftime('%Y-%m-%d', clock_in) = strftime('%Y-%m-%d', date('now'));


SELECT clock_in, clock_out from timetable WHERE user_id=3 AND clock_in like '2022-04-10%';

SELECT id, sum((julianday(clock_out) - julianday(clock_in)) * 24) as currentWeek
FROM timetable where user_id=3 AND
 DATE(clock_in) >= DATE('now', 'weekday 0', '-7 days');

SELECT sum((julianday(clock_out) - julianday(clock_in)) * 24) as currentMonth
FROM timetable where user_id=3 AND strftime('%Y', clock_in) = strftime('%Y',date('now')) AND 
strftime('%m', clock_in) = strftime('%m', date('now'));

delete from timetable where clock_in like '2022-04-10%';
SELECT clock_in, clock_out from timetable WHERE user_id=3;

-- update timetable set clock_out='2022-04-09 18:40:00' where user_id=3 and clock_in='2022-04-09 02:40:00';


