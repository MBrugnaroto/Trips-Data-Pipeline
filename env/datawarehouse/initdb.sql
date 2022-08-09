CREATE TABLE public.consumer_statistics(
	vehicle_id INT NOT NULL,
    total_viagens INT,
    total_km FLOAT,
    total_mv_h FLOAT,
    total_pd_h FLOAT,
    ref_month VARCHAR DEFAULT TO_CHAR(CURRENT_TIMESTAMP,'MM-YYYY') NOT NULL
);

ALTER TABLE public.consumer_statistics 
ADD CONSTRAINT id_consumer_statistics_pk 
PRIMARY KEY (vehicle_id, ref_month);