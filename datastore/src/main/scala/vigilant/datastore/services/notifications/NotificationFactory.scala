package vigilant.datastore.services.notifications

import org.slf4j.LoggerFactory
import vigilant.datastore.services.notifications.email.EmailClient
import vigilant.datastore.services.notifications.twillo.TwilloClient

object NotificationFactory {
  private val logger = LoggerFactory.getLogger(getClass)

  private var _twillo: TwilloClient = null
  private var _email: EmailClient = null

  def configure_twillo(account_sid: String, auth_token: String, from: String) = {
    _twillo = new TwilloClient(account_sid, auth_token, from)
  }

  def send_sms_notification(to: String, from: String, body: String) = {
   _twillo match {
     case null =>
     case _ => _twillo.send_sms(to, from, body)
   }
  }

  def configure_email(smtp_server: String, from: String) = {
    _email = new EmailClient(smtp_server, from)
  }

  def send_email_notification(to: String, subject: String, body: String) = {
    _email match {
      case null =>
      case _ => _email.send_email(to, subject, body)
    }
  }
}
