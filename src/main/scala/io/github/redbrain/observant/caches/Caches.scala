package io.github.redbrain.observant.caches

import io.github.redbrain.observant.models._

object HostCache extends MapCache[HostsDataModel] {}

object LogCache extends MapCache[LogDataModel] {}

object ProcCache extends MapCache[ProcessDataModel] {

  def getProcessesRunningOnHost(key: String): List[String] = {
    var procsRunningOnHost:List[String] = List[String]()
    getKeys().foreach(p => {
      val data = getCacheDataForKey(p)
      if ((data.length > 0) && (data(0).host == key)) {
        procsRunningOnHost ::= data(0).key
      }
    })
    procsRunningOnHost
  }
}
