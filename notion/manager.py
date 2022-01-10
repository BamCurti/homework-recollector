import json
import requests
from typing import Dict

printf = lambda h: print(json.dumps(h, indent=4))

def read_secrets(dir: str):
    """This function reads an external JSON which contains all the necessary secrets for working.

    Returns:
        dict: contains url and token.
    """
    with open(dir) as JF:
        secrets = json.load(JF)
        
    return secrets

def get_uploaded_homework() -> Dict:
    """This function interacts with the Notion API that returns all the pages that I have in my DB.
    
    Returns:
        Dict: This dictionary contains all the pages as JSON which contains all the information about the uploaded homework in Notion.
    """
    secrets = read_secrets("notion/secrets.json")
    
    url = "https://api.notion.com/v1/search"
    headers = secrets['headers']
    
    ans = {}
    request = requests.post(url=url, headers=headers).json()
    
    
    for h in request['results']:
        if h['object'] == 'page':
            id = h['properties']['id']['number']
            ans[id] = h
        
    return ans

def search_homework(id: str) -> bool:
    """This function returns a true value if the Notion API finds a page with the same name.

    Args:
        title (str): The name of the homework.

    Returns:
        bool: This represents if the title has an appearance in the
    """
    secrets = read_secrets("notion/secrets.json")
    url = "https://api.notion.com/v1/search"
    headers = secrets['headers']
    data = {'query': str(id)}
    
    request = requests.post(url=url, headers=headers, json=data).json()
    
    return len(request['results']) != 0   

def format_page(h: Dict) -> Dict:
    """This function returns a dictionary that is formatted as is required by Notion API.

    Args:
        h (Dict): This dictionary has the necessary data for formatting, like course, due_at, html_url, 
        id and name

    Returns:
        Dict: This dictionary is formatted as Notion API needs.
    """
    database_id = read_secrets("notion/secrets.json")['database_id']
    return {
        "parent": {
            "type": "database_id",
            "database_id": database_id,
        },
        "properties": {
            "ID": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": str(h['id'])
                        }
                    }
                ]
            },
            "Name": {
                "rich_text": [
                    {
                        "type": "text",
                        "text":{ 
                            "content": h['name']
                        }
                    }
                ]
            },
            "html_url": { 
                "url": h['html_url']
            },
            "due_at": {
                "date": {
                    "start": h['due_at'],
                }
            },
            "Course": {
                 "select": {
                    "name": h['course']
                }                  
            },
            "Is done": {
                "checkbox": False
            }
        }
    }

def post_homework(h: Dict) -> None:
    """This function makes an post request to Notion API, following
    the required format.        

    Args:
        h (Dict): The homework formatted as Notion API requested.
    """
    url = "https://api.notion.com/v1/pages"
    secrets = read_secrets(dir="notion/secrets.json")
    headers = secrets['headers']
    
    request = requests.post(url=url, headers=headers, json=format_page(h))
    return request.json()
    
if __name__ == '__main__':    
    test = {
        "course": "LENGUAJES FORMALES (O2021_ESI3180E)",
        "due_at": "2021-10-20T23:59:00.000-05:00",
        "html_url": "https://iteso.instructure.com/courses/127340000000018154/assignments/12734~303128",
        "id": "TEST 1",
        "name": "TEST 1"      
    }
    post_homework(test)
    
    
    #homework = get_uploaded_homework()
    
    
    #for h in homework:
    #    printf(homework[h])