from setuptools import setup, find_packages

setup(
    name='puttochain',
    version='0.1.0',
    description='A digital ethics system integrating Dhamma, Blockchain, and AI.',
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),
    install_requires=[
        # ใส่ Dependencies หลักที่มาจาก requirements.txt
        'fastapi',
        'uvicorn[standard]',
        'pydantic',
        'web3',
        'python-dotenv',
        # 'firebase-admin', # ถ้าติดตั้งจริง
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
    ],
)
