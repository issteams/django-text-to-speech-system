import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('abdulmumina535@gmail.com', 'eznhvpqnpqsrttxq')
    server.sendmail('abdulmumina535@gmail.com', 'abdulmumina535@gmail.com', 'Test email')
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
