package io.github.redbrain.observant.servlets

import org.scalatest.FunSuiteLike
import org.scalatra.test.scalatest._

class HostResourcesServletTest extends ScalatraSuite with FunSuiteLike {

  addServlet(classOf[HostResourcesServlet], "/hosts/*")

  test("Getting list of host keys") {
    get("/hosts/keys") {
      status should equal (200)
    }
  }
}
