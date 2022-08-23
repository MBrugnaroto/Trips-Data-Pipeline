CREATE TABLE public.consumer_statistics(
	vehicle_id VARCHAR NOT NULL,
    total_trips INT,
    total_distance FLOAT,
    total_moving FLOAT,
    total_idle FLOAT,
    ref_month TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

ALTER TABLE public.consumer_statistics 
ADD CONSTRAINT id_consumer_statistics_pk 
PRIMARY KEY (vehicle_id, ref_month);