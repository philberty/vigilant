package vigilant.datastore.services.notifications.twillo

import com.twilio.sdk.TwilioRestClient
import org.apache.http.NameValuePair
import org.apache.http.message.BasicNameValuePair
import org.slf4j.LoggerFactory

class TwilloClient(account_sid: String, auth_token: String, from: String) {
  private val logger = LoggerFactory.getLogger(getClass)

  private val _from = from
  private val _client = new TwilioRestClient(account_sid, auth_token)

  def send_sms(to: String, from: String, body: String) = {
    val params = new java.util.ArrayList[NameValuePair]()
    params.add(new BasicNameValuePair("Body", body))
    params.add(new BasicNameValuePair("To", to))
    params.add(new BasicNameValuePair("From", if (from == null || from.length == 0) _from else from))

    val message_factory = _client.getAccount.getMessageFactory
    val message = message_factory.create(params)
    logger.info(message.getSid)
  }
}
