import json

a = 2
def read_secrets(dir: str):
    """This function reads an external JSON which contains all the necessary secrets for working.

    Returns:
        dict: contains url and token.
    """
    with open(dir) as JF:
        secrets = json.load(JF)
        
    return secrets

if __name__ == '__main__':
    print(read_secrets("canvas/secrets.json"))