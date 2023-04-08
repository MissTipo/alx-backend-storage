-- lists all bands with Glam rock as their main style
-- ranked by their longevity
SELECT band_name, (COALESCE(split, 2022) - formed) AS lifespan 
FROM metal_bands 
WHERE style LIKE '%Glam rock%'
ORDER BY
CASE WHEN (COALESCE(split, 2022) - formed) != 0
  THEN lifespan
  ELSE 0
END DESC,
band_name DESC;

