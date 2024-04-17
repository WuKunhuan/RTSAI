
import os, glob, setuptools
from RTSAI.config import PACKAGE_NAME, PACKAGE_VERSION, DATA_PATH, ASSETS_PATH

def recursive(directory):
    file_patterns = os.path.join(directory, '**', '*')
    return [file for file in glob.glob(file_patterns, recursive=True)]

setuptools.setup (
    name = PACKAGE_NAME, 
    version = PACKAGE_VERSION, 
    description = 'The recreated RTSAI package with pip install. ', 
    long_description = 'The recreated RTSAI package with pip install. ', 
    long_description_content_type = 'text/x-rst', 
    author = 'wukunhuan', 
    author_email = 'u3577163@connect.hku.hk', 
    url = 'https://github.com/WuKunhuan/RTSAI', 
    entry_points = {
        'console_scripts': [
            'RTSAI = RTSAI.main:main'
        ]
    }, 
    project_urls = {
        "Source": "https://github.com/WuKunhuan/RTSAI", 
    }, 
    python_requires=">=3.10.0", 
    install_requires = [
        "pyautogui", 
        "validators", 
    ], 
    package_data={
        PACKAGE_NAME: recursive(DATA_PATH) + recursive(ASSETS_PATH)
    }, 

)
