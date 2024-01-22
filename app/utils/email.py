import smtplib

HOST = "smtp-mail.outlook.com"
PORT = 587


def send_email(
    title: str,
    body: str,
    to_email: str,
    from_email: str,
    password: str,
):
    message = f"""Subject: {title}

    {body}
    """

    smtp = smtplib.SMTP(HOST, PORT)

    status_code, response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code, response = smtp.starttls()
    print(f"[*] Starting TLS connection: {status_code} {response}")

    status_code, response = smtp.login(from_email, password)
    print(f"[*] Logging in: {status_code} {response}")

    smtp.sendmail(from_email, to_email, message)
    smtp.quit()
