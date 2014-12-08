package io.github.redbrain.observant.caches

import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.models.LogDataModel

/**
 * Created by redbrain on 02/12/2014.
 */
object LogCache {

  private var _cache:Map[String, List[LogDataModel]] = Map[String, List[LogDataModel]]()

  def getCacheDataForKey(key: String): List[LogDataModel] = {
    _cache.get(key) match {
      case None => List()
      case Some(data) => data
    }
  }

  def getHostKeys(): Set[String] = {
    _cache.keySet
  }

  def pushDataForKey(key: String, data: LogDataModel): Unit = {
    _cache.get(key) match {
      case None => {
        _cache += key -> List(data)
      }
      case Some(buffer) => {
        if (buffer.length >= Configuration.getCacheThreshold()) {
          _cache += key -> (buffer.drop(1) ::: List(data))
        } else {
          _cache += key -> (buffer ::: List(data))
        }
      }
    }
  }
}
