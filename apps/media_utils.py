from __future__ import annotations

from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def url_exists(url: str) -> bool:
    if not url:
        return False

    try:
        request = Request(url, method='HEAD')
        with urlopen(request, timeout=10) as response:
            return getattr(response, 'status', None) == 200
    except HTTPError as error:
        if error.code == 405:
            try:
                request = Request(url, method='GET')
                with urlopen(request, timeout=10) as response:
                    return getattr(response, 'status', None) == 200
            except Exception:
                return False
        return False
    except (URLError, ValueError, TimeoutError, OSError):
        return False
    except Exception:
        return False


def supabase_public_url(endpoint_url: str | None, bucket_name: str | None, object_name: str | None) -> str | None:
    if not endpoint_url or not bucket_name or not object_name:
        return None

    parsed = urlparse(endpoint_url)
    if not parsed.scheme or not parsed.netloc:
        return None

    project_host = parsed.netloc.replace('.storage.supabase.co', '.supabase.co')
    normalized_object = object_name.lstrip('/')
    return f"{parsed.scheme}://{project_host}/storage/v1/object/public/{bucket_name}/{normalized_object}"


def supabase_public_url_from_storage_url(storage_url: str | None) -> str | None:
    if not storage_url:
        return None

    parsed = urlparse(storage_url)
    if not parsed.scheme or not parsed.netloc:
        return None

    marker = '/storage/v1/s3/'
    if '.storage.supabase.co' in parsed.netloc and marker in parsed.path:
        project_host = parsed.netloc.replace('.storage.supabase.co', '.supabase.co')
        remainder = parsed.path.split(marker, 1)[1].lstrip('/')
        parts = remainder.split('/', 1)
        if len(parts) == 2:
            bucket_name, object_name = parts
            return f"{parsed.scheme}://{project_host}/storage/v1/object/public/{bucket_name}/{object_name}"

    return storage_url


def storage_object_name_from_url(url: str | None) -> str | None:
    if not url:
        return None

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return None

    if '/storage/v1/object/public/' in parsed.path:
        return parsed.path.split('/storage/v1/object/public/', 1)[1].lstrip('/')

    marker = '/storage/v1/s3/'
    if marker in parsed.path:
        remainder = parsed.path.split(marker, 1)[1].lstrip('/')
        parts = remainder.split('/', 1)
        if len(parts) == 2:
            return parts[1]

    if parsed.path.startswith('/media/'):
        return parsed.path.split('/media/', 1)[1].lstrip('/')

    return None


def resolve_media_url(
    *,
    raw_url: str | None = None,
    storage_name: str | None = None,
    endpoint_url: str | None = None,
    bucket_name: str | None = None,
    storage=None,
    request=None,
) -> str | None:
    candidates: list[str] = []

    if raw_url:
        raw_url = str(raw_url).strip()
        if raw_url.startswith('http://') or raw_url.startswith('https://'):
            candidates.append(supabase_public_url_from_storage_url(raw_url))
            candidates.append(raw_url)
        elif request and raw_url.startswith('/'):
            candidates.append(request.build_absolute_uri(raw_url))

    if storage_name:
        public_url = supabase_public_url(endpoint_url, bucket_name, storage_name)
        if public_url:
            candidates.append(public_url)

    seen: set[str] = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)

        if storage and storage_name:
            try:
                if storage.exists(storage_name):
                    return candidate
            except Exception:
                pass

        if url_exists(candidate):
            return candidate

    return None
