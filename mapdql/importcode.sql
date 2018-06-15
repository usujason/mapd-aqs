-- create AQI table, load
CREATE TABLE utah_air_quality_by_site (
CountyCode SMALLINT,
SiteNum SMALLINT,
lat FLOAT,
lon FLOAT,
AQSParameterDesc TEXT ENCODING DICT(32),
DateLocal DATE,
AQI FLOAT,
AQIDescription TEXT ENCODING DICT(32),
AQIColor TEXT ENCODING DICT(32));

copy utah_air_quality_by_site from '/home/mapdadmin/mapd-aqs/_out/*';

-- Get unique site locations
create table utah_aqi_sites as
select
sitenum,
min(lat) as lat,
min(lon) as lon
from utah_air_quality_by_site
group by 1;
