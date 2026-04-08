from setuptools import setup
import os
from glob import glob

package_name = 'twin_firmware'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/twin_firmware']),
    ('share/twin_firmware', ['package.xml']),
    ('share/twin_firmware/launch', ['launch/firmware.launch.py']),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='anand',
    maintainer_email='anand@todo.todo',
    description='Twin firmware package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
