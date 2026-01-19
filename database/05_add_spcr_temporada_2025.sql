-- Adds SPCR Temporada 2025 season with fixed id = 1
-- Safe to run multiple times (no-op if already present)

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM seasons WHERE id = 1) THEN
        INSERT INTO seasons (id, name, start_date, end_date, description)
        VALUES (
            1,
            'SPCR Temporada 2025',
            '2025-01-01',
            '2025-12-31',
            'SPCR Temporada 2025 season'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM seasons WHERE id = 2) THEN
        INSERT INTO seasons (id, name, start_date, end_date, description)
        VALUES (
            2,
            'SPCR Temporada 2026',
            '2026-01-01',
            '2026-12-31',
            'SPCR Temporada 2026 season'
        );
    END IF;

    -- Ensure the sequence is ahead of the max id
    PERFORM setval('seasons_id_seq', (SELECT GREATEST(COALESCE(MAX(id), 0), nextval('seasons_id_seq')) FROM seasons));
END $$;
