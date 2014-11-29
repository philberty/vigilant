package io.github.redbrain.observant.aggregator

import io.github.redbrain.observant.models.HostsDataModel
import play.api.libs.json.JsValue

trait ObservantProtocolFactory {

  def getHostDataModel(json: JsValue): HostsDataModel = {
    val hostname = (json \ "payload" \ "hostname").as[String]
    val timestamp = (json \ "payload" \ "timestamp").as[String]
    val usage = (json \ "payload" \ "usage").as[Float]
    val process = (json \ "payload" \ "process").as[Int]
    val cores = (json \ "payload" \ "cores").as[Int]
    val memoryTotal = (json \ "payload" \ "memory_total").as[Long]
    val memoryUsed = (json \ "payload" \ "memory_used").as[Long]
    val platform = (json \ "payload" \ "platform").as[String]
    val machine = (json \ "payload" \ "machine").as[String]
    val version = (json \ "payload" \ "version").as[String]
    val diskTotal = (json \ "payload" \ "disk_total").as[Long]
    val diskFree = (json \ "payload" \ "disk_free").as[Long]
    new HostsDataModel(hostname,timestamp,usage,process,cores,memoryTotal,memoryUsed,platform,machine,version,diskTotal,diskFree)
  }

}
