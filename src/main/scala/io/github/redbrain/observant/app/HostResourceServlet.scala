package io.github.redbrain.observant.app

import org.json4s.{DefaultFormats, Formats}
import org.scalatra.json._

class HostResourceServlet extends ObservantStack with JacksonJsonSupport {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/keys") {
    List(1,2,3,4)
  }
}
