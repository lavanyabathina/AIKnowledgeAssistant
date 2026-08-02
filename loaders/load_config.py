import yaml
from loaders.webdocument_loader import *
from loaders.localdocument_loader import *



def load_config(configFile) -> dict[str, any]:
    with open(configFile) as f:
        config=yaml.safe_load(f)
    return config


    



  
  
   
    
    
   