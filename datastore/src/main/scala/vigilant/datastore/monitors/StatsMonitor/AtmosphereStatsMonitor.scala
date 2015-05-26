package vigilant.datastore.monitors.StatsMonitor

import org.scalatra.atmosphere._
import vigilant.datastore.models.{ProcessDataModel, LogDataModel, HostsDataModel, StatType}
import vigilant.datastore.services.aggregator.{AggregatorService, StatsObserver}

class AtmosphereStatsMonitor(val key:String, val T:StatType.T) extends AtmosphereClient with StatsObserver {

  override def receive: AtmoReceive = {
    case Connected =>
      T match {
        case StatType.LOG => AggregatorService.registerLogStatObserver(this)
        case StatType.HOST => AggregatorService.registerHostStatObsever(this)
        case StatType.PROC => AggregatorService.registerProcStatObserver(this)
      }
    case Disconnected(disconnector, Some(error)) =>
      T match {
        case StatType.LOG => AggregatorService.unregisterLogStatObserver(this)
        case StatType.HOST => AggregatorService.unregisterHostStatObserver(this)
        case StatType.PROC => AggregatorService.unregisterProcStatObserver(this)
      }
  }

  def observedHostStat(data: HostsDataModel) {}
  def observedProcStats(data: ProcessDataModel) {}
  def observedLogStat(data: LogDataModel) {}
}