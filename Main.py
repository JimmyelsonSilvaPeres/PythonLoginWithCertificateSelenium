import winreg
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID
from selenium import webdriver

def UpdateStringValue(strigValueName,newValueOfStrinValue, stringValuePath):
  key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, stringValuePath, 0, winreg.KEY_ALL_ACCESS)
  winreg.SetValueEx(key, strigValueName, 0, winreg.REG_SZ, newValueOfStrinValue)
  winreg.CloseKey(key)


def GetCertificate(pathOfCertificate, passwordOfCertifcate):
    with open(pathOfCertificate,'rb') as f:
      private_key,certificado,additional_certificates = pkcs12.load_key_and_certificates(f.read(), bytes(passwordOfCertifcate,encoding='utf-8'))
    
    return certificado

if __name__ == "__main__":
    pathOfstringValue = 'SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'
    stringValueName = '1'

    certificate = GetCertificate("C:\Certificados\\45985371000108_000001010131997.pfx", 'br018726')
    subject = certificate.subject
    issuer = certificate.issuer
    url_where_certificate_will_be_send = "https://notacarioca.rio.gov.br/"
    url = 'https://notacarioca.rio.gov.br/senhaweb/login.aspx'
    
    json = \
    '{"pattern":"' + url_where_certificate_will_be_send + '", \
    "filter":{"ISSUER":{"CN":"' + issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value + '", \
    "C":"' + issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value + '",\
    "O":"' + issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value  + '"},\
    "SUBJECT":{"CN":"' + subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value + '",\
    "C":"' + subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value + '",\
    "O":"' + subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value + '"}}}'
    
    UpdateStringValue(stringValueName, json, pathOfstringValue)
    
    path = 'C:\\Users\\rodrigo.peres\Downloads\chromedriver_win32\\'
    driver = webdriver.Chrome()

    driver.get(url)

    btn_certificate_login = driver.find_element_by_id('ctl00_cphCabMenu_imgLoginICP')
    btn_certificate_login.click()
    driver.quit()




