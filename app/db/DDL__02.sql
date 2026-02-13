CREATE TABLE refills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    value NUMERIC(10,2) NOT NULL,

    liters REAL NOT NULL,

    current_distance_traveled REAL NOT NULL
);
