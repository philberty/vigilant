package io.github.redbrain.observant.aggregator

import io.github.redbrain.observant.models.{ProcessDataModel, LogDataModel, HostsDataModel}
import play.api.libs.json.JsValue

trait ProtocolFactory {

  def getDateObjectFromTimeStamp(timestamp: String): java.util.Date = {
    val format = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
    format.parse(timestamp)
  }

  def getHostDataModel(json: JsValue): HostsDataModel = {
    val ts = getDateObjectFromTimeStamp((json \ "ts").as[String])
    val hostname = (json \ "payload" \ "hostname").as[String]
    val timestamp = (json \ "payload" \ "timestamp").as[String]
    val usage = (json \ "payload" \ "usage").as[Float]
    val processes = (json \ "payload" \ "processes").as[Int]
    val cores = (json \ "payload" \ "cores").as[Int]
    val memoryTotal = (json \ "payload" \ "memory_total").as[Long]
    val memoryUsed = (json \ "payload" \ "memory_used").as[Long]
    val platform = (json \ "payload" \ "platform").as[String]
    val machine = (json \ "payload" \ "machine").as[String]
    val version = (json \ "payload" \ "version").as[String]
    val diskTotal = (json \ "payload" \ "disk_total").as[Long]
    val diskFree = (json \ "payload" \ "disk_free").as[Long]
    val stats = (json \ "payload" \ "cpu_stats").as[List[Float]]

    new HostsDataModel(hostname, timestamp, usage, processes, cores, memoryTotal,
      memoryUsed, platform, machine, version, diskTotal, diskFree, stats, ts)
  }

  def getLogDataModel(json: JsValue): LogDataModel = {
    val ts = getDateObjectFromTimeStamp((json \ "ts").as[String])
    val message = (json \ "payload" \ "message").as[String]
    val host = (json \ "host").as[String]
    new LogDataModel(host, message, ts)
  }

  def getProcessDataModel(json: JsValue): ProcessDataModel = {
    val ts = getDateObjectFromTimeStamp((json \ "ts").as[String])
    val host = (json \ "host").as[String]
    val pid = (json \ "payload" \ "pid").as[Int]
    val path = (json \ "payload" \ "path").as[String]
    val cwd = (json \ "payload" \ "cwd").as[String]
    val cmd = (json \ "payload" \ "cmdline").as[List[String]]
    val status = (json \ "payload" \ "status").as[String]
    val user = (json \ "payload" \ "user").as[String]
    val threads = (json \ "payload" \ "threads").as[Int]
    val fds = (json \ "payload" \ "fds").as[Int]
    val ofds = (json \ "payload" \ "files").as[List[String]]
    val usage = (json \ "payload" \ "usage").as[Float]
    val memory = (json \ "payload" \ "memory_percent").as[Float]
    val connections = (json \ "payload" \ "connections").as[List[String]]

    new ProcessDataModel(host, pid, path, cwd, cmd, status, user,
      threads, fds, ofds, usage, memory, connections, ts)
  }
}
