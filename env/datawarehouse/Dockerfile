FROM postgres:13

ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB mobi7_code_interview 

COPY ./initdb.sql \
     ./conf.sql /docker-entrypoint-initdb.d/

RUN chmod a+r /docker-entrypoint-initdb.d/conf.sql
RUN chmod a+r /docker-entrypoint-initdb.d/initdb.sql