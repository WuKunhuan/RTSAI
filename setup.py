
import os, setuptools
from RTSAI.config import PACKAGE_NAME, PACKAGE_VERSION, DATA_PATH, ASSETS_PATH

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
    ], 
    package_data={
        PACKAGE_NAME: [os.path.join(DATA_PATH, '*'), os.path.join(ASSETS_PATH, '*')]
    }, 

)
