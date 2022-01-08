import json
from json import dumps
from canvas.manager import get_homework
from notion.manager import search_homework, post_homework

printf = lambda h: print(dumps(h, indent=4))

if __name__ == '__main__':
    homework = get_homework()
    
    for h in homework:
        on_notion = search_homework(h['name'])
        if not on_notion:
            post_homework(h)