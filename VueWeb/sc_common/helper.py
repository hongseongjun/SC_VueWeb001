from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
import string
import random

# 1. HTML 포멧 내용의 Email 송신 스레드 클래스
class EmailThread(threading.Thread):
    # 1)  Email 송신자료 설정
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    # 2) 스레드 런 설정: 
    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)


# 2. EmailThread를 통한 Email 송신 
def send_mail(subject, recipient_list, body='', from_email='sjishong@naver.com', fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()
    """
    print('Send Mail Start')
    import smtplib
    from email.mime.text import MIMEText
    session = smtplib.SMTP('smtp.naver.com', 587)
    print('*****************-1')
    session.starttls()
    print('*****************-2')
    session.login('sjishong@naver.com', 'sj72157215')
    print('*****************-3')
    msg = MIMEText('TLS 본문 테스트 메시지')
    msg['Subject'] = '제목'
    msg['From'] = 'sjishong@naver.com'
    msg['To'] = 'sjishong@naver.com'
    session.sendmail('sjishong@naver.com', 'sjishong@naver.com', msg.as_string())
    session.quit()
    print('Send Mail End')
    """

# 3. 8자리 영숫자 인증번호 생성 함수(비밀번호 찾기 등에 활용)
def email_auth_num():
    # 1) 영숫자 문자열 설정
    LENGTH = 8
    string_pool = string.ascii_letters + string.digits

    # 2) 8자리 렌덤 영숫자 문자열 산출 
    auth_num = ""
    for i in range(LENGTH):
        auth_num += random.choice(string_pool)
    return auth_num