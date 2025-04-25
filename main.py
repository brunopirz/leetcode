"""
Aplicativo desktop para auxiliar na resolução de questões do LeetCode com captura de tela, integração com LLM e modo de privacidade.
"""

from ui_manager import UIManager

def main():
    app = UIManager()
    app.run()

if __name__ == "__main__":
    main()