package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.app.ObservantStack
import io.github.redbrain.observant.caches.HostCache
import io.github.redbrain.observant.models.HostsDataModel
import org.json4s.{DefaultFormats, Formats}
import org.scalatra.json._

case class HostDataPayload(key: String, payload: List[HostsDataModel])

class HostResourcesServlet extends ObservantStack with JacksonJsonSupport {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/keys") {
    HostCache.getHostKeys()
  }

  get("/data/:key") {
    val key = params("key")
    HostDataPayload(key, HostCache.getCacheDataForKey(key))
  }

}
