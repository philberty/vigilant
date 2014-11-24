import io.github.redbrain.observant.aggregator.udp.Transport
import io.github.redbrain.observant.app._
import org.scalatra._
import javax.servlet.ServletContext

import org.slf4j.LoggerFactory

class ScalatraBootstrap extends LifeCycle {

  val logger = LoggerFactory.getLogger(getClass)
  var _aggregator:Transport = null

  override def init(context: ServletContext) {

    _aggregator = new Transport(8080)
    _aggregator.start()

    logger.info("Loading Hosts Servlet")
    context.mount(new HostResourceServlet, "/hosts")

  }

  override def destroy(context: ServletContext) {
    logger.info("Shutting Down Observant Data Service")
    _aggregator.close()
  }
}
