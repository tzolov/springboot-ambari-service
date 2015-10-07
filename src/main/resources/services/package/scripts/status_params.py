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
from resource_management import *
import sys, os

config = Script.get_config()

application_name = '@APPLICATION_NAME@'

app_env = config['configurations'][application_name + '-env']

user = app_env['user']
group = app_env['group']

pid_dir = app_env['pid_dir']
pid_file = os.path.join(pid_dir, application_name, application_name + '.pid')
 
java64_home = config['hostLevelParams']['java_home']
java_opts = app_env['java_opts']

log_dir = os.path.join(app_env['log_dir'], application_name)
log_file = os.path.join(log_dir, application_name + '-setup.log')

# Application specific properties
install_dir = os.path.join(app_env['install_dir'], application_name)
install_jar_path = os.path.join(*[install_dir, application_name + '.jar'])

spring_boot_config_content = app_env['spring_boot_config_content']
spring_boot_config_path = os.path.join(install_dir, application_name + '.conf')
