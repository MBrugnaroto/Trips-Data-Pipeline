CONSUMER_GET_STATISTICS = \
    """
    SELECT 
        vehicle_id, 
        COUNT(vehicle_id) AS total_viagens,
        SUM(total_distance) AS total_km,
        SUM(total_moving)/3600::float AS total_mv_h,
        SUM(total_idle)/3600::float AS total_pd_h
    FROM trip
    GROUP BY vehicle_id
    """

CONSUMER_INSERT_STATISTICS = \
    """
    INSERT INTO {table}({columns}) 
    VALUES %s
    """