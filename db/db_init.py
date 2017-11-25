from db.sql import db, Server, Cluster, User, File


print('DB initialization started...')
print('Starting creating servers...')
# Servers
server1 = Server(status=True, address='127.0.0.1')
server2 = Server(status=True, address='127.0.0.2')
server3 = Server(status=True, address='127.0.0.3')
server4 = Server(status=True, address='127.0.0.4')
server5 = Server(status=True, address='127.0.0.5')
server6 = Server(status=True, address='127.0.0.6')
print('Starting creating clusters...')
# Clusters
cluster1 = Cluster(main=1, second1=2, second2=3)
cluster2 = Cluster(main=4, second1=5, second2=6)
print('Starting creating users...')
# Users
user1 = User(alias='user1', password='pass1', cluster=1, port=8020, size=2000)
user2 = User(alias='user2', password='pass1', cluster=1, port=8021, size=2000)
user3 = User(alias='user3', password='pass1', cluster=1, port=8022, size=2000)
user4 = User(alias='user4', password='pass1', cluster=1, port=8023, size=2000)
user5 = User(alias='user5', password='pass1', cluster=1, port=8024, size=2000)
print('Starting creating files...')
# Files
file1 = File(name='/user1/kek', size=10, user_id=1)
file2 = File(name='/user2/kek', size=10, user_id=2)
file3 = File(name='/user1/kek1', size=10, user_id=1)
file4 = File(name='/user1/kekdir/', size=10, user_id=1)
file5 = File(name='/user1/kekdir/kek1', size=10, user_id=1)
file6 = File(name='/user1/kekdir/kek2', size=10, user_id=1)

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
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)
db.session.add(file1)
db.session.add(file2)
db.session.add(file3)
db.session.add(file4)
db.session.add(file5)
print('Upload DB to Amazon...')
db.session.commit()
print('DB successfully created!!!')

