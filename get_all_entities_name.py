import json

json_path = r"E:\Practice\krr\KRR_Project\entity_subsumers.json"

def get_parent_entities():
    """
    Returns a list of parent entities (top-level keys)
    from entity_subsumers.json
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return list(data.keys())


# Example usage
if __name__ == "__main__":
    parents = get_parent_entities()
    print(parents)
