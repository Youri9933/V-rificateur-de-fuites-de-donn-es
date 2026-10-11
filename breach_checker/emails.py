from functools import lru_cache
from urllib.parse import quote

import requests

from .errors import BreachCheckError

API_URL = "https://api.xposedornot.com/v1/check-email/{email}"
TIMEOUT_SECONDS = 8

_session = requests.Session()
_session.headers.update({"User-Agent": "breach-checker-hackathon"})


@lru_cache(maxsize=128)
def find_breaches(email: str) -> tuple[str, ...]:
  try:
    response = _session.get(
        API_URL.format(email=quote(email, safe="@")),
        timeout=TIMEOUT_SECONDS,
    )
  except requests.RequestException as exc:
    raise BreachCheckError("Service XposedOrNot injoignable.") from exc

  if response.status_code == 404:
    return ()
  if response.status_code == 429:
    raise BreachCheckError("Trop de requêtes. Réessaie dans un instant.")
  if not response.ok:
    raise BreachCheckError(f"Erreur du service ({response.status_code}).")

  names: list[str] = []
  for group in response.json().get("breaches") or []:
    names.extend(group if isinstance(group, list) else [group])
  return tuple(names)
