-- SQL script that ranks country origins of bands,
-- ordered by the number of (non-unique) fans
SELECT band_name, (IFNULL(split, '2022') - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;
