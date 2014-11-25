package io.github.redbrain.observant.caches

import io.github.redbrain.observant.configuration.ConfigurationService
import io.github.redbrain.observant.models.HostsDataModel

object HostCache {

  private var _cache:Map[String, List[HostsDataModel]] = Map[String, List[HostsDataModel]]()

  def getCacheDataForKey(key: String): List[HostsDataModel] = {
    _cache.get(key) match {
      case None => List()
      case Some(data) => data
    }
  }

  def getHostKeys(): Set[String] = {
    _cache.keySet
  }

  def pushDataForKey(key: String, data: HostsDataModel): Unit = {
    _cache.get(key) match {
      case None => {
        _cache += key -> List(data)
      }
      case Some(buffer) => {
        if (buffer.length >= ConfigurationService.getCacheThreshold()) {
          _cache += key -> (buffer.drop(1) ::: List(data))
        } else {
          _cache += key -> (buffer ::: List(data))
        }
      }
    }
  }
}
