FROM debezium/postgres:13

ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB mobi7_code_interview 

COPY postgresql.conf /home/config/ 
COPY initdb.sql /docker-entrypoint-initdb.d/