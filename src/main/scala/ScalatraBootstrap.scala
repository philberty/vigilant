import io.github.redbrain.observant.aggregator.TransportType
import io.github.redbrain.observant.app._
import io.github.redbrain.observant.configuration.Configuration
import io.github.redbrain.observant.servlets.HostResourceServlet
import org.scalatra._
import javax.servlet.ServletContext

import org.slf4j.LoggerFactory

class ScalatraBootstrap extends LifeCycle {

  private val logger = LoggerFactory.getLogger(getClass)
  private var _aggregator:TransportType = null

  override def init(context: ServletContext) {
    _aggregator = Configuration.getTransportFromConfiguration()
    _aggregator.start()

    logger.info("Loading Hosts Servlet")
    context.mount(new HostResourceServlet, "/hosts")
  }

  override def destroy(context: ServletContext) {
    logger.info("Shutting Down Observant Data Service")
    _aggregator.close()
  }
}
