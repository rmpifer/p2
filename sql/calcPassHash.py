import hashlib
import uuid

algorithm = 'sha512'

password = 'paulpass93'
salt = uuid.uuid4().hex

m = hashlib.new(algorithm)
m.update(salt + password)
password_hash = m.hexdigest()

print '$'.join([algorithm, salt, password_hash])

password = 'rebeccapass15'
salt = uuid.uuid4().hex

m = hashlib.new(algorithm)
m.update(salt + password)
password_hash = m.hexdigest()

print '$'.join([algorithm, salt, password_hash])

password = 'bob1pass'
salt = uuid.uuid4().hex

m = hashlib.new(algorithm)
m.update(salt + password)
password_hash = m.hexdigest()

print '$'.join([algorithm, salt, password_hash])