-- Select band name and calculate their lifespan based on the 'formed' and 'split' years
SELECT band_name, 
       CASE 
           -- If the band has not split, calculate lifespan as 2022 - formed
           WHEN split IS NULL THEN 2022 - formed
           -- If the band split, calculate lifespan as split - formed
           ELSE split - formed
       END AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;