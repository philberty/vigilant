package io.github.redbrain.observant.aggregator

import io.github.redbrain.observant.models._

trait StatsObserver {
  def observedHostStat(data: HostsDataModel)
  def observedProcStats(data: ProcessDataModel)
  def observedLogStat(data: LogDataModel)
}
