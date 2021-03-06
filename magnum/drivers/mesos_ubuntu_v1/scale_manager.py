# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from marathon import MarathonClient

from magnum.conductor.scale_manager import ScaleManager


class MesosScaleManager(ScaleManager):
    """When scaling a mesos cluster, MesosScaleManager will inspect the

    nodes and find out those with containers on them. Thus we can
    ask Heat to delete the nodes without containers. Note that this
    is a best effort basis -- Magnum doesn't have any synchronization
    with Marathon, so while Magnum is checking for the containers to
    choose nodes to remove, new containers can be deployed on the
    nodes to be removed.
    """

    def __init__(self, context, osclient, cluster):
        super(MesosScaleManager, self).__init__(context, osclient, cluster)

    def _get_hosts_with_container(self, context, cluster):
        marathon_client = MarathonClient(
            'http://' + cluster.api_address + ':8080')
        hosts = set()
        for task in marathon_client.list_tasks():
            hosts.add(task.host)

        return hosts
