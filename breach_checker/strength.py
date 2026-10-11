import math
import string
from dataclasses import dataclass


@dataclass(frozen=True)
class Strength:
  entropy: float
  label: str
  tips: list[str]



  def _charset_size(password: str) -> int:
    pool = [
      (string.ascii_lowercase, 26),
      (string.ascii_uppercase, 26),
      (string.digits, 10),
      (string.punctuation, len(string.punctuation)),
    ]
    size = sum(n for chars, n in pool if any(c in chars for c in password))

    if any(c not in string.printable for c in password):
      size += 32
    return size



  def _label(bits: float) -> str:
    if bits < 40:
      return "Weak"
    if bits < 60:
      return "AVERAGE"
    if bits < 80:
      return "good"
    return "Excellent"

  def evaluate(password: str) -> "Strength":
    if not password:
      return Strength(0.0, "Empty", [])

    bits = len(password) * math.log2(Strength._charset_size(password))

    tips = []
    if len(password) < 12:
      tips.append("Use at least 12 characters.")
    if password.lower() == password or password.upper() == password:
      tips.append("Use a mix of uppercase and lowercase letters.")
    if not any(c.isdigit() for c in password):
      tips.append("Include at least one number.")
    if len(set(password)) < len(password) /2:
      tips.append("Avoid repeating characters.")
    tips.append("A long passphrase is more secure than a complex password.")

    return Strength(round(bits, 1), Strength._label(bits), tips)
  