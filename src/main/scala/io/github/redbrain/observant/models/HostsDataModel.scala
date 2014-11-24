package io.github.redbrain.observant.models

import play.api.libs.json._

/**
 * Created by redbrain on 24/11/2014.
 */
object HostsDataModel {

  def getCachedDataForKey(key: String): JsArray = {
    null
  }

  def getKeys(): List[String] = {
    List("Test", "test2")
  }

  def pushData(json: JsValue): Unit = {

  }
}
