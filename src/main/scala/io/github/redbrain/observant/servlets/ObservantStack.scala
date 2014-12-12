package io.github.redbrain.observant.servlets

import org.scalatra._
import org.scalatra.scalate.ScalateSupport

trait ObservantStack extends ScalatraServlet with ScalateSupport {

  notFound {
    resourceNotFound()
  }

}
