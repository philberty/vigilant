package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.app.ObservantStack
import io.github.redbrain.observant.caches.LogCache
import io.github.redbrain.observant.models.LogDataModel
import org.json4s.{DefaultFormats, Formats}
import org.scalatra.json.JacksonJsonSupport

case class LogDataPayload(key: String, payload: List[LogDataModel])

class LogResourcesServlet extends ObservantStack with JacksonJsonSupport {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/keys") {
    LogCache.getHostKeys()
  }

  get("/data/:key") {
    val key = params("key")
    LogDataPayload(key, LogCache.getCacheDataForKey(key))
  }

}
