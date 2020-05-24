package genefinder;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class FileResource {
    private final String data;

    public FileResource(String filename) {
        try {
            InputStream is = new FileInputStream(filename);
            try (BufferedReader buff = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))) {
                StringBuilder contents = new StringBuilder();
                String line;
                while ((line = buff.readLine()) != null) {
                    contents.append(line).append("\n");
                }
                this.data = contents.toString();
            } catch (Exception e) {
                throw new ResourceException("FileResource: error encountered reading " + filename, e);
            }

        }
        catch (Exception e) {
            throw new ResourceException("FileResource: cannot access " + filename);
        }
    }

    public String getData() {
        return data;
    }
}

class ResourceException extends RuntimeException {
    public static final long serialVersionUID = 1L;

    public ResourceException (String message) {
        super(message);
    }

    public ResourceException (String message, Throwable cause) {
        super(message, cause);
    }
}