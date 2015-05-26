package vigilant.datastore.services.triggers

import vigilant.datastore.models.{Email, Sms}
import vigilant.datastore.services.configuration.ConfigurationService
import vigilant.datastore.services.notifications.NotificationFactory

class Trigger(val identifier: String, val sms_notification: Sms, val email_notification: Email) {

  private var _subject: String = ""
  private var _body: String = ""
  private var _ts: java.util.Date = null

  def sms(subject: String) = {
    sms_notification match {
      case null =>
      case _ =>
        // this is really bad but ok for now but we cannot go live with this
        scala.util.control.Exception.ignoring(classOf[Exception]) {
          NotificationFactory.send_sms_notification(sms_notification.to, null, subject)
        }
    }
  }

  def email(subject: String, body: String) = {
    email_notification match {
      case null =>
      case _ =>
        scala.util.control.Exception.ignoring(classOf[Exception]) {
          NotificationFactory.send_email_notification(email_notification.to, subject, body)
        }
    }
  }

  def now: java.util.Date = new java.util.Date()

  def grace_period: Long = ConfigurationService.trigger_notification_grace_period

  def grace_period_expired: Boolean = {
    _ts match {
      case null => true
      case _ => ((now.getTime - _ts.getTime) / 1000) >= grace_period
    }
  }

  def data_changed(subject: String, body: String): Boolean = {
    val change = !((_subject == subject) && (_body == body))
    if (change) {
      _subject = subject
      _body = body
    }
    change
  }

  def notify(subject: String, body: String) = {
    if (data_changed(subject, body)) {
      _ts = now
      sms(subject)
      email(subject, body)
    }
  }

}
