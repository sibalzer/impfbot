from alerts import send_telegram_msg

try:
    send_telegram_msg("Test")
    print("Test erfolgreich!")
except Exception as e:
    print(f"Da ist ewas schiefgelaufen... {e}")
