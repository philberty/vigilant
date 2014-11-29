package io.github.redbrain.observant.aggregator

/**
 * Created by redbrain on 25/11/2014.
 */
trait TransportType {

  /* Non-blocking function to start the transport */
  def start();

  /* Function to dealloc the transport */
  def close();

}
