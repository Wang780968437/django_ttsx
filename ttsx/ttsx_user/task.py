#!/user/bin/env python3
# -*- conding:utf-8 -*-
from celery import task
from django.core.mail import send_mail
from django.conf import settings

@task
def sendmail(uid,email):
    msg = '<a href="http://127.0.0.1:8000/user/active%s/" target="_blank">点击激活</a>' % (uid)
    send_mail('天天生鲜用户激活', '',
              settings.EMAIL_FROM,
              [email],
              html_message=msg)





