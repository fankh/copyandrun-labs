FROM maven:3.9-eclipse-temurin-21
RUN mvn -q dependency:copy -Dartifact=com.h2database:h2:2.2.224 -DoutputDirectory=/opt/lib
WORKDIR /app
COPY *.java /app/
RUN javac -encoding UTF-8 -cp /opt/lib/h2-2.2.224.jar -d /app/out *.java
CMD ["java", "-Dfile.encoding=UTF-8", "-cp", "/app/out:/opt/lib/h2-2.2.224.jar", "App"]
