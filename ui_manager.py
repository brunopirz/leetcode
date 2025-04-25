"""
Gerencia a interface gráfica principal do aplicativo LeetCode Helper.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from screen_capture import ScreenCapture
from api_manager import APIManager
from privacy_manager import PrivacyManager

class UIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LeetCode Helper")
        self.api_manager = APIManager()
        self.screen_capture = ScreenCapture(self)
        self.privacy_manager = PrivacyManager(self)
        self.response_overlay = None
        self.preview_window = None
        self.hidden_mode = False
        self._build_ui()

    def _build_ui(self):
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Entrada manual
        label = ttk.Label(main_frame, text="Cole o enunciado ou código da questão:")
        label.pack(anchor=tk.W)
        self.text_input = tk.Text(main_frame, height=10)
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=5)

        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        self.capture_btn = ttk.Button(btn_frame, text="Capturar Área da Tela", command=self.screen_capture.start_capture)
        self.capture_btn.pack(side=tk.LEFT, padx=2)
        self.send_btn = ttk.Button(btn_frame, text="Enviar para LLM", command=self._send_to_llm)
        self.send_btn.pack(side=tk.LEFT, padx=2)
        self.toggle_privacy_btn = ttk.Button(btn_frame, text="Ativar Modo Oculto", command=self.toggle_privacy_mode)
        self.toggle_privacy_btn.pack(side=tk.LEFT, padx=2)
        self.test_privacy_btn = ttk.Button(btn_frame, text="Testar Modo Oculto", command=self.test_privacy_visual)
        self.test_privacy_btn.pack(side=tk.LEFT, padx=2)

        # Status bar
        self.status_var = tk.StringVar(value="Pronto.")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def _send_to_llm(self):
        texto = self.text_input.get("1.0", tk.END).strip()
        if not texto:
            self.set_status("Por favor, insira ou capture o texto da questão.")
            return
        self.set_status("Enviando para API...")
        self.root.after(100, lambda: self._async_send(texto))

    def _async_send(self, texto):
        try:
            resposta = self.api_manager.send_question(texto)
            self.show_response_overlay(resposta)
            self.set_status("Resposta recebida.")
        except Exception as e:
            self.set_status(f"Erro: {e}")
            messagebox.showerror("Erro ao enviar para LLM", str(e))

    def show_response_overlay(self, resposta):
        if self.response_overlay:
            self.response_overlay.destroy()
        self.response_overlay = tk.Toplevel(self.root)
        self.response_overlay.title("Resposta da LLM")
        self.response_overlay.geometry("500x300+100+100")
        self.response_overlay.protocol("WM_DELETE_WINDOW", self.response_overlay.withdraw)
        text = tk.Text(self.response_overlay, wrap=tk.WORD, state=tk.NORMAL)
        text.insert(tk.END, resposta)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.response_overlay, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        copy_btn = ttk.Button(self.response_overlay, text="Copiar Resposta", command=lambda: self._copy_to_clipboard(resposta))
        copy_btn.pack(pady=5)
        if self.hidden_mode:
            self.response_overlay.withdraw()

    def _copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.set_status("Resposta copiada para a área de transferência.")

    def set_status(self, msg):
        self.status_var.set(msg)

    def toggle_privacy_mode(self):
        if not self.hidden_mode:
            self.hidden_mode = True
            self.privacy_manager.hide_sensitive_windows()
            self.toggle_privacy_btn.config(text="Desativar Modo Oculto")
            self.root.title("LeetCode Helper (Modo Oculto)")
            self.status_label.config(foreground="red")
            self.set_status("Modo oculto ativado.")
        else:
            self.hidden_mode = False
            self.privacy_manager.show_sensitive_windows()
            self.toggle_privacy_btn.config(text="Ativar Modo Oculto")
            self.root.title("LeetCode Helper")
            self.status_label.config(foreground="black")
            self.set_status("Modo oculto desativado.")

    def test_privacy_visual(self):
        # Simula rapidamente o efeito visual do modo oculto sem alterar o estado real
        if not self.hidden_mode:
            self.privacy_manager.hide_sensitive_windows()
            self.toggle_privacy_btn.config(text="Desativar Modo Oculto")
            self.root.title("LeetCode Helper (Modo Oculto)")
            self.status_label.config(foreground="red")
            self.set_status("[Teste] Modo oculto ativado.")
            self.root.after(1000, lambda: self._restore_privacy_visual())
        else:
            self.privacy_manager.show_sensitive_windows()
            self.toggle_privacy_btn.config(text="Ativar Modo Oculto")
            self.root.title("LeetCode Helper")
            self.status_label.config(foreground="black")
            self.set_status("[Teste] Modo oculto desativado.")
            self.root.after(1000, lambda: self._restore_privacy_visual())

    def _restore_privacy_visual(self):
        # Restaura o visual original após o teste
        if not self.hidden_mode:
            self.privacy_manager.show_sensitive_windows()
            self.toggle_privacy_btn.config(text="Ativar Modo Oculto")
            self.root.title("LeetCode Helper")
            self.status_label.config(foreground="black")
            self.set_status("Pronto.")
        else:
            self.privacy_manager.hide_sensitive_windows()
            self.toggle_privacy_btn.config(text="Desativar Modo Oculto")
            self.root.title("LeetCode Helper (Modo Oculto)")
            self.status_label.config(foreground="red")
            self.set_status("Modo oculto ativado.")

    def run(self):
        self.root.mainloop()