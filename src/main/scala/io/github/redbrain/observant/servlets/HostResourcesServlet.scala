package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.caches.HostCache
import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.models.{Liveness, HostsDataModel}
import org.json4s.{DefaultFormats, Formats}
import org.scalatra.json._

case class HostDataSnap(key: String, payload: HostsDataModel)
case class HostDataPayload(key: String, payload: List[HostsDataModel])

class HostResourcesServlet extends ObservantStack with JacksonJsonSupport with DataFactory {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/keys") {
    HostCache.getHostKeys()
  }

  get("/liveness/:key") {
    val key = params("key")
    val data = HostCache.getCacheDataForKey(key)
    Liveness(
      isDataAliveForTimeout(
        data(data.length - 1).ts,
        Configuration.getHostsDataTimeout()
      )
    )
  }

  get("/rest/:key") {
    val key = params("key")
    HostDataPayload(key, HostCache.getCacheDataForKey(key))
  }

  post("/rest/:key") {
    val key = params("key")
    HostDataSnap(key, HostCache.getCacheDataForKey(key).head)
  }

}
