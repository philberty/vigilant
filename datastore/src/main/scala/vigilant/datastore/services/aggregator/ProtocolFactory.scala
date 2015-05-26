package vigilant.datastore.services.aggregator

import play.api.libs.json.JsValue
import vigilant.datastore.models.{ProcessDataModel, LogDataModel, HostsDataModel}

trait ProtocolFactory {

  def date_object_from_timestamp(timestamp: String): java.util.Date = {
    val format = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
    format.parse(timestamp)
  }

  def host_data_model_from_json(json: JsValue): HostsDataModel = {
    val key = (json \ "key").as[String]
    val ts = (json \ "ts").as[String]
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
    val stats = (json \ "payload" \ "cpu_stats").as[Seq[Float]]

    new HostsDataModel(key, hostname, timestamp, usage, processes, cores, memoryTotal,
      memoryUsed, platform, machine, version, diskTotal, diskFree, stats, ts)
  }

  def log_data_model_from_json(json: JsValue): LogDataModel = {
    val key = (json \ "key").as[String]
    val ts = (json \ "ts").as[String]
    val message = (json \ "payload" \ "message").as[String]
    val host = (json \ "host").as[String]

    new LogDataModel(key, host, message, ts)
  }

  def process_data_model_from_json(json: JsValue): ProcessDataModel = {
    val key = (json \ "key").as[String]
    val ts = (json \ "ts").as[String]
    val host = (json \ "host").as[String]
    val pid = (json \ "payload" \ "pid").as[Int]
    val usage = (json \ "payload" \ "usage").as[Float]

    new ProcessDataModel(key, host, pid, usage, ts)
  }
}
