# project: p3
# submitter: kkhill4
# partner: none
# hours: 12

from collections import deque
import os
import pandas as pd

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ Record the node value in self.order, and return its children
        param: node
        return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        self.visited.clear()
        self.order = []
        self.dfs_visit(node)

    def dfs_visit(self, node):
        if node in self.visited:
            return
        self.visited.add(node)
        children = self.visit_and_get_children(node)
        for child in children:
            self.dfs_visit(child)

    def bfs_search(self, node):
        added = {node}
        todo = deque([node])
        while len(todo) > 0:
            current = todo.popleft()
            children = self.visit_and_get_children(current)
            for child in children:
                if child not in added:
                    todo.append(child)
                    added.add(child)  
                    

class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def visit_and_get_children(self, node):
        self.order.append(node)
        children = []
        row = self.df.loc[node]
        for child, has_edge in row.items():
            if has_edge == 1:
                children.append(child)
        return children

    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        self.directory = 'file_nodes'

    def visit_and_get_children(self, node):
        file_path = os.path.join(self.directory, node)
        children = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.order.append(lines[0].strip())
            children = [child.strip() for child in lines[1].split(',')]
        return children

    def concat_order(self):
        return ''.join(self.order)
    


class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tablelist = []
        
    def visit_and_get_children(self, url):
        self.driver.get(url)
        self.order.append(url)
        pagesource = self.driver.page_source
        children = self.driver.find_elements(by = 'tag name', value = 'a')
        smalltable = pd.read_html(pagesource)[0]
        self.tablelist.append(smalltable)
        result = []
        for link in children:
            attribute = link.get_attribute('href')
            result.append(attribute)
        return result
    
    def table(self):
        return pd.concat(self.tablelist, ignore_index = True)
                    


from selenium.webdriver.common.by import By
import time
import requests

def reveal_secrets(driver,url,travellog):
    password = ''
    for clue in travellog.clue:
        password += str(clue)
        
    driver.get(url)
    
    password_input = driver.find_element(by = "id", value = "password-textbox")
    password_input.send_keys(password)
    button = driver.find_element(by = "id", value = "submit-button")
    button.click()
    time.sleep(1)
    
    view_location_button = driver.find_element(by = "id", value = "view-location-button")
    view_location_button.click()
    time.sleep(2)
            
    image_url = driver.find_element(by = "id", value="image").get_attribute("src") 
    response = requests.get(image_url)
    response.raise_for_status()
    with open("Current_Location.jpg", "wb") as file:
        file.write(response.content)
    current_location = driver.find_element(by = "id", value = "location").text
    return current_location
