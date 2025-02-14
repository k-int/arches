from enum import Enum, unique


IntegrityCheckDescriptions = {
    1005: "Nodes with ontologies found in graphs without ontologies",
    1012: "Node Groups without contained nodes",
    1013: "Node Groups without a grouping node",
    1014: "Publication missing for language",
}


@unique
class IntegrityCheck(Enum):
    NODE_HAS_ONTOLOGY_GRAPH_DOES_NOT = 1005
    NODELESS_NODE_GROUP = 1012
    NODEGROUP_WITHOUT_GROUPING_NODE = 1013
    PUBLICATION_MISSING_FOR_LANGUAGE = 1014

    def __str__(self):
        return IntegrityCheckDescriptions[self.value]


class ExtensionType(Enum):
    DATATYPES = "datatypes"
    ETL_MODULES = "etl_modules"
    FUNCTIONS = "functions"
    SEARCH_COMPONENTS = "search_components"
    PERMISSIONS_FRAMEWORKS = "permissions"
