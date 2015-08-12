frodo
=====

generic locking blocking engine
------------
motivation: never saw getting this problem solved right
use cases: flight, kino, train... tickets, hotel rooms, sth like that - limited resource in time
way: simple, it has to be done on db level, using constraints - not updates, count(1) etc.
implementation: with postgresql >= 9.2 (tsrange used)
api: simple REST
performance: greater then You need

setup service
------------
...

REST API
------------
...

running tests
------------
from the same directory as README run:

python -m unittest frodo.test.test_plain
