package io.github.redbrain.observant.aggregator

import io.github.redbrain.observant.models.HostsDataModel
import play.api.libs.json.JsValue

trait ObservantProtocolFactory {

  def getHostDataModel(json: JsValue): HostsDataModel = {
    val hostname:String = (json \ "payload" \ "hostname").as[String]
    val timestamp:String = (json \ "payload" \ "timestamp").as[String]
    val usage:Float = (json \ "payload" \ "usage").as[Float]
    val process:Int = (json \ "payload" \ "process").as[Int]
    val cores:Int = (json \ "payload" \ "cores").as[Int]
    val memoryTotal:Int = (json \ "payload" \ "memory_total").as[Int]
    val memoryUsed:Int = (json \ "payload" \ "memory_used").as[Int]
    val platform:String = (json \ "payload" \ "platform").as[String]
    val machine:String = (json \ "payload" \ "machine").as[String]
    val version:String = (json \ "payload" \ "version").as[String]
    val diskTotal:Int = (json \ "payload" \ "disk_total").as[Int]
    val diskFree:Int = (json \ "payload" \ "disk_free").as[Int]
    new HostsDataModel(hostname,timestamp,usage,process,cores,memoryTotal,memoryUsed,platform,machine,version,diskTotal,diskFree)
  }

}
