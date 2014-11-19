package io.github.observant;

import io.github.observant.services.web.WebServer;

/**
 * Created by redbrain on 19/11/2014.
 */
public class ObservantServerMain {
    public static void main(String []args) {

        WebServer server = new WebServer("localhost", 8888);
        server.run();

    }
}
