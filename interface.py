import streamlit as st
import yaml
import subprocess
import os

# Função para carregar o arquivo YAML
def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Função para salvar o arquivo YAML
def save_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(data, file, allow_unicode=True)

# Caminho do arquivo YAML
yaml_path = 'configs/apex.yaml'

# Carregar dados do arquivo YAML
data = load_yaml(yaml_path)

st.title('Configurações do Apex')

# Verificar e definir valores padrão para chaves faltantes
default_values = {
    'label_list': [],
    'enemy_list': [],
    'conf': 0.5,
    'smooth': 0.5,
    'resolution_x': 1920,
    'resolution_y': 1080,
    'detect_length': 640,
    'mouse_button_1': 'left',
    'mouse_button_2': 'right',
    'auto_lock_button': 'middle',
    'pos_factor': 0.5,
    'max_lock_dis': 500,
    'max_step_dis': 50,
    'max_pid_dis': 10,
    'pidx_kp': 0.1,
    'pidx_kd': 0.01,
    'pidx_ki': 0.005,
    'pidy_kp': 0.1,
    'pidy_kd': 0.01,
    'pidy_ki': 0.005,
    'save_screenshot': False,
    'visualization': False,
    'speed_test': False,
    'print_button': False,
    'delay': 0.01,
    'onnx_path': '',
    'trt_path': ''
}

for key, default in default_values.items():
    if key not in data:
        data[key] = default

# Extract base name for weights from the onnx_path or trt_path
weights_name_default = os.path.basename(data['onnx_path']).replace('.onnx', '')

# Adicionar campo para o nome do arquivo de pesos
weights_name = st.text_input('Weights Name', weights_name_default)
data['onnx_path'] = f'weights/{weights_name}.onnx'
data['trt_path'] = f'weights/{weights_name}.trt'

# Create tabs
tab1, tab2 = st.tabs(["Configurações do Mouse", "Configurações IA"])

with tab1:
    st.header("Configurações do Mouse")
    # Editar configurações do mouse
    data['mouse_button_1'] = st.text_input('Mouse Button 1', data['mouse_button_1'])
    data['mouse_button_2'] = st.text_input('Mouse Button 2', data['mouse_button_2'])
    data['auto_lock_button'] = st.text_input('Auto Lock Button', data['auto_lock_button'])

    # Editar configurações avançadas com sliders
    data['pidx_kp'] = st.slider('PID X KP', 0.0, 10.0, data['pidx_kp'])
    data['pidx_kd'] = st.slider('PID X KD', 0.0, 10.0, data['pidx_kd'])
    data['pidx_ki'] = st.slider('PID X KI', 0.0, 10.0, data['pidx_ki'])
    data['pidy_kp'] = st.slider('PID Y KP', 0.0, 10.0, data['pidy_kp'])
    data['pidy_kd'] = st.slider('PID Y KD', 0.0, 10.0, data['pidy_kd'])
    data['pidy_ki'] = st.slider('PID Y KI', 0.0, 10.0, data['pidy_ki'])

    # Sliders for Max Lock Distance, Max Step Distance, and Max PID Distance
    data['max_lock_dis'] = st.slider('Max Lock Distance', 0, 1000, data['max_lock_dis'])
    data['max_step_dis'] = st.slider('Max Step Distance', 0, 300, data['max_step_dis'])
    data['max_pid_dis'] = st.slider('Max PID Distance', 0, 100, data['max_pid_dis'])

with tab2:
    st.header("Configurações IA")
    # Editar listas
    label_list = st.text_input('Label List', ', '.join(data['label_list']))
    data['label_list'] = [item.strip() for item in label_list.split(',')]

    enemy_list = st.text_input('Enemy List', ', '.join(data['enemy_list']))
    data['enemy_list'] = [item.strip() for item in enemy_list.split(',')]

    # Editar configurações gerais
    data['conf'] = st.slider('Conf', 0.0, 1.0, data['conf'])
    data['smooth'] = st.slider('Smooth', 0.0, 1.0, data['smooth'])
    data['resolution_x'] = st.number_input('Resolution X', value=data['resolution_x'])
    data['resolution_y'] = st.number_input('Resolution Y', value=data['resolution_y'])
    data['detect_length'] = st.number_input('Detect Length', value=data['detect_length'])

    # Editar outras funções
    data['pos_factor'] = st.slider('Pos Factor', 0.0, 1.0, data['pos_factor'])
    data['save_screenshot'] = st.checkbox('Save Screenshot', value=data['save_screenshot'])
    data['visualization'] = st.checkbox('Visualization', value=data['visualization'])
    data['speed_test'] = st.checkbox('Speed Test', value=data['speed_test'])
    data['print_button'] = st.checkbox('Print Button', value=data['print_button'])
    data['delay'] = st.number_input('Delay', value=data['delay'])

# Botão para salvar configurações
if st.button('Salvar Configurações'):
    save_yaml(data, yaml_path)
    st.success('Configurações salvas com sucesso!')

# Função para iniciar o script apex.py
def start_apex():
    # Carregar novamente a configuração para garantir que estamos usando a última versão salva
    data = load_yaml(yaml_path)
    return subprocess.Popen(['python', 'apex.py'])

# Botão para iniciar o script apex.py
if st.button('Iniciar Apex'):
    apex_process = start_apex()
    st.session_state.apex_process = apex_process
    st.success('Apex iniciado com sucesso!')

