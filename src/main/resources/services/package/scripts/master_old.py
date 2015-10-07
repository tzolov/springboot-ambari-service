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

class Master(Script):

    def install(self, env):
        import params
        env.set_params(params)   

        # Install the osSpecifics
        self.install_packages(env)    
        
        # Create user and group if they don't exist
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
            # Download the application executable jar
            # Execute(format('wget {jar_download_url} -O {install_jar_path} -a {log_file}'), user=params.user)              
            Execute(format('cp {service_jar_path} {install_jar_path} >> {log_file}'), 
                    user=params.user, 
                    group=params.group)
            # Make the jar executable so it can be used as a Linux service. 
            # http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#deployment-service
            Execute(format('chmod a+x {install_jar_path}'), user=params.user)
            # Make spring boot application jar  a /etc/init.d service 
            Link(format('/etc/init.d/{application_name}'), to=params.install_jar_path)
        
        # Update the configs specified by user
        self.configure(env)
        
    def configure(self, env):
        import params
        env.set_params(params)
        
#         File(params.application_properties_filepath,
#              owner=params.user,
#              group=params.group,
#              content=InlineTemplate(params.application_properties_content)) 

        File(params.application_properties_filepath,
             content=Template("application.properties.j2", 
                              configurations = params.application_site_dict),
             owner=params.user,
             group=params.group
        )

        #File(params.application_properties_filepath,
        #     content=Template("application.properties.old.j2"),
        #     owner=params.user,
        #     group=params.group
        #)
        
        # Create application configuraiton file (/opt/<application_name>)
        # http://docs.spring.io/spring-boot/docs/1.3.0.M5/reference/htmlsingle/#deployment-script-customization
        File(params.config_file,
             owner=params.user,
             group=params.group,
             content=InlineTemplate(params.application_config_content)) 

    def start(self, env):
        import params
        env.set_params(params)
        
        # Update the configs specified by user
        self.configure(env)
                
        #Service(params.application_name, action="start")   
        Execute (format('/etc/init.d/{application_name} start'), 
                 user=params.user, 
                 group=params.group,
                 logoutput=True, 
                 timeout=300)      

    def stop(self, env):
        import params
        env.set_params(params)
        
        Execute(format('kill -9 + $(cat {pid_file} ) >> {log_file}'), user=params.user)
        #Execute (format('/etc/init.d/{application_name} stop'), user=params.user, group="hadoop", logoutput=True, timeout=300)

    def status(self, env):
        import status_params
        env.set_params(status_params)               
        check_process_status(status_params.pid_file)
        #Execute (format('/etc/init.d/{application_name} status'), user=status_params.user)
              
if __name__ == "__main__":
  Master().execute()
