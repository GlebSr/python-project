from typing import Dict, Any

def to_dict_with_id(data: Dict[str, Any]) -> Dict[str, Any]:
    data['id'] = str(data['_id'])
    return data