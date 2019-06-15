print("settings.py :: You may disable/enable inserting data in Fuseki / Elastic [DEBUG / INFO]") 

import ontologyAPI.ontology_api as ontology
import elasticSearch.elasticSearch_api as elastic

# ontology.insert_artontology() # COMMENT TO DISABLE
elastic.create_clean_index() # COMMENT TO DISABLE