package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.app.ObservantStack
import io.github.redbrain.observant.models.HostsDataModel
import io.github.redbrain.observant.caches.HostCache
import org.json4s.{Formats, DefaultFormats}
import org.scalatra.json.JacksonJsonSupport

case class StateDataPayload(payload: List[HostsDataModel])

class StateResourcesServlet extends ObservantStack with JacksonJsonSupport {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/") {
    val keys = HostCache.getHostKeys()
    var payload = List[HostsDataModel]()

    keys.foreach(key => {
      payload = payload :+ HostCache.getCacheDataForKey(key).head
    });

    StateDataPayload(payload)
  }

}
