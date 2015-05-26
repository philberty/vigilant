package vigilant.datastore.services.configuration

import java.net.InetSocketAddress
import java.nio.file.{Paths, Files}

import akka.actor.Props
import play.api.libs.json.{JsValue, Json}
import vigilant.datastore.services.notifications.NotificationFactory
import vigilant.datastore.services.transports.Transport
import vigilant.datastore.services.transports.udp.UDPTransport

object ConfigurationService {

  private var _configuration: JsValue = null

  def load_configuration_from_file(filepath: String) = {
    _configuration = Json.parse(Files.readAllBytes(Paths.get(filepath)))
    configure_email
    configure_twillo
  }

  def configure_twillo = {
    val account_sid = (_configuration \ "twillo" \ "account_sid").as[String]
    val auth_token = (_configuration \ "twillo" \ "auth_token").as[String]
    val from = (_configuration \ "twillo" \ "from").as[String]
    NotificationFactory.configure_twillo(account_sid, auth_token, from)
  }

  def configure_email = {
    val smtp_server = (_configuration \ "email" \ "smtp_server").as[String]
    val from = (_configuration \ "email" \ "from").as[String]
    NotificationFactory.configure_email(smtp_server, from)
  }

  def cache_timeout: Int = {
    try {
      (_configuration \ "cache" \ "timeout").as[Int]
    } catch {
      case e: Exception => 30
    }
  }

  def cache_threshold: Int = {
    try {
      (_configuration \ "cache" \ "threshold").as[Int]
    } catch {
      case e: Exception => 40
    }
  }

  def trigger_notification_grace_period: Long = {
    try {
      (_configuration \ "triggers" \ "notification_threshold").as[Long]
    } catch {
      case e: Exception => 120
    }
  }

  def database_jdbc: String = (_configuration \ "database" \ "jdbc").as[String]

  def transport_type: String = (_configuration \ "transport" \ "type").as[String]

  def transport_bind: String = (_configuration \ "transport" \ "host").as[String]

  def transport_port: Int = (_configuration \ "transport" \ "port").as[Int]

  def transport_address: InetSocketAddress = new InetSocketAddress(transport_bind, transport_port)

  def transport: Transport = {
    transport_type match {
      case "udp" => UDPTransport
      case _ => throw new Exception("Invalid transport type")
    }
  }

  def transport_actor: Props = {
    transport_type match {
      case "udp" => Props(classOf[UDPTransport], transport_address)
      case _ => throw new Exception("Invalid transport type")
    }
  }

}
