"""
Módulo para captura de tela seletiva usando mss e Tkinter para seleção dinâmica.
"""
import tkinter as tk
from tkinter import Toplevel
import mss
from PIL import Image, ImageTk
import io

class ScreenCapture:
    """
    Módulo para captura de tela seletiva usando mss e Tkinter para seleção dinâmica.

    Atributos:
        ui_manager: Referência ao gerenciador de interface do usuário.
        capture_window: Janela de captura de tela.
        start_x, start_y, end_x, end_y: Coordenadas para seleção de área.
        rect: Retângulo de seleção.
        preview_img: Imagem de pré-visualização.
    """
    def __init__(self, ui_manager):
        """
        Inicializa o módulo de captura de tela com o gerenciador de interface do usuário.

        Parâmetros:
            ui_manager: O gerenciador de interface do usuário associado.
        """
        self.ui_manager = ui_manager
        self.capture_window = None
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.rect = None
        self.preview_img = None

    def start_capture(self):
        """
        Inicia o processo de captura de tela, criando uma janela de seleção.
        """
        self.capture_window = tk.Toplevel(self.ui_manager.root)
        self.capture_window.attributes('-fullscreen', True)
        self.capture_window.attributes('-alpha', 0.3)
        self.capture_window.config(bg='black')
        self.capture_window.bind('<ButtonPress-1>', self.on_mouse_down)
        self.capture_window.bind('<B1-Motion>', self.on_mouse_drag)
        self.capture_window.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.capture_window.focus_set()

    def on_mouse_down(self, event):
        """
        Registra a posição inicial do clique do mouse para a seleção.

        Parâmetros:
            event: Evento de clique do mouse.
        """
        self.start_x = self.capture_window.winfo_pointerx()
        self.start_y = self.capture_window.winfo_pointery()
        if self.rect:
            self.capture_window.delete(self.rect)
        self.rect = None

    def on_mouse_drag(self, event):
        """
        Atualiza o retângulo de seleção conforme o mouse é arrastado.

        Parâmetros:
            event: Evento de arrasto do mouse.
        """
        x, y = self.capture_window.winfo_pointerx(), self.capture_window.winfo_pointery()
        if self.rect:
            self.capture_window.delete(self.rect)
        canvas = self.get_canvas()
        self.rect = canvas.create_rectangle(self.start_x, self.start_y, x, y, outline='red', width=2)

    def on_mouse_up(self, event):
        """
        Finaliza a seleção e captura a área selecionada.

        Parâmetros:
            event: Evento de liberação do mouse.
        """
        self.end_x = self.capture_window.winfo_pointerx()
        self.end_y = self.capture_window.winfo_pointery()
        self.capture_window.destroy()
        self.capture_window = None
        self._capture_area()

    def _capture_area(self):
        """
        Captura a área selecionada da tela e exibe a pré-visualização.
        """
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
            img = sct.grab(monitor)
            img_pil = Image.frombytes('RGB', img.size, img.rgb)
            self.preview_img = img_pil
            self.show_preview(img_pil)

    def show_preview(self, img_pil):
        """
        Exibe a pré-visualização da captura de tela em uma nova janela.

        Parâmetros:
            img_pil: Imagem capturada a ser exibida.
        """
        if self.ui_manager.preview_window:
            self.ui_manager.preview_window.destroy()
        preview = Toplevel(self.ui_manager.root)
        preview.title("Pré-visualização da Captura")
        preview.geometry("300x200+150+150")
        img_pil = img_pil.resize((280, 180))
        img_tk = ImageTk.PhotoImage(img_pil)
        label = tk.Label(preview, image=img_tk)
        label.image = img_tk
        label.pack(padx=10, pady=10)
        close_btn = tk.Button(preview, text="Fechar Pré-visualização", command=preview.withdraw)
        close_btn.pack(pady=5)
        self.ui_manager.preview_window = preview
        if self.ui_manager.hidden_mode:
            self.ui_manager.preview_window.withdraw()

    def get_canvas(self):
        """
        Cria um canvas transparente sobre a janela de captura.

        Retorna:
            Canvas: O canvas criado para desenhar a seleção.
        """
        if not hasattr(self, '_canvas'):
            self._canvas = tk.Canvas(self.capture_window, bg='', highlightthickness=0)
            self._canvas.pack(fill=tk.BOTH, expand=True)
        return self._canvas