import io.github.redbrain.observant.app._
import org.scalatra._
import javax.servlet.ServletContext

import org.slf4j.LoggerFactory

class ScalatraBootstrap extends LifeCycle {

  val logger =  LoggerFactory.getLogger(getClass)

  override def init(context: ServletContext) {

    logger.info("Loading Hosts Servlet")
    context.mount(new HostResourceServlet, "/hosts")

  }

  override def destroy(context: ServletContext) {
    logger.info("Shutting Down Observant Data Service")
  }
}
