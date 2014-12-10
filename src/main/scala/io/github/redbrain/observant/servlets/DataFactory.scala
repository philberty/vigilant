package io.github.redbrain.observant.servlets

import java.util.Calendar
import java.util.Date

trait DataFactory {

  def isDataAliveForTimeout(timestamp: Date, timeout: Int): Boolean  = {
    val now = Calendar.getInstance().getTime()
    val seconds = (now.getTime() - timestamp.getTime()) / 1000
    if (seconds >= timeout) false else true
  }

}
