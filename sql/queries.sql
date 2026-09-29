-- 1. Pacientes con al menos un tratamiento activo

SELECT DISTINCT
    p.id,
    p.identification,
    p.first_name,
    p.last_name
FROM patients_patient AS p
INNER JOIN patients_treatment AS t
    ON t.patient_id = p.id
WHERE t.status = 'active';


-- 2. Pacientes que nunca han tenido tratamientos

SELECT
    p.id,
    p.identification,
    p.first_name,
    p.last_name
FROM patients_patient AS p
LEFT JOIN patients_treatment AS t
    ON t.patient_id = p.id
WHERE t.id IS NULL;


-- 3. Cantidad de tratamientos por paciente

SELECT
    p.id,
    p.identification,
    p.first_name,
    p.last_name,
    COUNT(t.id) AS treatment_count
FROM patients_patient AS p
LEFT JOIN patients_treatment AS t
    ON t.patient_id = p.id
GROUP BY
    p.id,
    p.identification,
    p.first_name,
    p.last_name
ORDER BY treatment_count DESC;


-- 4. Tratamiento más reciente de cada paciente
-- Criterio: mayor start_date

WITH ranked_treatments AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.patient_id
            ORDER BY t.start_date DESC, t.id DESC
        ) AS position
    FROM patients_treatment AS t
)
SELECT
    p.id AS patient_id,
    p.first_name,
    p.last_name,
    rt.id AS treatment_id,
    rt.name,
    rt.start_date,
    rt.end_date,
    rt.status
FROM patients_patient AS p
INNER JOIN ranked_treatments AS rt
    ON rt.patient_id = p.id
WHERE rt.position = 1;


-- 5. Los 10 pacientes con mayor cantidad de tratamientos

SELECT
    p.id,
    p.identification,
    p.first_name,
    p.last_name,
    COUNT(t.id) AS treatment_count
FROM patients_patient AS p
LEFT JOIN patients_treatment AS t
    ON t.patient_id = p.id
GROUP BY
    p.id,
    p.identification,
    p.first_name,
    p.last_name
ORDER BY treatment_count DESC
LIMIT 10;