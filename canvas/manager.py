import requests
import json
from typing import List, Dict
from datetime import datetime, timedelta

def read_secrets(dir: str):
    """This function reads an external JSON which contains all the necessary secrets for working.

    Returns:
        dict: contains url and token.
    """
    with open(dir) as JF:
        secrets = json.load(JF)
        
    return secrets

def get_courses() -> List:
    """This function returns a list of dicts that contains all the information about the courses.
    For the API requests, it's necessary to pass as params {enrollment_state = active},
    and it needs the authorization token.

    Returns:
        List: [courses( as dict )]
    """
    secrets = read_secrets('canvas/secrets.json')
    
    params = {"enrollment_state": "active"}
    headers = secrets['headers']
    url = secrets['url']
    r = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )
    
    return r.json()

def get_active_homework(id: int) -> List[Dict]:
    """This function returns a list of dicts that contains all the information about the active homework.

    Args:
        id (int): Is the id of the course. It is necessary to access to all the homework.

    Returns:
        List[Dict]: A list of homework of the course.
    """
    secrets = read_secrets('canvas/secrets.json')
    headers = secrets['headers']
    params = {'bucket': ['overdue']}
    url = f"https://canvas.instructure.com/api/v1/courses/{id}/assignments"
        
    r = requests.get(
        url=url,
        params=params,
        headers=headers
    )

    return r.json()

def get_homework()-> List[Dict]:
    """This function returns the formatted homework, ready to be linked to the Notion Database.

    Returns:
        List[Dict]: Every dict in the list will havehis course, due_at, html_url, id and name. It also will have and "is_done" attr, for compatibility
    with Notion.
    """
    
    courses = get_courses()
    
    if len(courses) == 0: return
    
    homework = []
    
    for c in courses:
        id = c['id']
        homework_list = get_active_homework(id)
        

        for h in homework_list:
            h_formatted = format_homework(h=h, course_name=c['name'])
            if h_formatted:
            
                homework.append(h_formatted) 
        
    return homework
                
def format_homework(h: Dict, course_name: str)-> Dict:
    """This function returns the formatted homework, as is requested by Notion API.

    Args:
        h (Dict): A dictionary which contains the homework information.
        course_name (str): The name of the course of the homework.

    Returns:
        Dict: a formatted dictionary with homework information.
    """
    if h is None: return
    
    #Url formatting
    url = h['html_url'].replace("canvas", 'iteso')
    
    #Datetime formatting for 
    date_str = h['due_at']
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    delta = timedelta(hours=5) #Because I am in GMT-5
    date_formatted = date - delta
    
    return {
                'course': course_name,
                'due_at': date_formatted.strftime("%Y-%m-%dT%H:%M:%S.000-05:00"),
                'html_url': url,
                'id': h['id'],
                'name': h['name'],
    }
                
                        
if __name__ == '__main__':
    homework = get_homework()
    
    for h in homework:
        print(json.dumps(h, indent=4))
        
        
    
