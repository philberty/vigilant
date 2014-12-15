package io.github.redbrain.observant.backends

import io.github.redbrain.observant.aggregator.{StatsAggregator, StatsObserver}
import io.github.redbrain.observant.models.{ProcessDataModel, LogDataModel, HostsDataModel}


class MongoBackend extends Backend with StatsObserver {

  override def start(): Unit = {
    StatsAggregator.registerHostStatObsever(this)
    StatsAggregator.registerLogStatObserver(this)
    StatsAggregator.registerProcStatObserver(this)
  }

  override def stop(): Unit = {
    StatsAggregator.unregisterHostStatObserver(this)
    StatsAggregator.unregisterLogStatObserver(this)
    StatsAggregator.unregisterProcStatObserver(this)
  }

  override def observedProcStats(data: ProcessDataModel): Unit = {

  }

  override def observedLogStat(data: LogDataModel): Unit = {

  }

  override def observedHostStat(data: HostsDataModel): Unit = {

  }
}
