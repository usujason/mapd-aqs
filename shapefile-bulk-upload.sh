https://gis.utah.gov/data/cadastre/parcels/#UtahLIRParcels

#1. saved to utah_lir_shapefiles directory

$ ls -lrt utah_lir_shapefiles/
total 408688
-rw-rw-r-- 1 rzwitch rzwitch    954984 Jun  1 13:10 Parcels_Beaver_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   7183466 Jun  1 13:10 Parcels_BoxElder_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   9152777 Jun  1 13:10 Parcels_Cache_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   3279384 Jun  1 13:10 Parcels_Carbon_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch    356058 Jun  1 13:10 Parcels_Daggett_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch  18908413 Jun  1 13:10 Parcels_Davis_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   3900415 Jun  1 13:10 Parcels_Duchesne_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   2689950 Jun  1 13:10 Parcels_Garfield_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   2156109 Jun  1 13:10 Parcels_Grand_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   8107608 Jun  1 13:10 Parcels_Iron_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   1975537 Jun  1 13:10 Parcels_Juab_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   3273485 Jun  1 13:10 Parcels_Kane_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   2741403 Jun  1 13:10 Parcels_Millard_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   1110627 Jun  1 13:10 Parcels_Morgan_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   2970626 Jun  1 13:10 Parcels_Rich_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch 200183664 Jun  1 13:11 Parcels_SaltLake_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   1397522 Jun  1 13:11 Parcels_SanJuan_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   1576757 Jun  1 13:11 Parcels_Sanpete_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   7911261 Jun  1 13:11 Parcels_Summit_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   4480456 Jun  1 13:11 Parcels_Tooele_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch  69690149 Jun  1 13:11 Parcels_Utah_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch   5025674 Jun  1 13:11 Parcels_Wasatch_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch  35896908 Jun  1 13:11 Parcels_Washington_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch    298313 Jun  1 13:11 Parcels_Wayne_LIR.zip
-rw-rw-r-- 1 rzwitch rzwitch  23225130 Jun  1 13:11 Parcels_Weber_LIR.zip

#2. unzip all files into new directory
mkdir utah_lir_shapefiles_unzipped && unzip utah_lir_shapefiles/\*.zip -d utah_lir_shapefiles_unzipped

#3. Use -p mode to create table, but not load any data
shp2pgsql -I -s 4326 -p utah_lir_shapefiles_unzipped/Parcels_Beaver_LIR/Parcels_Beaver_LIR.shp utahlirparcels  | PGPASSWORD=<CHANGEME> psql -h localhost -U mapd gisdata;

#4. Load all the data using -a mode (append)
for i in $(find utah_lir_shapefiles_unzipped/ -type f -name '*.shp'); do 
  shp2pgsql -I -s 4326 -a $i utahlirparcels  | PGPASSWORD=<CHANGEME> psql -h localhost -U mapd gisdata; 
done;
