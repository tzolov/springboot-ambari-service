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
import sys, os
import status_params
from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default

# server configurations
config = Script.get_config()

###############################################################################
#      User Space 
###############################################################################

# Add your properties here

###############################################################################
#      Do not modify the properties in the section below!
###############################################################################

#  Mirror the Spring Boot environment settings   
application_name = status_params.application_name
user = status_params.user.lower()
group = status_params.group.lower()
pid_dir = status_params.pid_dir
pid_file = status_params.pid_file
log_dir = status_params.log_dir
log_file = status_params.log_file
install_dir = status_params.install_dir
install_jar_path = status_params.install_jar_path

# The absolute path of the target application.properties file
application_properties_path = os.path.join(install_dir, 'application.properties')

# Absolute path of the spring boot application jar file before it is moved to the install 
application_jar_path =  os.path.join(os.path.dirname(__file__), '..', 'lib', '@APPLICATION_JAR_NAME@')

application_site = default("/configurations/" + application_name + "-site", None)
#application_site = config['configurations'][application_name + '-site']

# ambari_host = str(config['clusterHostInfo']['ambari_server_host'][0])
