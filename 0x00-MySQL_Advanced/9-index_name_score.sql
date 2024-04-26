-- SQL script that creates an index on two tables.
CREATE INDEX idx_name_first_score ON names(name(1), score);
