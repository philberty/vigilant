package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.app.ObservantStack
import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.models.HostsDataModel
import io.github.redbrain.observant.caches.HostCache
import org.json4s.{Formats, DefaultFormats}
import org.scalatra.json.JacksonJsonSupport

case class StateHost(alive: Boolean, data: HostsDataModel)
case class StateDataPayload(payload: List[StateHost])

class StateResourcesServlet extends ObservantStack with JacksonJsonSupport with DataFactory {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/") {
    val keys = HostCache.getHostKeys()
    var payload = List[StateHost]()

    keys.foreach(key => {
      val cache = HostCache.getCacheDataForKey(key)
      val data = cache(cache.length - 1)
      payload = payload :+ StateHost(
        isDataAliveForTimeout(
          data.ts, Configuration.getHostsDataTimeout()
        ), data
      )
    })

    StateDataPayload(payload)
  }

}
