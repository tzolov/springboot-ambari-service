# Create Ambari Services from Spring Boot Applications

Toolkit to bundle any [Spring Boot](http://projects.spring.io/spring-boot) application into an [Ambari Service](https://ambari.apache.org/). This allows Ambari to provision, manage and monitor the target spring boot applications, providing blueprint automation and versioned configuration management. 

To use the toolkit, copy the target spring boot application jar into the `lib` directory, set the name and the version of the generated Ambari Service and define the application properties to be managed by Ambari. Next the springboot-ambari-service toolkit generates an Ambari Service and RPMs to install it in the Ambari Server. Once installed you can use the Ambari Wizard or the Blueprint API to deploy the spring boot app as a native Ambari Service.

### Quick Start
Follow the instructions to bundle a Spring Boot application into an Ambari Service:

1) (Re)build your Spring Boot application using Spring Boot 1.3+ (e.g [1.3.0.M5](http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#getting-started-installation-instructions-for-java) or [1.3.0.BUILD-SNAPSHOT](http://docs.spring.io/spring-boot/docs/1.3.0.BUILD-SNAPSHOT/reference/htmlsingle/#getting-started-installation-instructions-for-java)) and enable the [maven/gradle plugin executable configuration](http://docs.spring.io/spring-boot/docs/1.3.0.BUILD-SNAPSHOT/reference/htmlsingle/#deployment-install) to produce [fully executable jar](http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#deployment-install).

2) Clone the [springboot-ambari-service](https://github.com/tzolov/springboot-ambari-service) project
```
git clone https://github.com/tzolov/springboot-ambari-service.git
```

3) Copy the spring boot application jar (build in step 1) into the `src/main/resources/services/package/lib` folder. 

4) Edit the build.gradle file and set the `applicationName`, `ambariServicerVersion` and `displayName` properties.

5) Edit the `src/main/resources/services/configuration/application-site.xml` to set all application and system properties to be exposed (e.g. the `applicaton.properties` entires)

6) Build the springboot-ambari-service RPMs. The springboot-ambari-service does all the plumbing
```
./gradlew clean dist
```

7) Copy the appropriate rpm (-phd30, -hdp22 or -hdp23) from `build/distribution` to the Ambari server node.
```
scp build/distributions/springboot-app-ambari-service-phd30-0.0.10-1.noarch.rpm
ambari@ambari.server.node:
```

8) On the Ambari node Install the rpm plugin and restart the Ambari server: 
```
sudo yum -y install ./springboot-app-ambari-service-phd30-0.0.10-1.noarch.rpm 
sudo /etc/init.d/ambari-server restart
```
