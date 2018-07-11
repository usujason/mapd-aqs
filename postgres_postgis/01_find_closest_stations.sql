--merge those within 200km, then get closest
--even 200km might not even make performance difference
create table closest_aqi_overall as
select
*
from
(with parcels as (select gid, geom4326 from utahlirparcels)
SELECT
parcels.gid,
points.stationkey,
ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)/1000 as distance_km,
row_number() over (partition by gid order by ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)) as station_rank
FROM parcels
inner join aqistations as points ON ST_DWithin(parcels.geom4326::geography, points.aqi_pgis_point::geography, 200000)) innert
where station_rank = 1;

create table closest_aqi_particulatematter0_10 as
select
*
from
(with parcels as (select gid, geom4326 from utahlirparcels)
SELECT
parcels.gid,
points.stationkey,
ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)/1000 as distance_km,
row_number() over (partition by gid order by ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)) as station_rank
FROM parcels
inner join aqistations as points ON ST_DWithin(parcels.geom4326::geography, points.aqi_pgis_point::geography, 200000)
where particulatematter0_10 = 1) innert
where station_rank = 1;

create table closest_aqi_ozone as
select
*
from
(with parcels as (select gid, geom4326 from utahlirparcels)
SELECT
parcels.gid,
points.stationkey,
ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)/1000 as distance_km,
row_number() over (partition by gid order by ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)) as station_rank
FROM parcels
inner join aqistations as points ON ST_DWithin(parcels.geom4326::geography, points.aqi_pgis_point::geography, 200000)
where ozone = 1) innert
where station_rank = 1;

create table closest_aqi_carbonmonoxide as
select
*
from
(with parcels as (select gid, geom4326 from utahlirparcels)
SELECT
parcels.gid,
points.stationkey,
ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)/1000 as distance_km,
row_number() over (partition by gid order by ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)) as station_rank
FROM parcels
inner join aqistations as points ON ST_DWithin(parcels.geom4326::geography, points.aqi_pgis_point::geography, 200000)
where carbonmonoxide = 1) innert
where station_rank = 1;

create table closest_aqi_nitrogendioxide as
select
*
from
(with parcels as (select gid, geom4326 from utahlirparcels)
SELECT
parcels.gid,
points.stationkey,
ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)/1000 as distance_km,
row_number() over (partition by gid order by ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)) as station_rank
FROM parcels
inner join aqistations as points ON ST_DWithin(parcels.geom4326::geography, points.aqi_pgis_point::geography, 200000)
where nitrogendioxide = 1) innert
where station_rank = 1;

create table closest_aqi_particulatematter2pt5 as
select
*
from
(with parcels as (select gid, geom4326 from utahlirparcels)
SELECT
parcels.gid,
points.stationkey,
ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)/1000 as distance_km,
row_number() over (partition by gid order by ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)) as station_rank
FROM parcels
inner join aqistations as points ON ST_DWithin(parcels.geom4326::geography, points.aqi_pgis_point::geography, 200000)
where particulatematter2pt5 = 1) innert
where station_rank = 1;

create table closest_aqi_sulferdioxide as
select
*
from
(with parcels as (select gid, geom4326 from utahlirparcels)
SELECT
parcels.gid,
points.stationkey,
ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)/1000 as distance_km,
row_number() over (partition by gid order by ST_Distance(parcels.geom4326::geography, points.aqi_pgis_point::geography)) as station_rank
FROM parcels
inner join aqistations as points ON ST_DWithin(parcels.geom4326::geography, points.aqi_pgis_point::geography, 200000)
where sulferdioxide = 1) innert
where station_rank = 1;
