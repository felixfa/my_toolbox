import requests
import re
from bs4 import BeautifulSoup

def scrap_n_top_packages_per_day(n):
    response = requests.get("https://pypistats.org/top")
    soup = BeautifulSoup(response.content,'html.parser')

    all_a = []
    for el in soup.find_all('a'):
        all_a.append(el.text)

    start = 4
    end = start + n
    top_n_packages_per_day = all_a[start:end]

    return top_n_packages_per_day

list_packages = scrap_n_top_packages_per_day(n=10)
print(list_packages)
print('')

def scrap_requirements_for_package_list(list_packages):
    github_adresses = []
    for package_name in list_packages:
        response = requests.get("https://pypi.org/project/" + str(package_name))
        soup = BeautifulSoup(response.content,'html.parser')
        for el in soup.find_all('a',href=True):
            if 'github' in el['href'] and el['href'].endswith(str(package_name)):
                github_adresses.append(el['href'])
                break
    return github_adresses


ga = scrap_requirements_for_package_list(list_packages)
print(ga)
print('')

def finding_requirement_address_for_packages(list_packages, github_adresses):
    requirements = {}
    for index,adresses in enumerate(github_adresses):
        response = requests.get(str(adresses))
        soup = BeautifulSoup(response.content,'html.parser')
        for el in soup.find_all('a',href=True):
            if 'requirements' in el['href']:
                requirements[list_packages[index]] = (el['href'])
                break
    return requirements


requirement_address_dict = finding_requirement_address_for_packages(list_packages, ga)
print(requirement_address_dict)
print('')

def get_requirements_for_package(requirement_address_dict):
    requirements = {}
    for package_name, adresses in requirement_address_dict.items():
        response = requests.get('https://github.com/' + str(adresses))
        soup = BeautifulSoup(response.content,'html.parser')
        requirements_package=[]
        for el in soup.find_all('tr'):
            requirements_package.append(el.text.split("=")[0].strip().rstrip('>'))
        requirements[package_name] = requirements_package

    return requirements

requirements_dict = get_requirements_for_package(requirement_address_dict)

def plot_requirements_Graph_for_package(requirements_dict):
    for package_name, requirement_list in requirements_dict.items():
        print(f'{package_name}')
        for el in requirement_list:
            print(f'├── {el}' )
        print('')
    return None

plot_requirements_Graph_for_package(requirements_dict)
