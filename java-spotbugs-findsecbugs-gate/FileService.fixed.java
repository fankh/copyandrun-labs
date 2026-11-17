package lab;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class FileService {
    private final Path base;

    public FileService(String base) {
        this.base = Path.of(base).toAbsolutePath().normalize();
    }

    public String read(String fileName) throws IOException {
        Path target = base.resolve(fileName).normalize();
        if (!target.startsWith(base)) {
            throw new IOException("허용된 폴더 밖의 경로입니다");
        }
        return new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
    }
}
