from db.sql import db, Server, Cluster, User, File

print('DB initialization started...')
print('Starting creating servers...')
# Servers
server1 = Server(status=False, updated=True, address='188.130.155.44')
server2 = Server(status=False, updated=True, address='188.130.155.48')
server3 = Server(status=False, updated=True, address='188.130.155.44')
server4 = Server(status=False, updated=True, address='127.0.0.4')
server5 = Server(status=False, updated=True, address='127.0.0.5')
server6 = Server(status=False, updated=True, address='127.0.0.6')
print('Starting creating clusters...')
# Clusters
cluster1 = Cluster(main=1, second1=2, second2=3)
cluster2 = Cluster(main=4, second1=5, second2=6)
print('Starting creating users...')
# Users
# user1 = User(alias='user1', password='pass1', cluster=1, port=8020, size=0, description=' ')

print('Starting creating files...')
# Files
# file1 = File(name='/user1/kek', size=0, user_id=1)

print('Drop database...')
db.drop_all()
print('Create new tables...')
db.create_all()
db.session.add(server1)
db.session.add(server2)
db.session.add(server3)
db.session.add(server4)
db.session.add(server5)
db.session.add(server6)
db.session.add(cluster1)
db.session.add(cluster2)
# db.session.add(user1)
# db.session.add(file1)
print('Upload DB to Amazon...')
db.session.commit()
print('DB successfully created!!!')
