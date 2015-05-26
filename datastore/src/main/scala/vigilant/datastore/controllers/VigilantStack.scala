package vigilant.datastore.controllers

import java.util.{Calendar, Date}
import org.json4s._
import org.scalatra._
import org.scalatra.atmosphere.AtmosphereSupport
import org.scalatra.json.NativeJsonSupport
import vigilant.datastore.services.aggregator.ProtocolFactory
import vigilant.datastore.services.configuration.ConfigurationService

case class ErrorResponse(error: String)

trait VigilantStack extends ScalatraServlet
  with NativeJsonSupport
  with AtmosphereSupport
  with ProtocolFactory {

  protected implicit val jsonFormats: Formats = DefaultFormats

  notFound {
    status = 404
    ErrorResponse("No such resource")
  }

  before() {
    contentType = formats("json")
  }

  def online_status_for_timestamp(timestamp: String): String = {
    is_timestamp_alive(timestamp) match {
      case true => "online"
      case false => "offline"
    }
  }

  def is_timestamp_alive(ts: String): Boolean = {
    val timestamp = date_object_from_timestamp(ts)
    val timeout = ConfigurationService.cache_timeout
    val now = Calendar.getInstance.getTime
    val difference = (now.getTime - timestamp.getTime) / 1000
    difference <= timeout
  }

  def encodeJson(src: AnyRef): JValue = {
    import org.json4s.jackson.Serialization
    import org.json4s.{Extraction, NoTypeHints}
    implicit val formats = Serialization.formats(NoTypeHints)
    Extraction.decompose(src)
  }
}
