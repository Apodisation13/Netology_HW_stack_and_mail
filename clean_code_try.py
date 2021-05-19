import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self):
        self.GMAIL_SMTP = "smtp.gmail.com"
        self.GMAIL_IMAP = "imap.gmail.com"

        self.sender = 'your_gmail@com'  # откуда отправлять письмо

        with open('password.txt', 'r', encoding='utf-8') as f:
            self.password = f.readline()

        # self.password = 'your_gmail_pass'

        self.recipients = [self.sender, 'navalihin-1998@mail.ru']  # пробую отправить себе

        self.header = None

    def send_message(self, subject: str, message: str):
        """здесь наверное можно написать докстринг, но вроде и так наглядно, что есть что"""
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        try:
            ms = smtplib.SMTP(self.GMAIL_SMTP, 587)  # identify ourselves to smtp gmail client
            ms.ehlo()  # secure our email with tls encryption
            ms.starttls()  # re-identify ourselves as an encrypted connection
            ms.ehlo()

            ms.login(self.sender, self.password)

            ms.sendmail(self.sender, self.recipients, msg.as_string())
            print(f'Успешно отправлено письмо на адреса {self.recipients}')

            ms.quit()

        except Exception as E:
            print(E)

    def receive_mail(self, number=100, *header: str):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.sender, self.password)
        mail.list()
        mail.select("inbox")

        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', criterion)
        # здесь было так: ('search', None, criterion) - ругалось на None, но работало. Работает так же и без него.

        assert data[0], 'There are no letters with current header'  # если такого заголовка нет, то прерываемся
        latest_email_uid = int(data[0].split()[-1])

        for mail_num in range(latest_email_uid, latest_email_uid - number, -1):  # последние number писем
            result, data = mail.uid('fetch', str(mail_num), '(RFC822)')

            if data[0]:  # тут смысл такой: если дальше нет писем, то сразу выйдем из цикла
                raw_email = data[0][1]
                print(raw_email)
                email_message = email.message_from_string(str(raw_email, 'utf-8'))
                print(f'CООБЩЕНИЕ номер {mail_num}\n')  # для проверки сколько раз тут выведется.
                print(email_message)
            else:
                print('Дальше сообщений нет')
                break

        mail.logout()


if __name__ == '__main__':
    gmail = Mail()
    gmail.send_message('Topic', 'Send_Try2')
    head = 'rtt'
    gmail.receive_mail(2, head)
