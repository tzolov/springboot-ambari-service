# Wrap Spring Boot application as an Ambari Service

This project makes it easy to wrap any Spring Boot application as an Ambari Service and enable Ambari to provision, manage and monitor the application.

To use the springboot-ambari-service, copy the target spring boot app jar into project’s lib directory, set the name and the version of the new Ambari Service and define the application properties to be exposed and managed by Ambari. With this set springboot-ambari-service builds service Rpm ready to install on the Ambari Server node. Then Ambari can provision, manage monitor the spring boot app as a native Ambari Service.

Following detail instructions will walk you through the steps of wrapping an spring boot application into Ambari Service:

* (Re)build the Spring Boot application using Spring Boot 1.3+ or newer  (e.g [1.3.0M5](http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#getting-started-installation-instructions-for-java) or [1.3.0.BUILD-SNAPSHOT](http://docs.spring.io/spring-boot/docs/1.3.0.BUILD-SNAPSHOT/reference/htmlsingle/#getting-started-installation-instructions-for-java)) to make fully executable applications for Unix systems (Linux, OSX, FreeBSD etc). Enable the [maven/gradle plugin executable configuration]((http://docs.spring.io/spring-boot/docs/1.3.0.BUILD-SNAPSHOT/reference/htmlsingle/#deployment-install)) to generate `fully executable jars`.
* Clone the springboot-ambari-service project
```
git clone https://github.com/tzolov/springboot-ambari-service.git
```
* Copy the spring boot application jar (build in step 1) into the _src/main/resources/services/package/lib_ folder. 
* Edit the build.gradle file and set the *applicationName*, *ambariServicerVersion* and *displayName* properties.
* Edit the _src/main/resources/services/configuration/application-site.xml_ to set all application and system properties to be exposed (e.g. the _applicaton.properties_ entires)
* Build the springboot-ambari-service RPMs. The springboot-ambari-service does all the plumbing
```
./gradlew clean dist
```
* Copy the appropriate rpm (-phd30, -hdp22 or -hdp23) from build/distribution to the Ambari server node.
```
scp build/distributions/springboot-app-ambari-service-phd30-0.0.10-1.noarch.rpm
ambari@ambari.server.node:
```

* On the Ambari node Install the rpm plugin and restart the Ambari server: 
```
sudo yum -y install ./springboot-app-ambari-service-phd30-0.0.10-1.noarch.rpm 
sudo /etc/init.d/ambari-server restart
```
