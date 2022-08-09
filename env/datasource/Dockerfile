FROM debezium/postgres:13

ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB mobi7_code_interview 

COPY env/datasource/postgresql.conf /home/config/ 
COPY env/datasource/initdb.sql /docker-entrypoint-initdb.d/