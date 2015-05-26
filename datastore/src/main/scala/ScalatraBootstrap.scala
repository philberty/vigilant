import java.io.{File, IOException}
import javax.servlet.ServletContext

import _root_.akka.actor.ActorSystem
import org.scalatra._
import org.slf4j.LoggerFactory
import vigilant.datastore.controllers.StatsController
import vigilant.datastore.controllers.swagger.{StatsSwagger, ResourcesApp}
import vigilant.datastore.services.aggregator.AggregatorService
import vigilant.datastore.services.configuration.ConfigurationService
import vigilant.datastore.services.database.DatabaseService
import vigilant.datastore.services.transports.TransportService
import vigilant.datastore.services.triggers.TriggersService

class ScalatraBootstrap extends LifeCycle {

  val system = ActorSystem()
  val logger = LoggerFactory.getLogger(getClass)
  implicit val swagger = new StatsSwagger

  override def init(context: ServletContext) {
    val configHome = System.getenv("VIGILANT_HOME")
    if (configHome == null) {
      throw new IOException("Unable to find [VIGILANT_HOME]/vigilant.json")
    }

    ConfigurationService.load_configuration_from_file(new File(new File(configHome), "vigilant.json").getPath)
    logger.info("Configuration Loaded")

    AggregatorService.actor = system.actorOf(AggregatorService.props)
    logger.info("Started Stats Aggregator Service")

    DatabaseService.actor = system.actorOf(DatabaseService.props)
    DatabaseService.start()
    logger.info("Started Database Service")

    TriggersService.actor = system.actorOf(TriggersService.props)
    TriggersService.start()
    logger.info("Started Triggers Service")

    TransportService.setTransport(
      system.actorOf(ConfigurationService.transport_actor),
      ConfigurationService.transport)
    TransportService.start()
    logger.info("Started Transport Service")

    context.mount(new StatsController, "/api", "api")
    context.mount(new ResourcesApp, "/api-doc")
    logger.info("Restful Controllers ready")
  }

  override def destroy(context: ServletContext) {
    logger.info("Shutting Down Observant Data Service")
    TransportService.stop()
    TriggersService.stop()
    DatabaseService.stop()
    system.shutdown()
  }
}
