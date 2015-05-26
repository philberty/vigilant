package vigilant.datastore.services.notifications.email

import javax.mail.{Transport, Message, Session}
import javax.mail.internet.{InternetAddress, MimeMessage}

class EmailClient(smtp_server: String, from: String) {

  private val properties = System.getProperties()
  properties.setProperty("mail.smtp.host", smtp_server)

  val session= Session.getDefaultInstance(properties)

  def send_email(to: String, subject: String, body: String) = {
    val message = new MimeMessage(session)

    message.setFrom(new InternetAddress(from))
    message.addRecipient(Message.RecipientType.TO, new InternetAddress(to))
    message.setSubject(subject)
    message.setText(body)

    Transport.send(message)
  }
}
