package vigilant.datastore.controllers.swagger

import org.scalatra.ScalatraServlet
import org.scalatra.swagger.{ApiInfo, NativeSwaggerBase, Swagger}

class ResourcesApp(implicit val swagger: Swagger) extends ScalatraServlet with NativeSwaggerBase

object StatsApiInfo extends ApiInfo(
  "Vigilant Stats API",
  "Docs for the Stats API",
  "http://vigilantlabs.co.uk",
  "support@vigilantlabs.co.uk",
  "License Type",
  "License URL")

class StatsSwagger extends Swagger(Swagger.SpecVersion, "1.0.0", StatsApiInfo)