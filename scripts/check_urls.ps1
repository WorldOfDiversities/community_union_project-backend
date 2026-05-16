$urls = @(
 'https://ncdlncqapgcoqaqriebv.supabase.co/storage/v1/object/public/AWS_STORAGE_BUCKET_NAME/gallery/2026/05/16/1000528991.jpg',
 'https://ncdlncqapgcoqaqriebv.supabase.co/storage/v1/s3/AWS_STORAGE_BUCKET_NAME/gallery/2026/05/16/1000528991.jpg',
 'https://community-union-project-backend-1.onrender.com/media/gallery/2026/05/16/1000528991.jpg'
)

foreach ($u in $urls) {
    Write-Output "--- $u ---"
    try {
        $r = Invoke-WebRequest -Uri $u -Method Head -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
        Write-Output "Status: $($r.StatusCode)"
        if ($r.Headers['Content-Type']) { Write-Output "Content-Type: $($r.Headers['Content-Type'])" }
        if ($r.Headers['Content-Length']) { Write-Output "Content-Length: $($r.Headers['Content-Length'])" }
    } catch {
        Write-Output "ERROR: $($_.Exception.Message)"
    }
}
