-- Lists all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name, ((CASE WHEN split IS NULL THEN 2022 ELSE split END) - formed) AS lifespan 
FROM metal_bands 
WHERE style LIKE '%Glam rock%'
ORDER BY
CASE WHEN ((CASE WHEN split IS NULL THEN 2022 ELSE split END) - formed) != 0
	THEN lifespan
	ELSE 0
END DESC,
band_name DESC;

