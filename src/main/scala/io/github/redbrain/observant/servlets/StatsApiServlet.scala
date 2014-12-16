package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.caches.{LogCache, ProcCache, HostCache}
import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.models.{LogDataModel, ProcessDataModel, Liveness, HostsDataModel}
import org.json4s.{DefaultFormats, Formats}
import org.scalatra.json._

case class LogDataPayload(key: String, payload: List[LogDataModel])
case class ProcessDataPayload(key: String, payload: List[ProcessDataModel])
case class HostDataSnap(key: String, payload: HostsDataModel)
case class HostDataPayload(key: String, payload: List[HostsDataModel])

class StatsApiServlet extends ObservantStack with JacksonJsonSupport with DataFactory {

  protected implicit val jsonFormats: Formats = DefaultFormats

  // Turn all respsonses into json
  before() {
    contentType = formats("json")
  }

  get("/host/keys") {
    HostCache.getHostKeys()
  }

  get("/proc/keys") {
    ProcCache.getHostKeys()
  }

  get("/logs/keys") {
    LogCache.getHostKeys()
  }

  get("/host/liveness/:key") {
    val key = params("key")
    val data = HostCache.getCacheDataForKey(key)
    Liveness(
      isDataAliveForTimeout(
        data(data.length - 1).ts,
        Configuration.getHostsDataTimeout()
      )
    )
  }

  get("/proc/liveness/:key") {
    val key = params("key")
    val data = ProcCache.getCacheDataForKey(key)
    Liveness(
      isDataAliveForTimeout(
        data(data.length - 1).ts,
        Configuration.getHostsDataTimeout()
      )
    )
  }

  get("/logs/liveness/:key") {
    val key = params("key")
    val data = LogCache.getCacheDataForKey(key)
    Liveness(
      isDataAliveForTimeout(
        data(data.length - 1).ts,
        Configuration.getHostsDataTimeout()
      )
    )
  }

  get("/host/rest/:key") {
    val key = params("key")
    HostDataPayload(key, HostCache.getCacheDataForKey(key))
  }


  get("/proc/rest/:key") {
    val key = params("key")
    ProcessDataPayload(key, ProcCache.getCacheDataForKey(key))
  }

  get("/logs/rest/:key") {
    val key = params("key")
    LogDataPayload(key, LogCache.getCacheDataForKey(key))
  }


}
