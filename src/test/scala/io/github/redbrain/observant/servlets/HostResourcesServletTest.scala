package io.github.redbrain.observant.servlets

import io.github.redbrain.observant.servlets.HostResourceServlet
import org.scalatest.FunSuiteLike
import org.scalatra.test.scalatest._

class HostResourcesServletTest extends ScalatraSuite with FunSuiteLike {
  // `HelloWorldServlet` is your app which extends ScalatraServlet
  addServlet(classOf[HostResourceServlet], "/hosts/*")

  test("simple get") {
    get("/hosts/keys") {
      status should equal (200)
    }
  }
}