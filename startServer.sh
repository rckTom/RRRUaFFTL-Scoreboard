#!bin/sh -
uwsgi --socket /home/rrruafttl/RRRUaFTTLScoreboard/com.sock --chdir /home/rrruafttl/RRRUaFTTLScoreboard --module RRRUaFTTL.wsgi --chmod-socket=666
