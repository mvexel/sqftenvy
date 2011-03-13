import psycopg2
import web

urls = (
	'/', 'index',
	'/(.+),(.+),(.+)', 'getavg'
)

application = web.application(urls, globals()).wsgifunc()

class index:
	def GET(self):
		return "usage: sqftenvy/lon,lat,radius"

class getavg:
	def GET(self,lon,lat,radius):
		lon=float(lon)
		lat=float(lat)
		radius=int(radius)
		if radius > 10000:
			return "max radius 10000"
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
		avg = c.fetchone()[0]
		return avg or 0

if __name__ == "__main__": app.run()