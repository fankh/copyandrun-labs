package lab;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;

/** 연습용 코드입니다. 일부러 취약하게 만들었으므로 실제 서비스에 쓰지 않습니다. */
public class FileService {
    private final String base;

    public FileService(String base) {
        this.base = base;
    }

    public String read(String fileName) throws IOException {
        File f = new File(base, fileName);
        return new String(Files.readAllBytes(f.toPath()), StandardCharsets.UTF_8);
    }
}
