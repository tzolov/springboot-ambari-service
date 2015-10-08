"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys, os, pwd, grp, signal, time, glob
from resource_management import *
from subprocess import call

"""
The Spring Boot application has to be complied with SpringBoot 1.3+ to leverage the Linux init.d support: http://bit.ly/1WMBHC5
- On installation the spring boot application jar is linked as an init.d service enabling the start/stop/status/restart init.d operations 
- The execution environment is configured through a application-env.xml. It follows the customizing the startup script instructions: http://bit.ly/1MYUvcM
- The application is configured through the application-site.xml file. All properties defined in the application-site.xml are converted into application.properties key/value entries.  
"""
class Master(Script):

    def install(self, env):
        import params
        env.set_params(params)   

        # Install the osSpecifics binary packages
        self.install_packages(env)    
        
        # Create spring boot application user and group (if they don't exist)
        try: grp.getgrnam(params.group)
        except KeyError: Execute(format('groupadd {group}')) 
                
        try: pwd.getpwnam(params.user)
        except KeyError: Execute(format('adduser {user} -g {group}'))
        
        # Create the log dir if it not already present        
        Directory([os.path.join(params.pid_dir, params.application_name), params.log_dir, params.install_dir],
                  owner=params.user,
                  group=params.group,
                  recursive=True)
        
        # Initialize the log file
        File(params.log_file, owner=params.user, group=params.group)    
        
        # Fetch application jar build, if no cached
        if not os.path.exists(params.install_jar_path):
            # Move the spring boot application executable jar into the target install dir
            Execute(format('cp {application_jar_path} {install_jar_path} >> {log_file}'),
                    user=params.user,
                    group=params.group)
            # Make the jar executable so to used it as a Linux service. 
            # http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#deployment-service
            Execute(format('chmod a+x {install_jar_path}'), user=params.user)
            # Make spring boot application jar  a /etc/init.d service 
            Link(format('/etc/init.d/{application_name}'), to=params.install_jar_path)
        
        # Update the configs specified by user
        self.configure(env)
        
    def configure(self, env):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)
        
        # Generate SpringBoot applicaiton.properties file. Fill in the properties form form the
        # <app name>-application-site.xml 
        File(params.application_properties_path,
             content=Template("application.properties.j2", configurations=params.application_site),
             owner=params.user,
             group=params.group)
        
        # Create application SpringBoot configuration file:
        # http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#deployment-script-customization
        File(status_params.spring_boot_config_path,
             content=InlineTemplate(status_params.spring_boot_config_content),
             owner=params.user,
             group=params.group) 

    def start(self, env):
        import params
        env.set_params(params)
        
        # Update the configs specified by user
        self.configure(env)
                
        # Service(params.application_name, action="start")   
        Execute (format('/etc/init.d/{application_name} start'),
                 user=params.user,
                 group=params.group,
                 logoutput=True,
                 timeout=300)      

    def stop(self, env):
        import params
        env.set_params(params)
        
        Execute(format('kill -9 + $(cat {pid_file} ) >> {log_file}'), user=params.user)

    def status(self, env):
        import status_params
        env.set_params(status_params)               
        check_process_status(status_params.pid_file)
              
if __name__ == "__main__":
  Master().execute()
