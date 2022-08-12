CREATE TABLE public.consumer_statistics(
	vehicle_id INT NOT NULL,
    total_trips INT,
    total_distance FLOAT,
    total_moving FLOAT,
    total_idle FLOAT,
    ref_month VARCHAR DEFAULT TO_CHAR(CURRENT_TIMESTAMP,'MM-YYYY') NOT NULL
);

ALTER TABLE public.consumer_statistics 
ADD CONSTRAINT id_consumer_statistics_pk 
PRIMARY KEY (vehicle_id, ref_month);