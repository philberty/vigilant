package io.github.redbrain.observant.caches

import io.github.redbrain.observant.configuration.Configuration

trait StatsDataCache[T] {
  private var _cache:Map[String, List[T]] = Map[String, List[T]]()

  def getCacheDataForKey(key: String): List[T] = {
    _cache.get(key) match {
      case None => List()
      case Some(data) => data
    }
  }

  def getHostKeys(): Set[String] = {
    _cache.keySet
  }

  def pushDataForKey(key: String, data: T): Unit = {
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
