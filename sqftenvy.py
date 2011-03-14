import psycopg2
import web
import simplejson as json

DEBUG=True

urls = (
	'/', 'index',
	'/(.+),(.+),(.+)', 'getavg'
)

if DEBUG:
	app = web.application(urls, globals())
else:
	app = web.application(urls, globals()).wsgifunc()	

class index:
	def GET(self):
		return "usage: sqftenvy/lon,lat,radius"

class getavg:
	def GET(self,lon,lat,radius):
		lon=float(lon)
		lat=float(lat)
		radius=int(radius)
		if radius > 500:
			return "max radius 500"
		SQL = """select avg(oppervlakt) from adressen where 
	ST_Within(
		wkb_geometry,
		transform(Buffer(transform(GeomFromText('POINT(%f %f)',4326),28992) ,%i), 4326)) 
	and gebruiksdo = 'woonfunctie' 
	and oppervlakt > 1;""" % (lon,lat,radius)
		conn = psycopg2.connect("dbname=adressen user=mvexel")
		c = conn.cursor()
		c.execute(SQL)
		conn.commit()
		avg = round(c.fetchone()[0], 2) or 0
		SQL = """select round(avg(bouwjaar)), count(*) from panden where 
	ST_Within(
		wkb_geometry,
		transform(Buffer(transform(GeomFromText('POINT(%f %f)',4326),28992) ,%i), 4326))
	and bouwjaar > 1100
	and bouwjaar < 2020
	;""" % (lon,lat,radius)
		c.execute(SQL)
		conn.commit()
		bouwjaar = int(c.fetchone()[0]) or 0
		return json.dumps({"avgsqm":avg,"avgyear":bouwjaar})

if __name__ == "__main__": app.run()