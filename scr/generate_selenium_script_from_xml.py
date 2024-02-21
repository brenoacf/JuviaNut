import argparse
import xml.etree.ElementTree as ET

def generate_python_script_from_xml(xml_file_path):

    template_file_path = "template.py"
    output_file_path = 'generated_script.py'

    # Ler o arquivo de template
    with open(template_file_path, 'r') as file:
        template_content = file.read()

    # Gerar o código dinâmico como antes
    method_calls = []
    method_implementations = ''
    dynamic_code_1 = ''  # Código para #d1 - chamada métodos dinâmicos
    dynamic_code_2 = ''  # Código para #d2 - implementação métodos dinâmicos
        
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Gerar métodos para cada script
    for script in root.findall('script'):
        script_name = script.get('name')
        method_name = script_name.lower()
        method_implementations += f'''
    def {script_name.lower()}(self):
        script_name = '{script_name}'
        print("Executando o script: {script_name}\\n")

        # Acessa a URL especificada no script
        driver = webdriver.Firefox()
        driver.get(self.data_structure[script_name]['url'])
        driver.implicitly_wait(10)

        # Executa as acoes definidas em steps
        self.run_script(script_name,driver)

'''
    method_calls.append(f"self.{method_name}()")

    # Incluir chamadas de método no método main
    dynamic_code_1 = '\n'.join(method_calls)  

    # Incluir implementações dos métodos
    dynamic_code_2 = method_implementations     

    # Substituir espaços reservados no template pelo código dinâmico
    final_script = template_content.replace('#d1', dynamic_code_1).replace('#d2', dynamic_code_2)

    # Salvar o script final em um novo arquivo
    with open(output_file_path, 'w') as output_file:
        output_file.write(final_script)    

    print(f"Script Python gerado com sucesso: {output_file_path}")
    print(f"Execute o script da seguinte forma: python {output_file_path} --xml {xml_file_path}")

if __name__ == '__main__':
    xml_path = None
    parser = argparse.ArgumentParser(description="Gera um script Python a partir de um arquivo XML de entrada")
    parser.add_argument('--xml', type=str, nargs='+', help="O caminho para o arquivo XML de entrada")
    args = parser.parse_args()

    if len(args.xml) == 0:
        print("Nenhuma arquivo encontrado!\n")
        quit()
    else:
        xml_path = args.xml[0]

        # Chamada da função com o caminho do arquivo passado como argumento
        generate_python_script_from_xml(xml_path)
