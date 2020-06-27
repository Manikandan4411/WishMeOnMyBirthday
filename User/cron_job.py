from django_cron import CronJobBase, Schedule
from User import views
from User import templates
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class MyCron(CronJobBase):
  RUN_EVERY_MINS = 2
  shedule = Schedule(run_every_mins=RUN_EVERY_MINS)
  code = 'User.MyCron'

  def do(self):
    message = render_to_string('sample.html', {})
    mail_subject = 'Sample Mail Test'
    to_email = 'santhosh220897@gmail.com'
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()