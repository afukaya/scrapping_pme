from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

import time
import json

# Carrega a página e aguarda a autenticação do Captcha
nire_list = []
driver = webdriver.Firefox(executable_path = r'.\webdriver\geckodriver.exe')

print('Carregando a página de busca...')
driver.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=')
txtMunicipio = driver.find_element_by_id('ctl00_cphContent_frmBuscaAvancada_txtMunicipio')
txtMunicipio.send_keys('santos')
btPesquisar = driver.find_element_by_id('ctl00_cphContent_frmBuscaAvancada_btPesquisar')
btPesquisar.click()

print("Realize a autenticação do CAPTCHA.")
input('Pressione <enter> para contiuar.')

# Percorre todas as páginas com os resultados da pesquisa e extrai a tabela 
# com os dados e armazena os NIREs em uma lista.
print('Carregando a lista de NIREs')

while True:
    try:
        result       = int(driver.find_element(By.ID,'ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.split()[-1])
        result_count = int(driver.find_element(By.ID,'ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))
        print("Recuperando NIREs {} - {} de {}".format(result,result+15,result_count))

        data_table = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
        raw_data = data_table.find_elements_by_tag_name('td')
        for nire in raw_data:
            if nire.get_attribute("class") == 'item01':
                nire_list.append(nire.text.strip())

        btNext = driver.find_element(By.ID,'ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText')
        if (result < result_count):
            btNext.click()
            loading = WebDriverWait(driver,5).until(EC.invisibility_of_element((By.ID,'ctl00_cphContent_gdvResultadoBusca_qtpLoading_pnlMessage')))
            time.sleep(5) # Verificar se o grid esta a carregar.
        else:
            break
    except:
        pass
    

url_base = 'https://www.jucesponline.sp.gov.br/Pre_Visualiza.aspx?nire='
empresas = []
for nire in nire_list:
    driver.get(url_base + nire)
    
    timestamp         = driver.find_element(By.ID,"ctl00_cphContent_frmPreVisualiza_lblEmissao").text
    nome              = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblEmpresa").text
    tipo              = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblDetalhes").text
    data_constituicao = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblConstituicao").text
    inicio_atividade  = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblAtividade").text
    cnpj              = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblCnpj").text
    ie                = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblInscricao").text
    objeto            = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblObjeto").text
    capital           = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblCapital").text
    logradouro        = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblLogradouro").text
    numero            = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblNumero").text
    bairro            = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblBairro").text
    complemento       = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblComplemento").text
    municipio         = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblMunicipio").text
    cep               = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblCep").text
    uf                = driver.find_element(By.ID, "ctl00_cphContent_frmPreVisualiza_lblUf").text

    empresas.append({'timestamp':timestamp, 'nire':nire, 'nome':nome,'tipo':tipo,'data_constituicao':data_constituicao, 'inicio_atividade':inicio_atividade, 'cnpj':cnpj, 'ie':ie, 'objeto':objeto, 'capital':capital,'logradouro':logradouro, 'numero':numero, 'bairro':bairro, 'complemento':complemento, 'municipio':municipio, 'cep':cep, 'uf':uf})
    time.sleep(10)

f = open('data_file.json','w')
f.write(json.dumps(empresas))    