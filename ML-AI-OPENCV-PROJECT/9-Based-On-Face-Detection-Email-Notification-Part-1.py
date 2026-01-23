import smtplib as s

m = s.SMTP('smtp.gmail.com', 587)
e = 'juwelpal1010@gmail.com'  # Sender Mail
p = 'hnot zqrx pyux ynwx'  # App Password
msg = 'Hello Juwel'

m.ehlo()
m.starttls()
m.login(e,p)
m.sendmail(e, 'recieve email', msg)
m.close()
print('Working')