import re

def clean_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)