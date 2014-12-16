package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.aggregator.{StatsAggregator, StatsObserver}
import io.github.redbrain.observant.models.{HostsDataModel, LogDataModel, ProcessDataModel}
import org.scalatra.atmosphere._

object StatType extends Enumeration {
  type T = Value
  val LOG, PROC, HOST = Value
}

class AtmosphereStatsClientMonitor(val key:String, val T:StatType.T) extends AtmosphereClient with StatsObserver {

  override def receive: AtmoReceive = {
    case Connected =>
      T match {
        case StatType.LOG => StatsAggregator.registerLogStatObserver(this)
        case StatType.HOST => StatsAggregator.registerHostStatObsever(this)
        case StatType.PROC => StatsAggregator.registerProcStatObserver(this)
      }
    case Disconnected(disconnector, Some(error)) =>
      T match {
        case StatType.LOG => StatsAggregator.unregisterLogStatObserver(this)
        case StatType.HOST => StatsAggregator.unregisterHostStatObserver(this)
        case StatType.PROC => StatsAggregator.unregisterProcStatObserver(this)
      }
  }

  def observedHostStat(data: HostsDataModel) {}
  def observedProcStats(data: ProcessDataModel) {}
  def observedLogStat(data: LogDataModel) {}
}