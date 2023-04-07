-- lists all bands with Glam rock as their main style
SELECT band_name, 
  TIMESTAMPDIFF(YEAR, STR_TO_DATE(split, '%Y-%m-%d'), STR_TO_DATE(formed, '%Y-%m-%d')) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
