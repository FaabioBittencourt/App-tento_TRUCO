"""from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from colors import *

COR_FUNDO     = [0.08, 0.05, 0.02, 1]
COR_DOURADO   = [0.85, 0.65, 0.1,  1]
COR_VERDE     = [0.18, 0.12, 0.04, 1]
COR_AZUL      = [0.1,  0.25, 0.55, 1]
COR_TEXTO_SEC = [0.6,  0.5,  0.3,  1]
COR_HEADER    = [0.12, 0.07, 0.02, 1]

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"
        self._build_ui()

    def _build_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=COR_FUNDO,
            padding=[dp(24), dp(32)], 
            spacing=dp(16)
            )
        root.add_widget(MDLabel(
            text="🃏",
            font_size="64sp",
            halign="center",
            size_hint_y=None,
            height=dp(80)
            ))
        root.add_widget(MDLabel(
            text="TRUCO DOS PIÁ",
            font_size="28sp",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
            size_hint_y=None,
            height=dp(48),
            bold=True
            ))
        root.add_widget(MDLabel(
            size_hint_y=None,
            height=dp(24)
            ))

        for texto, cor, tela in [
            ("Nova Partida", COR_VERDE,   "setup"),
            ("Jogadores",    COR_DOURADO,  "players"),
            ("Histórico",    COR_AZUL,    "history"),
        ]:
            btn = MDButton(
                style="filled",
                size_hint=(1, None),
                height=dp(56)
                )
            btn.md_bg_color = cor

            btn.add_widget(MDLabel(
                text=texto,
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
                halign="center",
                font_size="16sp"
                ))
            btn.bind(on_release=lambda x, t=tela: setattr(self.manager, "current", t))
            root.add_widget(btn)

        root.add_widget(MDLabel(
            size_hint_y=None,
            height=dp(24)))

        root.add_widget(MDLabel(
            text="Vai jogar viado!?",
            theme_text_color="Custom",
            text_color=COR_TEXTO_SEC,
            halign="center",
            font_size="13sp"
            ))                           # =====>   SIM FIZ 2 SINTAXES. AMBOS PARA TESTES, COMENTADO PELO MOTIVO: FOI ADC OUTRA PAGINA(COLORS.PY);   < =======
        self.add_widget(root)"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from colors import *


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"
        self.md_bg_color = COR_FUNDO
        self._build_ui()

    def _build_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=COR_FUNDO,
            padding=[dp(32), dp(48)],
            spacing=dp(24),
        )

# ------- Título -------
        root.add_widget(MDLabel(
            text="TRUCO DOS PIÁ",
            font_size="50sp",
            bold=True,
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
            size_hint_y=None,
            height=dp(56),
        ))
        root.add_widget(MDLabel(
            text="Marcador de Pontos",
            font_size="26sp",
            theme_text_color="Custom",
            text_color=[0.75, 0.65, 0.4, 1],
            halign="center",
            size_hint_y=None,
            height=dp(28),
            )
        )

        root.add_widget(MDLabel(
            size_hint_y=None,
            height=dp(32))
        )

# ------- Botões do menu -------
        for texto, tela in [
            ("Nova Partida",    "setup"),
            ("Jogadores"   ,  "players"),
            ("Histórico"   ,  "history"),
        ]:
            btn = MDButton(
                style="filled",
                theme_width= "Custom",
                size_hint=(1, None),
                height=dp(58),
            )

            btn.md_bg_color = COR_BTN

            btn.add_widget(
                MDButtonText(
                    text=texto,
                    font_size="18sp",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    theme_text_color="Custom",
                    text_color=[1, 1, 1, 1],
               )
            )

            btn.bind(
                on_release=lambda x, t=tela: 
                setattr(self.manager, "current", t)
            )

            root.add_widget(btn)

# ------- Rodapé -------
        root.add_widget(MDLabel(size_hint_y=None, height=dp(32)))

        root.add_widget(MDLabel(
            text="Vai jogar viado!?",
            font_size="13sp",
            theme_text_color="Custom",
            text_color=COR_TEXTO_SEC,
            halign="center",
        ))

        self.add_widget(root)