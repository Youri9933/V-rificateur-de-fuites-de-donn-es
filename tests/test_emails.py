from breach_checker import emails


class FakeResponse:
  def __init__(self, status_code, payload=None):
    self.status_code = status_code
    self.payload = payload or {}
    self.ok = status_code < 400

  def json(self):
    return self.payload


def test_email_not_found(monkeypatch):
    emails.find_breach.cache_clear()
    monkeypatch.setattr(emails._session, "get", lambda *a, **k: FakeResponse(404))
    assert emails.find_breaches("a@b.com") == ()


def test_email_found(monkeypatch):
    emails.find_breaches.cache_clear()
    payload = {"breaches": [["adobe", "LinkedIn"]]}
    monkeypatch.setattr(emails._session, "get", lambda *a, **k: FakeResponse(200, payload))
    assert emails.find_breaches("c@d.com") == ("Adobe", "LinkedIn")
    