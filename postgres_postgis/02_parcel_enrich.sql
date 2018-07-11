create table utahlirparcels_with_keys as
select
parcels.gid,
upper(county_nam) as county_name,
county_id,
current_as,
parcel_id,
serial_num,
upper(parcel_add) as parcel_add,
upper(parcel_cit) as parcel_city,
upper(taxexempt_) as taxexempt,
tax_distri as tax_district,
cast(total_mkt_ as bigint) as total_mkt_value,
cast(land_mkt_v as bigint) as land_mkt_value,
parcel_acr as parcel_acreage,
prop_class as property_class,
primary_re as primary_residence,
cast(house_cnt as int) as house_cnt,
upper(subdiv_nam) as subdiv_name,
bldg_sqft,
floors_cnt,
built_yr,
effbuilt_y as effbuilt_yr,
upper(const_mate) as const_material,
shape_leng as shape_length,
shape_area,
geom4326,
closest.stationkey as stationkey_closest,
closest.distance_km as stationkey_closest_distance_km,
par10.stationkey as stationkey_pm10,
par10.distance_km as stationkey_pm25_km,
oz.stationkey as stationkey_ozone,
oz.distance_km as stationkey_ozone_km,
co.stationkey as stationkey_co,
co.distance_km as stationkey_co_km,
no2.stationkey as stationkey_no2,
no2.distance_km as stationkey_no2_km,
pm2pt5.stationkey as stationkey_pm2pt5,
pm2pt5.distance_km as stationkey_pm2pt5_km,
so2.stationkey as stationkey_so2,
so2.distance_km as stationkey_so2_km
from utahlirparcels as parcels
left join closest_aqi_overall as closest on (parcels.gid = closest.gid)
left join closest_aqi_particulatematter0_10 as par10 on (parcels.gid = par10.gid)
left join closest_aqi_ozone as oz on (parcels.gid = oz.gid)
left join closest_aqi_carbonmonoxide as co on (parcels.gid = co.gid)
left join closest_aqi_nitrogendioxide as no2 on (parcels.gid = no2.gid)
left join closest_aqi_particulatematter2pt5 as pm2pt5 on (parcels.gid = pm2pt5.gid)
left join closest_aqi_sulferdioxide as so2 on (parcels.gid = so2.gid);
