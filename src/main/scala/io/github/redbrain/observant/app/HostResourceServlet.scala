package io.github.redbrain.observant.app

import io.github.redbrain.observant.models.HostsDataModel
import org.json4s.{DefaultFormats, Formats}
import org.scalatra.json._
import play.api.libs.json.{JsString, JsObject}

class HostResourceServlet extends ObservantStack with JacksonJsonSupport {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/keys") {
    HostsDataModel.getKeys()
  }

  get("/data/:key") {
    val key:String = params("key");
    JsObject(Seq(
      "key" -> JsString(key),
      "data" -> HostsDataModel.getCachedDataForKey(key)
    ))
  }
}
