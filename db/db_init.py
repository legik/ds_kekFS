from db.sql import db, Server, Cluster, User, File

print('DB initialization started...')
print('Starting creating servers...')
# Servers
server1 = Server(status=True, updated=True, address='188.130.155.44')
server2 = Server(status=True, updated=True, address='188.130.155.48')
server3 = Server(status=True, updated=True, address='188.130.155.48')
print('Starting creating clusters...')
# Clusters
cluster1 = Cluster(main=1, second1=2, second2=3)

print('Drop database...')
db.drop_all()
print('Create new tables...')
db.create_all()
db.session.add(server1)
db.session.add(server2)
db.session.add(server3)
db.session.add(cluster1)
print('Upload DB to Amazon...')
db.session.commit()
print('DB successfully created!!!')
