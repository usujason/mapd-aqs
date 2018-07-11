--shapefiles loaded into table utahlirparcels by shapefile shell script
shp2pgsql -I -s 26912 -p utah_lir_shapefiles_unzipped/Parcels_Beaver_LIR/Parcels_Beaver_LIR.shp \
utahlirparcels  | PGPASSWORD='password' psql -h localhost -U user gisdata;

for i in $(find utah_lir_shapefiles_unzipped/ -type f -name '*.shp'); do
  shp2pgsql -I -s 26912 -a $i utahlirparcels  | PGPASSWORD='password' psql -h localhost -U user gisdata;
done;

--switch to 4326, works well with other lat/lon data
alter table utahlirparcels add column geom4326 geometry(multipolygon, 4326);
update utahlirparcels set geom4326 = ST_TRANSFORM(geom,4326);

--create weather table, upload
create table utahdailyweather(
countycode int,
sitenum int,
latitude float,
longitude float,
aqs_parameter_desc varchar,
date_local date,
aqi float,
aqi_description varchar,
aqi_color varchar
);

\copy utahdailyweather from '/home/rzwitch/dailyweather.csv' DELIMITER ',' CSV HEADER;

--see if records are duplicated
--not enough to make a difference
create table utahweatherduplicatecheck as
select
countycode,
sitenum,
latitude,
longitude,
aqs_parameter_desc,
date_local,
aqi,
aqi_description,
aqi_color,
rank() over (partition by countycode, sitenum, aqs_parameter_desc, date_local order by aqi desc) as record_dedup
from utahdailyweather;

--transpose table
create table utahweathertransposed as
select
countycode,
sitenum,
latitude,
longitude,
date_local,
max(case when aqs_parameter_desc = 'PM10 Total 0-10um STP' then aqi end) as aqi_particulatematter0_10,
max(case when aqs_parameter_desc = 'PM10 Total 0-10um STP' then aqi_description end) as aqi_desc_particulatematter0_10,
max(case when aqs_parameter_desc = 'PM10 Total 0-10um STP' then aqi_color end) as aqi_color_aqi_particulatematter0_10,
max(case when aqs_parameter_desc = 'Ozone' then aqi end) as aqi_ozone,
max(case when aqs_parameter_desc = 'Ozone' then aqi_description end) as aqi_desc_ozone,
max(case when aqs_parameter_desc = 'Ozone' then aqi_color end) as aqi_color_ozone,
max(case when aqs_parameter_desc = 'Carbon monoxide' then aqi end) as aqi_carbonmonoxide,
max(case when aqs_parameter_desc = 'Carbon monoxide' then aqi_description end) as aqi_desc_carbonmonoxide,
max(case when aqs_parameter_desc = 'Carbon monoxide' then aqi_color end) as aqi_color_carbonmonoxide,
max(case when aqs_parameter_desc = 'Nitrogen dioxide (NO2)' then aqi end) as aqi_nitrogendioxide,
max(case when aqs_parameter_desc = 'Nitrogen dioxide (NO2)' then aqi_description end) as aqi_desc_nitrogendioxide,
max(case when aqs_parameter_desc = 'Nitrogen dioxide (NO2)' then aqi_color end) as aqi_color_nitrogendioxide,
max(case when aqs_parameter_desc = 'PM2.5 - Local Conditions' then aqi end) as aqi_particulatematter2pt5,
max(case when aqs_parameter_desc = 'PM2.5 - Local Conditions' then aqi_description end) as aqi_desc_particulatematter2pt5,
max(case when aqs_parameter_desc = 'PM2.5 - Local Conditions' then aqi_color end) as aqi_color_particulatematter2pt5,
max(case when aqs_parameter_desc = 'Sulfur dioxide' then aqi end) as aqi_sulferdioxide,
max(case when aqs_parameter_desc = 'Sulfur dioxide' then aqi_description end) as aqi_desc_sulferdioxide,
max(case when aqs_parameter_desc = 'Sulfur dioxide' then aqi_color end) as aqi_color_sulferdioxide
from utahweatherduplicatecheck
where record_dedup = 1
group by 1,2,3,4,5

--create table of stations, make pseudo primary/match key
create table aqistations as
select
innert.*,
ST_SetSRID(ST_Point(longitude, latitude),4326) as aqi_pgis_point
from
(select
row_number() over() as stationkey,
countycode,
sitenum,
latitude,
longitude,
max(case when aqi_particulatematter0_10 is not null then 1 else 0 end) as particulatematter0_10,
max(case when aqi_ozone is not null then 1 else 0 end) as ozone,
max(case when aqi_carbonmonoxide is not null then 1 else 0 end) as carbonmonoxide,
max(case when aqi_nitrogendioxide is not null then 1 else 0 end) as nitrogendioxide,
max(case when aqi_particulatematter2pt5 is not null then 1 else 0 end) as particulatematter2pt5,
max(case when aqi_sulferdioxide is not null then 1 else 0 end) as sulferdioxide
from utahweathertransposed
group by 2,3,4,5) as innert;
