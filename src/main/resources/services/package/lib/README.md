# Your Spring Boot Application Jar

The `lib` folder contains the target application jar to be wrapped as Ambari Service. Exactly one jar file can contained!
 
Current version of the `springboot-ambari-service` leverages the Spring Boot 1.3+ feature to make fully executable applications for Unix systems (Linux, OSX, FreeBSD etc). Therefore the application jat has to be (re)build with Spring Boot 1.3+ or newer (e.g [1.3.0.M5](http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#getting-started-installation-instructions-for-java) or [1.3.0.BUILD-SNAPSHOT](http://docs.spring.io/spring-boot/docs/1.3.0.BUILD-SNAPSHOT/reference/htmlsingle/#getting-started-installation-instructions-for-java)). Also the build configuration must set the [maven/gradle plugin executable configuration](http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#deployment-install) to generate fully executable jars.

