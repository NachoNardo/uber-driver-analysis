CREATE TABLE travels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    total_value NUMERIC(10,2) NOT NULL,

    street_start TEXT NOT NULL,
    neiborghood_start TEXT NOT NULL,

    street_end TEXT NOT NULL,
    neiborghood_end TEXT NOT NULL,

    distance_start REAL NOT NULL,
    distance_travel REAL NOT NULL,

    time_start DATETIME NOT NULL,
    time_reach DATETIME NOT NULL,
    time_end DATETIME NOT NULL,

    time_total INTEGER NOT NULL
);
