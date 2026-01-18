
SELECT *
FROM ciudad_region;


SELECT *
FROM fact_ventas as fv
INNER JOIN cursos as c
ON fv."CURSO_ID" = c."CURSO_ID"
WHERE c."CURSO" LIKE '%aux%';

-- Consulta para saber la cantidad de clientes entre fechas especificas date format "YYYY-MM-DD"
SELECT COUNT("CLIENTE_ID")
FROM fact_ventas
WHERE "FECHA_DE_VENTA" BETWEEN '2025-01-01' AND '2025-12-31';
