package io.github.redbrain.observant.backends

import io.github.redbrain.observant.aggregator.{StatsAggregator, StatsObserver}
import io.github.redbrain.observant.models.{LogDataModel, ProcessDataModel, HostsDataModel}

/**
 * Created by redbrain on 15/12/2014.
 */
trait Backend extends StatsObserver {

  def start(): Unit = {
    StatsAggregator.registerHostStatObsever(this)
    StatsAggregator.registerLogStatObserver(this)
    StatsAggregator.registerProcStatObserver(this)
  }

  def stop(): Unit = {
    StatsAggregator.unregisterHostStatObserver(this)
    StatsAggregator.unregisterLogStatObserver(this)
    StatsAggregator.unregisterProcStatObserver(this)
  }

  override def observedHostStat(data: HostsDataModel): Unit = {}

  override def observedProcStats(data: ProcessDataModel): Unit = {}

  override def observedLogStat(data: LogDataModel): Unit = {}

}
