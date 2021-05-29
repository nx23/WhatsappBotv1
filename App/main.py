#!/usr/bin/env python3
import pathlib
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

class Whatsappbot():
    def __init__(self):
        self.__path = str(pathlib.Path(__file__).parent.absolute())
        self.__geckopath = self.__path + r'\geckodriver\geckodriver.exe'
        self.__logado = False
        self._retrycount = 10
        self.webdriver = webdriver.Firefox(executable_path=self.__geckopath)
        self.webdriver.get('https://web.whatsapp.com/')
        sleep(3)
        self.verifica_login()

    def logar(self):
        self.__logado = True

    def verifica_login(self):
        while not self.__logado:
            if self._retrycount > 0:
                try:
                    qr_code = self.webdriver.find_element_by_class_name('-A_bA')
                    print('Você está deslogado, por favor realize o login.')
                    self._retrycount -= 1
                    sleep(10)
                except NoSuchElementException:
                    print('Login realizado com sucesso.')
                    sleep(3)
                    self.logar()

    def checar_novas_mensagens(self):
        try:
            novas_msgs = self.webdriver.find_elements_by_css_selector('._2Z4DV._1V5O7')
            if novas_msgs:
                return novas_msgs
        except Exception:
            traceback.print_exc()
            return []

    def responder(self, nova_msg):
        nova_msg.click()
        sleep(1)
        contato = self.webdriver.find_element_by_class_name('_2KQyF').text
        mensagens_recebidas = self.webdriver.find_elements_by_class_name('_1bR5a')
        ultima_msg = mensagens_recebidas[-1].text
        print(f'{contato} diz:\n{ultima_msg}')
        #msg = f'Olá {contato}, no momento não estou podendo responder, estou de férias.'
        msg = input("Digite a mensagem ou 'pass' para não responder:\n")
        if msg.lower() == 'pass':
            pass
        else:
            msg_box = self.webdriver.find_elements_by_class_name('_2_1wd.copyable-text.selectable-text')
            msg_box[-1].send_keys(msg)
            sleep(1)
            btn_enviar = self.webdriver.find_element_by_class_name('_1E0Oz')
            btn_enviar.click()

def main():
    bot = Whatsappbot()
    while True:
        novas_msgs = bot.checar_novas_mensagens()
        if novas_msgs:
            print(f'Existem {len(novas_msgs)} conversas não respondidas.')
            comando = input('Deseja responder ? S/N\n')
            if comando.upper() == 'S':
                for nova_msg in novas_msgs:
                    bot.responder(nova_msg)

if __name__ == '__main__':
    main()