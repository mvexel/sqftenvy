sqftenvy
========

this service caclulates the average square metrage of apartments within a radius around a point.

currently this works for the small area that we got BAG data for at Hack De Overheid #3

Nudge me if you want the BAG extract shapefile used to fill the database (see below). You only need this if you want to play with the script and the data yourself. 

You can try the service live here:

	http://lima.schaaltreinen.nl/sqftenvy/4.89465,52.37346,150

db setup
--------

	create postgres database adressen and add postgis functions
	createdb adressen 
	createlang plpgsql adressen 
	psql -d adressen -f postgis.sql
	psql -d adressen -f spatial_ref_sys.sql

create the table in postgis:
	
	ogr2ogr -overwrite -s_srs EPSG:28992 -t_srs EPSG:4326 -f PostgreSQL PG:dbname=adressen adressen.shp
	
make sure you have web.py

	pip install web.py

usage
-----

host/sqftenvy/lon,lat,radius

lon: longitude in EPSG:4326
lat: latitude in EPSG:4326
radius: radius in meters

