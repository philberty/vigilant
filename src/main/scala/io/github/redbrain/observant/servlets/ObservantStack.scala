package io.github.redbrain.observant.servlets

import java.util.{Calendar, Date}

import org.json4s._
import org.scalatra._
import org.scalatra.scalate.ScalateSupport

trait ObservantStack extends ScalatraServlet with ScalateSupport {

  notFound {
    status = 404
    resourceNotFound()
  }

  def isDataAliveForTimeout(timestamp: Date, timeout: Int): Boolean  = {
    val now = Calendar.getInstance.getTime
    val seconds = (now.getTime - timestamp.getTime) / 1000
    if (seconds >= timeout) false else true
  }

  def encodeJson(src: AnyRef): JValue = {
    import org.json4s.{Extraction, NoTypeHints}
    import org.json4s.jackson.Serialization
    implicit val formats = Serialization.formats(NoTypeHints)
    Extraction.decompose(src)
  }
}
