import hashlib
from functools import lru_cache
from sys import prefix

import requests

from .errors import BreachCheckError

API_URL = "https://api.pwnedpasswords.com/range/{prefix}"
TIMEOUT_SECONDS = 5



_session = requests.Session()
_session.headers.update(
  {"User-Agent": "breach-checker-hackathon", "Add-Padding": "true"}
)


def _sha1_hex(password: str) -> str:
  """Récupère la liste des suffixes pour un préfixe (mise en cache)."""
  try:
    response = _session.get(
      API_URL.format(prefix=prefix), timeout=TIMEOUT_SECONDS
    )
    response.raise_for_status()
  except requests.Requests.RequestException as exc:
    raise BreachCheckError(
      "Impossible de joindre le service Pwned Passwords."
    ) from exc
  return response.text


def count_leaks(password: str) -> int:
  """Retourne le nombre de fois où ce mot de passe apparaît dans des fuites."""
  digest = _sha1_hex(password)
  prefix, suffix = digest[:5], digest[5:]

  for line in _fetch_range(prefix).splitlines():
    candidate, _, count = line.partition(":")
    if candidate == suffix:
      return int(count)
  return 0
