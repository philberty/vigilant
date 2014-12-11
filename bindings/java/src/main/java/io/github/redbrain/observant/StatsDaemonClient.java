package io.github.redbrain.observant;

/**
 * Created by redbrain on 11/12/2014.
 */
public class StatsDaemonClient {

    private String lockFile;
    private String socketPath;

    public StatsDaemonClient(String lockFile, String socketPath) {
        this.lockFile = lockFile;
        this.socketPath = socketPath;
    }

    public boolean connect() {
        return true;
    }

    public void close() {

    }

    public void postLogMessage(String key, String message) {

    }

    public void postWatchPid(String key, int pid) {

    }
}
