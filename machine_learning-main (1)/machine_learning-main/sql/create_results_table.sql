CREATE TABLE IF NOT EXISTS clustering_results (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    n_clusters INTEGER NOT NULL,
    used_iterations INTEGER NOT NULL,
    coordinates FLOAT8[] NOT NULL,
    assigned_cluster INTEGER NOT NULL,
    is_centroid BOOLEAN NOT NULL,
    centroid_label TEXT
);