package vigilant.datastore.caches

import vigilant.datastore.caches.buffer.Cache
import vigilant.datastore.models.ProcessDataModel
import vigilant.datastore.services.configuration.ConfigurationService

object ProcCache extends Cache[ProcessDataModel](ConfigurationService.cache_threshold) {

  /* return process keys for host */
  def process_keys_on_host(key: String): Set[String] = {
    var procs = Set[String]()
    keys.foreach(p => {
      headForKey(p) match {
        case Some(data) =>
          if (data.host == key) {
            procs += p
          }
        case _ =>
      }
    })
    procs
  }

  /* return head process data for host */
  def process_head_for_host(host: String): Set[ProcessDataModel] = {
    var procs = Set[ProcessDataModel]()
    process_keys_on_host(host).foreach(k => {
      headForKey(k) match {
        case Some(data) => procs += data
        case _ =>
      }
    })
    procs
  }

}