#! /bin/bash

set -x

# auth
http -f post :8000/api-token-auth/ username=f password=f


# customers
http :8000/customers/
http -f POST :8000/customers/ name=foo faceid=bar


# bots
http GET :8000/bots


# songs
http -f post :8000/songs/ username=f password=f


# commands
h -f post :8000/mitra/commands/ 'Authorization: Token foo' type=2 name=2
