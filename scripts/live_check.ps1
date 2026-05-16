$base='https://community-union-project-backend-1.onrender.com'
$creds = @{ email='karim@gmail.com'; password='karim1234' }
try {
    Write-Output "LOGIN -> $base/api/v1/auth/login/"
    $r = Invoke-RestMethod -Uri "$base/api/v1/auth/login/" -Method Post -ContentType 'application/json' -Body (ConvertTo-Json $creds -Depth 5) -TimeoutSec 30
    Write-Output "LOGIN_RESPONSE: $(ConvertTo-Json $r -Depth 5)"
    $token = $null
    if ($r.access) { $token = $r.access } elseif ($r.access_token) { $token = $r.access_token } elseif ($r.token) { $token = $r.token } elseif ($r.data -and $r.data.access) { $token = $r.data.access }
    if (-not $token) { Write-Output "NO_ACCESS_TOKEN_FOUND"; exit 2 }
    Write-Output "ACCESS_TOKEN_LENGTH: $($token.Length)"

    $hdr = @{ Authorization = "Bearer $token" }
    Write-Output "GALLERY -> $base/api/v1/gallery/"
    $g = Invoke-RestMethod -Uri "$base/api/v1/gallery/" -Headers $hdr -Method Get -TimeoutSec 30
    Write-Output "GALLERY_RESPONSE: $(ConvertTo-Json $g -Depth 6)"
    Write-Output "G_RESPONSE_PROPERTIES: $((($g | Get-Member -MemberType NoteProperty) | ForEach-Object { $_.Name }) -join ', ')"

    # Support different API shapes: direct array (preferred), value (our current), results (DRF)
    if ($g -is [System.Array]) { $items = $g }
    elseif ($g.value) { $items = $g.value }
    elseif ($g.results) { $items = $g.results }
    else { $items = @($g) }

    Write-Output "ITEM_COUNT: $($items.Count)"
    if ($items.Count -gt 0) {
        Write-Output "FIRST_ITEM_JSON: $(ConvertTo-Json $items[0] -Depth 6)"
        Write-Output "FIRST_ITEM_PROPERTIES: $((($items[0] | Get-Member -MemberType NoteProperty) | ForEach-Object { $_.Name }) -join ', ')"
    }
    $i = 0
    foreach ($item in $items) {
        $i++
        $url = $null
        if ($item.media_url) { $url = $item.media_url } elseif ($item.image) { $url = $item.image } elseif ($item.url) { $url = $item.url }
        Write-Output "--- ITEM $i ---"
        Write-Output "MEDIA_URL: $url"
        if ($url) {
            try {
                $h = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
                Write-Output "HEAD_STATUS: $($h.StatusCode) ContentType:$($h.Headers['Content-Type'])"
            } catch {
                Write-Output "HEAD_FAIL: $($_.Exception.Message)"
            }
            if ($url -match '/storage/v1/s3/') {
                $public = $url -replace '/storage/v1/s3/','/storage/v1/object/public/'
                Write-Output "MAPPED_PUBLIC_URL: $public"
                try {
                    $hp = Invoke-WebRequest -Uri $public -Method Head -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
                    Write-Output "PUBLIC_HEAD_STATUS: $($hp.StatusCode) ContentType:$($hp.Headers['Content-Type'])"
                } catch {
                    Write-Output "PUBLIC_HEAD_FAIL: $($_.Exception.Message)"
                }
            } elseif ($url -match '/storage/v1/object/public/') {
                try {
                    $hp2 = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
                    Write-Output "PUBLIC_HEAD_STATUS: $($hp2.StatusCode) ContentType:$($hp2.Headers['Content-Type'])"
                } catch {
                    Write-Output "PUBLIC_HEAD_FAIL: $($_.Exception.Message)"
                }
            }
        }
    }
    exit 0
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
    exit 1
}
