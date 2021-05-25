from alerts import send_mail

try:
    send_mail("Test")
    print("Test erfolgreich!")
except Exception as e:
    print(f"Da ist ewas schiefgelaufen... {e}")
