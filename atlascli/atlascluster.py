import pprint
from typing import Dict
from atlascli.atlasresource import AtlasResource
from atlascli.atlasapi import AtlasAPI

class AtlasCluster(AtlasResource):

    @classmethod
    def default_single_region_cluster(cls):
        return {
          #"name" : "DataStore",
          "diskSizeGB" : 100,
          "numShards" : 1,
          "providerSettings" : {
            "providerName" : "AWS",
            "diskIOPS" : 300,
            "instanceSizeName" : "M40",
            "regionName" : "US_EAST_1"
          },
          "replicationFactor" : 3,
          "autoScaling":{"diskGBEnabled":True},
        }

    def __init__(self, api:AtlasAPI, project_id:str, cluster:Dict):
        self._project_id = project_id
        super().__init__(api, cluster)


    @classmethod
    def get_cluster(cls, api:AtlasAPI, project_id:str, cluster_name:str):
        cluster = api.get_one_cluster(project_id, cluster_name)
        o = cls(api, project_id, cluster)

    @property
    def cluster_id(self):
        return self._project_id
        
    def is_paused(self):
        return self.resource["paused"]

    def pause(self):
        self.resource = self._api.pause(self._project_id, self.name)
        return self.resource


    def resume(self):
        self.resource = self._api.resume(self._project_id, self.name)
        return self.resource

    def __str__(self):
        return f"{pprint.pformat(self.resource)}"

