import winreg
from OpenSSL import crypto
from selenium import webdriver

def UpdateStringValue(strigValueName,newValueOfStrinValue, stringValuePath):
  key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, stringValuePath, 0, winreg.KEY_ALL_ACCESS)
  winreg.SetValueEx(key, strigValueName, 0, winreg.REG_SZ, newValueOfStrinValue)
  winreg.CloseKey(key)


def GetCertificate(pathOfCertificate, passwordOfCertifcate):
    pkcs12 = crypto.load_pkcs12(open(pathOfCertificate, 'rb').read(), passwordOfCertifcate)   
    return pkcs12.get_certificate()


if __name__ == "__main__":
    pathOfstringValue = 'SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'
    stringValueName = '1'

    certificate = GetCertificate("C:\Certificados\\45985371000108_000001010131997.pfx", 'br018726')
    subject = certificate.get_subject()
    issuer = certificate.get_issuer()
    url_where_certificate_will_be_send = "https://notacarioca.rio.gov.br/"
    url = 'https://notacarioca.rio.gov.br/senhaweb/login.aspx'
    json = '{"pattern":"' + url_where_certificate_will_be_send + '","filter":{"ISSUER":{"CN":"' + issuer.CN + '","C":"' + issuer.C + '","O":"' + issuer.O + '"},"SUBJECT":{"CN":"' + subject.CN + '","C":"' + subject.C + '","O":"' + subject.O + '"}}}'
    UpdateStringValue(stringValueName, json, pathOfstringValue)
    path = 'C:\\Users\\rodrigo.peres\Downloads\chromedriver_win32\\'
    driver = webdriver.Chrome()

    driver.get(url)

    btn_certificate_login = driver.find_element_by_id('ctl00_cphCabMenu_imgLoginICP')
    btn_certificate_login.click()
    driver.quit()




