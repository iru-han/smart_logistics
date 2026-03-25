from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'smart_logistics'

setup(
    name=package_name,
    version='0.0.0',
    packages=[
        package_name,
        f'{package_name}.core',
        f'{package_name}.database',
        f'{package_name}.navigation',
        f'{package_name}.vision',
        f'{package_name}.ui',
        package_name + '.ui.components',
    ],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 2. UI 파일을 설치 폴더에 포함시켜야 코드가 찾을 수 있음
        ('share/' + package_name + '/ui', glob(f'{package_name}/ui/*.ui')),
    ],
    package_data={
        package_name: ['ui/*.ui'],
    },
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='study.iru@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'main_node = smart_logistics.main:main',
        ],
    },
)
