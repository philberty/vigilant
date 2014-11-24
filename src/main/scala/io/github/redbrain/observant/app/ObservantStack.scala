package io.github.redbrain.observant.app

import org.scalatra._
import scalate.ScalateSupport

trait ObservantStack extends ScalatraServlet with ScalateSupport {

  notFound {
    resourceNotFound()
  }

}
