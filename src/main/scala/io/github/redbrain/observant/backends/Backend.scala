package io.github.redbrain.observant.backends

import io.github.redbrain.observant.aggregator.{StatsAggregator, StatsObserver}
import io.github.redbrain.observant.models.{LogDataModel, ProcessDataModel, HostsDataModel}

/**
 * Created by redbrain on 15/12/2014.
 */
trait Backend {

  def start()

  def stop()

}
