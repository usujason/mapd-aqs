-- Picks the closest distance from cartesian standpoint
-- This isn't necessarily the best air quality sensor to use, if mountains block area
-- or other natural phenomenon

create table utahparcelsaqi as
select
a.*,
(select sitenum from utah_aqi_sites limit 1) as pickup_building
from utahlirparcels as a;
