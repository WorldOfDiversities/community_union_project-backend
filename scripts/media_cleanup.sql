-- Media cleanup queries for stale Supabase references.
-- Broken filenames provided by the user:
-- 1000517791.jpg
-- 1000528991.jpg
-- 1000523574.jpg
-- 1000531260.jpg
-- 1000517468.jpg

-- 1) Locate broken references across the known media tables.
WITH broken_names(name) AS (
    VALUES
        ('1000517791.jpg'),
        ('1000528991.jpg'),
        ('1000523574.jpg'),
        ('1000531260.jpg'),
        ('1000517468.jpg')
)
SELECT 'gallery_media' AS table_name, id::text AS record_id, title, media_file::text AS media_ref
FROM gallery_media
WHERE EXISTS (
    SELECT 1
    FROM broken_names b
    WHERE media_file::text ILIKE '%' || b.name || '%'
)
   OR media_file::text ILIKE '%/storage/v1/s3/%'
   OR media_file::text ILIKE '%/storage/v1/object/public/%'
   OR media_file::text ILIKE '%old-bucket%'
UNION ALL
SELECT 'accounts_user', id::text, email, avatar_url
FROM accounts_user
WHERE EXISTS (
    SELECT 1
    FROM broken_names b
    WHERE COALESCE(avatar_url, '') ILIKE '%' || b.name || '%'
)
   OR COALESCE(avatar_url, '') ILIKE '%/storage/v1/%'
   OR COALESCE(avatar_url, '') ILIKE '%old-bucket%'
UNION ALL
SELECT 'organizationsettings', id::text, union_name, COALESCE(logo::text, '')
FROM settings_organizationsettings
WHERE COALESCE(logo::text, '') ILIKE ANY (ARRAY['%1000517791.jpg%','%1000528991.jpg%','%1000523574.jpg%','%1000531260.jpg%','%1000517468.jpg%'])
   OR COALESCE(logo::text, '') ILIKE '%/storage/v1/%'
   OR COALESCE(logo::text, '') ILIKE '%old-bucket%'
UNION ALL
SELECT 'meetings_meeting', meeting_id::text, title, image_url
FROM meetings_meeting
WHERE COALESCE(image_url, '') ILIKE ANY (ARRAY['%1000517791.jpg%','%1000528991.jpg%','%1000523574.jpg%','%1000531260.jpg%','%1000517468.jpg%'])
   OR COALESCE(image_url, '') ILIKE '%/storage/v1/%'
   OR COALESCE(image_url, '') ILIKE '%old-bucket%';

-- 2) Nullify / clear broken references while preserving valid records.
-- gallery_media.media_file is non-null in the model, so clear it to an empty string.
UPDATE gallery_media
SET media_file = ''
WHERE media_file::text ILIKE ANY (ARRAY[
    '%1000517791.jpg%',
    '%1000528991.jpg%',
    '%1000523574.jpg%',
    '%1000531260.jpg%',
    '%1000517468.jpg%',
    '%/storage/v1/s3/%',
    '%old-bucket%'
]);

UPDATE accounts_user
SET avatar_url = NULL
WHERE COALESCE(avatar_url, '') ILIKE ANY (ARRAY[
    '%1000517791.jpg%',
    '%1000528991.jpg%',
    '%1000523574.jpg%',
    '%1000531260.jpg%',
    '%1000517468.jpg%',
    '%/storage/v1/%',
    '%old-bucket%'
]);

UPDATE settings_organizationsettings
SET logo = NULL
WHERE COALESCE(logo::text, '') ILIKE ANY (ARRAY[
    '%1000517791.jpg%',
    '%1000528991.jpg%',
    '%1000523574.jpg%',
    '%1000531260.jpg%',
    '%1000517468.jpg%',
    '%/storage/v1/%',
    '%old-bucket%'
]);

UPDATE meetings_meeting
SET has_image = FALSE,
    image_url = ''
WHERE COALESCE(image_url, '') ILIKE ANY (ARRAY[
    '%1000517791.jpg%',
    '%1000528991.jpg%',
    '%1000523574.jpg%',
    '%1000531260.jpg%',
    '%1000517468.jpg%',
    '%/storage/v1/%',
    '%old-bucket%'
]);

-- 3) Identify duplicate image URLs/paths.
SELECT image_url, COUNT(*)
FROM meetings_meeting
WHERE COALESCE(image_url, '') <> ''
GROUP BY image_url
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC, image_url;

SELECT avatar_url, COUNT(*)
FROM accounts_user
WHERE COALESCE(avatar_url, '') <> ''
GROUP BY avatar_url
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC, avatar_url;

-- 4) Optional bucket migration examples.
-- Replace old bucket references with the current public bucket host/path.
-- UPDATE gallery_media
-- SET media_file = REPLACE(media_file::text, 'old-bucket-name', 'AWS_STORAGE_BUCKET_NAME')
-- WHERE media_file::text ILIKE '%old-bucket-name%';

-- UPDATE accounts_user
-- SET avatar_url = REPLACE(avatar_url, 'old-bucket-name', 'AWS_STORAGE_BUCKET_NAME')
-- WHERE COALESCE(avatar_url, '') ILIKE '%old-bucket-name%';
