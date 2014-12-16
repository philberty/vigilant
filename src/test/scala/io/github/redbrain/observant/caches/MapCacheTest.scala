package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.caches.MapCache
import org.scalatest.FunSuiteLike
import org.scalatra.test.scalatest.ScalatraSuite

class MapCacheTest extends ScalatraSuite with FunSuiteLike {

  class TestClass extends MapCache[Int]

  test("That pushing new data with key is available in the cache key set") {
    val mockMapCache = new TestClass
    mockMapCache.pushDataForKey("test", 1)
    assert(mockMapCache.getHostKeys().contains("test"))
  }

}