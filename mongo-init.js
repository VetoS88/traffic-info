print('Creating collection and user/pwd')

db = db.getSiblingDB('traffic');
db.createCollection('traffic');
db.createUser(
  {
    user: 'user',
    pwd: 'password',
    roles: [{ role: 'readWrite', db: 'traffic' }],
  },
);
print('user/paswd and collection created')