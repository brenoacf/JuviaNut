import argparse
import time
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Application:
    def __init__(self):
        self.data_structure = {}
        self.xml_path = None
        super().__init__()

    def main(self):
        self.ready_entry()
        self.xml_parse()
        #d1
#d2
    def xml_parse(self):
        # Parse o arquivo XML
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        # Itera sobre os elementos globais
        globals_element = root.find('globals')
        if globals_element is not None:
            for variable_element in globals_element.findall('variable') + globals_element.findall('constant'):
                variable_name = variable_element.get('name')
                variable_type = variable_element.get('type')
                variable_value = variable_element.text
                self.data_structure[variable_name] = {'type': variable_type, 'value': variable_value}  

        # Itera sobre os elementos de script
        for script_element in root.findall('script'):
            script_name = script_element.get('name')
            script_url = script_element.get('url')
            steps = []
            for step_element in script_element.findall('steps/step'):
                step_type_action = step_element.get('typeAction')
                step_type_tag = step_element.get('typeTag')
                step_value = step_element.get('value')
                step_wait = step_element.get('wait')
                step_input = step_element.get('input')
                steps.append({'typeAction': step_type_action, 'typeTag': step_type_tag, 'value': step_value, 'wait': step_wait, 'input': step_input})
            self.data_structure[script_name] = {
                'url': script_url,
                'steps': steps
            }

    def run_script(self, script_name, driver):
        for action in self.data_structure[script_name]['steps']:
            print(action)
            if action['typeAction'] == 'input':
                if action['wait']:
                    time.sleep(int(action['wait'].rstrip('s'))) 
                if action['typeTag'] == 'xpath':    
                    driver.find_element(By.XPATH, action['value']).send_keys(action['input']) 
                elif action['typeTag'] == 'id':
                    driver.find_element(By.ID, action['value']).send_keys(action['input']) 

            elif action['typeAction'] == 'click':
                if action['wait']:
                    time.sleep(int(action['wait'].rstrip('s')))
                if action['typeTag'] == 'xpath':    
                    driver.find_element(By.XPATH, action['value']).click()
                elif action['typeTag'] == 'id':
                    delay = 3 
                    try:
                        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, action['value'])))
                        driver.find_element(By.ID, action['value']).click()  
                    except TimeoutException:
                        print("Loading took too much time!")

    def ready_entry(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--xml', type=str, nargs='+')
        args = parser.parse_args()

        if len(args.xml) == 0:
            print("Nenhuma arquivo encontrado!\n")
            quit()
        else:
            self.xml_path = args.xml[0]

if __name__ == "__main__":
    app = Application()
    app.main()
