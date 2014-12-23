package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.caches.{LogCache, ProcCache, HostCache}
import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.models.{LogDataModel, ProcessDataModel, Liveness, HostsDataModel}
import org.json4s.{DefaultFormats, Formats}
import org.scalatra.SessionSupport
import org.scalatra.atmosphere._
import org.scalatra.json._

import scala.concurrent._
import ExecutionContext.Implicits.global

class StatsApiServlet extends ObservantStack with JacksonJsonSupport with SessionSupport with AtmosphereSupport {

  protected implicit val jsonFormats: Formats = DefaultFormats

  case class LogDataPayload(key: String, payload: List[LogDataModel])
  case class ProcessDataPayload(key: String, payload: List[ProcessDataModel])
  case class HostDataSnap(key: String, payload: HostsDataModel)
  case class HostDataPayload(key: String, payload: List[HostsDataModel])
  case class StateHost(alive: Boolean, data: HostsDataModel)
  case class StateDataPayload(payload: List[StateHost])

  before() {
    contentType = formats("json")
  }

  // --- --- --- ---

  get("/state") {
    val keys = HostCache.getKeys()
    var payload = List[StateHost]()

    keys.foreach(key => {
      val cache = HostCache.getCacheDataForKey(key)
      val data = cache(cache.length - 1)
      payload = payload :+ StateHost(
        isDataAliveForTimeout(
          data.ts,
          Configuration.getHostsDataTimeout()
        ), data
      )
    })
    StateDataPayload(payload)
  }

  // --- --- --- ---

  get("/host/keys") {
    HostCache.getKeys()
  }

  get("/proc/keys") {
    ProcCache.getKeys()
  }

  get("/logs/keys") {
    LogCache.getKeys()
  }

  // --- --- --- ---

  get("/host/liveness/:key") {
    val key = params("key")
    val data = HostCache.getCacheDataForKey(key)
    if (data.length == 0) {
      Liveness(false)
    } else {
      Liveness(
        isDataAliveForTimeout(
          data(data.length - 1).ts,
          Configuration.getHostsDataTimeout()
        )
      )
    }
  }

  get("/proc/liveness/:key") {
    val key = params("key")
    val data = ProcCache.getCacheDataForKey(key)
    if (data.length == 0) {
      Liveness(false)
    } else {
      Liveness(
        isDataAliveForTimeout(
          data(data.length - 1).ts,
          Configuration.getHostsDataTimeout()
        )
      )
    }
  }

  get("/logs/liveness/:key") {
    val key = params("key")
    val data = LogCache.getCacheDataForKey(key)
    if (data.length == 0) {
      Liveness(false)
    } else {
      Liveness(
        isDataAliveForTimeout(
          data(data.length - 1).ts,
          Configuration.getHostsDataTimeout()
        )
      )
    }
  }

  // --- --- --- ---

  get("/host/procs/:key") {
    val key = params("key")
    ProcCache.getProcessesRunningOnHost(key)
  }

  // --- --- --- ---

  get("/host/rest/:key") {
    val key = params("key")
    HostDataPayload(key, HostCache.getCacheDataForKey(key))
  }

  post("/host/rest/:key") {
    val key = params("key")
    HostCache.getCacheDataForKey(key)(0)
  }

  delete("/host/rest/:key") {
    val key = params("key")
    val data = HostCache.getCacheDataForKey(key)
    if (!isDataAliveForTimeout(data(data.length - 1).ts, Configuration.getHostsDataTimeout())) {
      HostCache.deleteKey(key)
    }
  }

  // --- --- --- ---

  get("/proc/rest/:key") {
    val key = params("key")
    ProcessDataPayload(key, ProcCache.getCacheDataForKey(key))
  }

  post("/proc/rest/:key") {
    val key = params("key")
    ProcCache.getCacheDataForKey(key)(0)
  }

  delete("/proc/rest/:key") {
    val key = params("key")
    val data = ProcCache.getCacheDataForKey(key)
    if (!isDataAliveForTimeout(data(data.length - 1).ts, Configuration.getProcDataTimeout())) {
      ProcCache.deleteKey(key)
    }
  }

  // --- --- --- ---

  get("/logs/rest/:key") {
    val key = params("key")
    LogDataPayload(key, LogCache.getCacheDataForKey(key))
  }

  post("/logs/rest/:key") {
    val key = params("key")
    LogCache.getCacheDataForKey(key)(0)
  }

  delete("/logs/rest/:key") {
    val key = params("key")
    val data = LogCache.getCacheDataForKey(key)
    if (!isDataAliveForTimeout(data(data.length - 1).ts, Configuration.getLogDataTimeout())) {
      LogCache.deleteKey(key)
    }
  }

  // --- --- --- ---

  atmosphere("/host/sock/:key") {
    new AtmosphereStatsClientMonitor(params("key"), StatType.HOST) {
      override def observedHostStat(data: HostsDataModel) {
        if (data.key == this.key) send(JsonMessage(encodeJson(data)))
      }
    }
  }

  atmosphere("/proc/sock/:key") {
    new AtmosphereStatsClientMonitor(params("key"), StatType.PROC) {
      override def observedProcStats(data: ProcessDataModel) {
        if (data.key == this.key) send(JsonMessage(encodeJson(data)))
      }
    }
  }

  atmosphere("/logs/sock/:key") {
    new AtmosphereStatsClientMonitor(params("key"), StatType.LOG) {
      override def observedLogStat(data: LogDataModel) {
        if (data.key == this.key) send(JsonMessage(encodeJson(data)))
      }
    }
  }

  // --- --- --- ---
}