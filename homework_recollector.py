import json
from json import dumps
from canvas.manager import get_homework
from notion.manager import search_homework, post_homework

printf = lambda h: print(dumps(h, indent=4))

if __name__ == '__main__':
    homework = get_homework()
    
    for h in homework:
        on_notion = search_homework(h['id'])
        if not on_notion:
            response = post_homework(h)
            printf(response)