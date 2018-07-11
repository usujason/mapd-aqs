create table utahdailyweather_withkeys as
select
aqs.stationkey,
udw.*
from utahweathertransposed as udw
left join aqistations as aqs on (udw.countycode = aqs.countycode and udw.sitenum = aqs.sitenum);

-- export data to csv from postgis, load to mapd
PGPASSWORD=password psql -h localhost -U mapd gisdata -c "\\Copy (select *, ST_ASTEXT(geom4326) as geo from utahlirparcels_with_keys) To STDOUT With CSV HEADER DELIMITER ',';" >> utahlirparcels_with_keys.tsv
PGPASSWORD=password psql -h localhost -U mapd gisdata -c "\\Copy (select * from utahdailyweather_withkeys) To STDOUT With CSV HEADER DELIMITER ',';" >> utahdailyweather_withkeys.tsv
