-- Select the band name and calculate their lifespan (years until 2022)
SELECT band_name, 
       CASE 
           -- If 'split' is null, the band is still active, so use 2022 as the end year
           WHEN split IS NULL THEN 2022 - formed
           -- If the 'split' year is 0, the band did not split, treat as active
           WHEN split = 0 THEN 2022 - formed
           -- Otherwise, calculate lifespan as 'split' year minus 'formed' year
           ELSE split - formed
       END AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;