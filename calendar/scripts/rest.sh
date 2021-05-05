curl -X POST http://localhost:8000/api-token-auth/ -d 'username=f&password=f'

curl http://localhost:8000/api/bots/  -H 'Authorization: Token '$MITRON_AUTH_TOKEN
curl -X POST http://localhost:8000/bots/ -d 'name=m10'


curl -X POST http://localhost:8000/bots/ -d 'name=m1' -H 'Authorization: Token 39b24539d43fa2451b40911c80f67d9cd359e1a3'

curl -X GET http://localhost:8000/users/ -d 'face_id=bar' -H 'Authorization: Token abb7ba8ea1f20fba453e279d5530d6de98dd4a8a'
curl -X POST http://localhost:8000/users/ -d 'name=foo&face_id=bar&face_id_source=2' -H 'Authorization: Token 794ee1f32672254b0de8a8b87c583c8c'

curl -X PATCH http://localhost:8000/users/bvis/ -d 'name=balajiv' -H 'Authorization: Token 794ee1f32672254b0de8a8b87c583c8ccbf929db'
curl -X PATCH http://localhost/users/bvis/ -d 'name=balajiv' -H 'Authorization: Token 794ee1f32672254b0de8a8b87c583c8ccbf929db'


# mitrausers
cag http://localhost:8000/api/mitrausers/
cap http://localhost:8000/api/mitrausers/ -d 'name=baz&face_id_source=2&face_id=29'
capa http://localhost:8000/api/mitrausers/2/ -d 'company=21'


# logs
cag http://localhost:8000/api/logs/
cap http://localhost:8000/api/logs/ -d 'data={"a": 2}'
