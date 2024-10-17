-- Select the band name and calculate their lifespan (years until 2022)
SELECT band_name, 
       CASE 
           WHEN split IS NULL THEN (2022 - formed)
           ELSE (split - formed)
       END AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
