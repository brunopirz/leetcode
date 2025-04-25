class PrivacyManager:
    """
    Gerencia a ocultação e restauração de janelas sensíveis para privacidade durante compartilhamento de tela.

    Atributos:
        ui_manager: Referência ao gerenciador de interface do usuário.
    """
    def __init__(self, ui_manager):
        """
        Inicializa o gerenciador de privacidade com o gerenciador de interface do usuário.

        Parâmetros:
            ui_manager: O gerenciador de interface do usuário associado.
        """
        self.ui_manager = ui_manager

    def hide_sensitive_windows(self):
        """
        Oculta janelas sensíveis, como overlay de resposta e pré-visualização, se existirem.
        """
        # Oculta overlay de resposta e pré-visualização, se existirem
        if self.ui_manager.response_overlay:
            self.ui_manager.response_overlay.withdraw()
        if self.ui_manager.preview_window:
            self.ui_manager.preview_window.withdraw()

    def show_sensitive_windows(self):
        """
        Restaura janelas sensíveis, como overlay de resposta e pré-visualização, se existirem.
        """
        # Restaura overlay de resposta e pré-visualização, se existirem
        if self.ui_manager.response_overlay:
            self.ui_manager.response_overlay.deiconify()
        if self.ui_manager.preview_window:
            self.ui_manager.preview_window.deiconify()

    def test_privacy_mode(self):
        """
        Alterna rapidamente o modo oculto para teste visual.
        """
        # Alterna rapidamente o modo oculto para teste visual
        if not self.ui_manager.hidden_mode:
            self.ui_manager.hidden_mode = True
            self.hide_sensitive_windows()
            self.ui_manager.toggle_privacy_btn.config(text="Desativar Modo Oculto")
            self.ui_manager.root.title("LeetCode Helper (Modo Oculto)")
            self.ui_manager.status_label.config(foreground="red")
        else:
            self.ui_manager.hidden_mode = False
            self.show_sensitive_windows()
            self.ui_manager.toggle_privacy_btn.config(text="Ativar Modo Oculto")
            self.ui_manager.root.title("LeetCode Helper")
            self.ui_manager.status_label.config(foreground="black")