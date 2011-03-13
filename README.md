sqftenvy
========

this service caclulates the average square metrage of apartments within a radius around a point.

email me for the BAG extract used by this service: m@rtijn.org

db setup
--------

	create postgres database adressen and add postgis functions
	createdb adressen 
	createlang plpgsql adressen 
	psql -d adressen -f postgis.sql
	psql -d adressen -f spatial_ref_sys.sql

create the table in postgis:
	
	ogr2ogr -overwrite -s_srs EPSG:28992 -t_srs EPSG:4326 -f PostgreSQL PG:dbname=adressen adressen.shp
