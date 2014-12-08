package io.github.redbrain.observant.caches

import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.models.ProcessDataModel

/**
 * Created by redbrain on 02/12/2014.
 */
object ProcessCache {

  private var _cache:Map[String, List[ProcessDataModel]] = Map[String, List[ProcessDataModel]]()

  def getCacheDataForKey(key: String): List[ProcessDataModel] = {
    _cache.get(key) match {
      case None => List()
      case Some(data) => data
    }
  }

  def getHostKeys(): Set[String] = {
    _cache.keySet
  }

  def pushDataForKey(key: String, data: ProcessDataModel): Unit = {
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
