import io.github.redbrain.observant.aggregator.TransportType
import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.servlets._

import org.scalatra._
import javax.servlet.ServletContext

import org.slf4j.LoggerFactory

class ScalatraBootstrap extends LifeCycle {

  private val logger = LoggerFactory.getLogger(getClass)
  private var _aggregator:TransportType = null

  override def init(context: ServletContext) {
    Configuration.loadConfiguration()
    logger.info("Configuration Loaded")

    _aggregator = Configuration.getTransportFromConfiguration()
    logger.info("Stats Aggregator Ready")

    _aggregator.start()
    logger.info("Aggregator Started")

    logger.info("Loading data Servlet")
    context.mount(new StatsApiServlet, "/api")

    logger.info("Loading State Servlet")
    context.mount(new DataStoreStateServlet, "/state")

    logger.info("Ready...")
  }

  override def destroy(context: ServletContext) {
    logger.info("Shutting Down Observant Data Service")
    _aggregator.close()
  }
}
