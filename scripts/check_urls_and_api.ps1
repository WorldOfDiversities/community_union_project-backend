& .\scripts\check_urls.ps1

Write-Output ""
Write-Output "Fetching backend gallery API..."
try {
    $r = Invoke-WebRequest -Uri 'https://community-union-project-backend-1.onrender.com/api/v1/gallery/' -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
    $json = $r.Content | ConvertFrom-Json
    if ($json -and $json.Count -gt 0) {
        $first = $json[0]
        Write-Output 'First item media_url:'
        if ($first.media_url) { Write-Output $first.media_url } else { Write-Output 'null' }
    } else {
        Write-Output 'No gallery items returned'
    }
} catch {
    Write-Output ('ERROR: ' + $_.Exception.Message)
}
