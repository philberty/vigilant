package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.caches.LogCache
import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.models.{Liveness, LogDataModel}
import org.json4s.{DefaultFormats, Formats}
import org.scalatra.json.JacksonJsonSupport

case class LogDataPayload(key: String, payload: List[LogDataModel])

class LogResourcesServlet extends ObservantStack with JacksonJsonSupport with DataFactory {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/keys") {
    LogCache.getHostKeys()
  }

  get("/liveness/:key") {
    val key = params("key")
    val data = LogCache.getCacheDataForKey(key)
    Liveness(
      isDataAliveForTimeout(
        data(data.length - 1).ts,
        Configuration.getHostsDataTimeout()
      )
    )
  }

  get("/rest/:key") {
    val key = params("key")
    LogDataPayload(key, LogCache.getCacheDataForKey(key))
  }

}
