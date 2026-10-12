import re
import streamlit as st

from breach_checker import emails, passwords, strength
from breach_checker.errors import BreachCheckError

email_pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

st.set_page_config(page_title="Breach Checker", )
st.title("Breach Checker")
st.caption("Check if your email or password has been compromised in a data breach.")

tab_password, tab_email = st.tabs(["Password", "Email"])


with tab_password:
  password = st.text_input("Enter your password:", type="password")
  st.info(
    "This tool checks if your password has been compromised in a data breach. It does not store or transmit your password. Please use a strong and unique password for each of your accounts." \
    "Never reuse passwords across multiple sites."
  )

  if password:
    result = strength.evaluate(password)
    col1, col2 = st.columns(2)
    col1.metric("Robustness", result.label)
    col2.metric("Entropy", f"{result.entropy} bits")

    try:
      leaks = passwords.count_leaks(password)
    except BreachCheckError as error:
      st.warning(str(error))
    else:
      if leaks:
        st.error(f"This password has leaked. {leaks:,} times. Change it.")
      else:
        st.success("No known leaks for this password.")

  with st.expander("Advice"):
    for tip in result.tips:
      st.write(f"- {tip}")


with tab_email:
  email = st.text_input("Enter your email address:")
  st.info(
    "Unlike the password, the email is sent to the service."
    "XposedOrNot for verification. Test only your own addresses."
  )

  if email and not email_pattern.match(email):
    st.error("Invalid email address.")
  elif email:
    try:
      breaches = emails.find_breaches(email)
    except BreachCheckError as error:
      st.warning(str(error))
    else:
      if not breaches:
        st.success("No known leaks for this email.")
      else:
        st.error(f" Present in {len(breaches)} leak(s).")
        st.write(", ".join(breaches))
        