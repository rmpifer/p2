import hashlib
import os
import uuid





sequenceNum = 0;

albumid = 1
filenames = ['sports_s1.jpg', 'sports_s2.jpg','sports_s3.jpg','sports_s4.jpg',
'sports_s5.jpg', 'sports_s6.jpg','sports_s7.jpg','sports_s8.jpg'] 
for x in filenames:
	m = hashlib.md5()
	m.update(str(albumid))
	m.update(x)
	print "INSERT INTO Photo (picID, format) VALUES (\'" + m.hexdigest() + "\', \'jpg\');"
	print "INSERT INTO Contain (sequenceNum, albumID, picID, caption)"
	print "VALUES (" + str(sequenceNum) + "," + str(albumid) + ",\'" + m.hexdigest() + "\', \'\');"
	os.rename(x, m.hexdigest()+".jpg")
	sequenceNum +=1


albumid = 2
filenames = ['football_s1.jpg', 'football_s2.jpg','football_s3.jpg','football_s4.jpg'] 
for x in filenames:
	m = hashlib.md5()
	m.update(str(albumid))
	m.update(x)
	print "INSERT INTO Photo (picID, format) VALUES (\'" + m.hexdigest() + "\', \'jpg\');"
	print "INSERT INTO Contain (sequenceNum, albumID, picID, caption)"
	print "VALUES (" + str(sequenceNum) + "," + str(albumid) + ",\'" + m.hexdigest() + "\', \'\');"
	os.rename(x, m.hexdigest()+".jpg")
	sequenceNum +=1



albumid = 3
filenames = ['world_EiffelTower.jpg', 'world_firenze.jpg', 'world_GreatWall.jpg', 'world_Isfahan.jpg', 
'world_Istanbul.jpg', 'world_Persepolis.jpg', 'world_Reykjavik.jpg', 'world_Seoul.jpg',
'world_Stonehenge.jpg', 'world_TajMahal.jpg', 'world_TelAviv.jpg', 'world_tokyo.jpg', 'world_WashingtonDC.jpg']
for x in filenames:
	m = hashlib.md5()
	m.update(str(albumid))
	m.update(x)
	print "INSERT INTO Photo (picID, format) VALUES (\'" + m.hexdigest() + "\', \'jpg\');"
	print "INSERT INTO Contain (sequenceNum, albumID, picID, caption)"
	print "VALUES (" + str(sequenceNum) + "," + str(albumid) + ",\'" + m.hexdigest() + "\', \'\');"
	os.rename(x, m.hexdigest()+".jpg")
	sequenceNum +=1


albumid = 4
filenames = ['space_EagleNebula.jpg', 'space_GalaxyCollision.jpg','space_HelixNebula.jpg',
'space_MilkyWay.jpg', 'space_OrionNebula.jpg']
for x in filenames:
	m = hashlib.md5()
	m.update(str(albumid))
	m.update(x)
	print "INSERT INTO Photo (picID, format) VALUES (\'" + m.hexdigest() + "\', \'jpg\');"
	print "INSERT INTO Contain (sequenceNum, albumID, picID, caption)"
	print "VALUES (" + str(sequenceNum) + "," + str(albumid) + ",\'" + m.hexdigest() + "\', \'\');"
	os.rename(x, m.hexdigest()+".jpg")
	sequenceNum +=1
