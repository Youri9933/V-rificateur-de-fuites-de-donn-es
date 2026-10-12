from breach_checker import passwords, strength

def test_sha1_prefix_is_known_value():
  assert passwords._sha1_hex("password").startswith("5BAA6")


def test_count_leaks_found(monkeypatch):
  fake = "1E4C9B93F3F0682250B6CF8331B7EE68FD8:42\nABCDEF:1"
  monkeypatch.setattr(passwords, "_fetch_range", lambda prefix: fake)
  assert passwords.count_leaks("password") == 42


def test_count_leaks_not_found(monkeypatch):
  monkeypatch.setattr(passwords, "_fetch_range", lambda prefix: "ABCDEF:1")
  assert passwords.count_leaks("password") == 0



def test_strength_ordering():
  assert strength.evaluate("abc").entropy < strength.evaluate("Xk9#mP2$vLq8").entropy_bits
  