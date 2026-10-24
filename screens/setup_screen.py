from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.metrics import dp
from colors import *
import database as db
from game_logic import sortear_duplas_sem_repeticao


def _snack(texto):
    from kivy.clock import Clock
    from kivymd.uix.label import MDLabel
    from kivy.core.window import Window
    lbl = MDLabel(
        text=texto,
        theme_text_color="Custom",
        text_color=[1, 1, 1, 1],
        font_size="14sp",
        halign="center",
        size_hint=(0.85, None),
        height=dp(48),
        pos_hint={"center_x": 0.5},
        y=dp(24),
        md_bg_color=[0.2, 0.14, 0.04, 1],
    )
    Window.add_widget(lbl)
    Clock.schedule_once(lambda dt: Window.remove_widget(lbl), 2.5)

class SetupScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "setup"
        self.md_bg_color = COR_FUNDO
        self.selecionados = set()
        self.time1 = []
        self.time2 = []
        self.modo_jogo = "2x2"
        self._build_ui()

    def _build_ui(self):
        root = MDBoxLayout(
            orientation="vertical", 
            md_bg_color=COR_FUNDO
        )

# -------  Header  --------
        header = MDBoxLayout(
            orientation="horizontal", 
            size_hint_y=None,
            height=dp(60),
            padding=[dp(8),dp(8)], 
            md_bg_color=COR_HEADER
        )

        btn_back = MDIconButton(
            icon="arrow-left", 
            theme_icon_color="Custom", 
            icon_color=COR_DOURADO
            )

        btn_back.bind(
            on_release=lambda x: 
            setattr(self.manager, "current", "home"))

        header.add_widget(btn_back)

        header.add_widget(MDLabel(
            text="Nova Partida", 
            font_size="20sp",
            theme_text_color="Custom", 
            text_color=COR_DOURADO, 
            halign="center"
            )
        )

        header.add_widget(MDLabel(
            size_hint_x=None,
            width=dp(48)
            )
        )

        scroll = MDScrollView(size_hint_y=0.42)
        self.lista = MDList(padding=[dp(8),dp(4)])

        scroll.add_widget(self.lista)

        self.card_times = MDCard(
            orientation="vertical", 
            size_hint=(0.92,None),
            height=dp(110), 
            pos_hint={"center_x":0.5},
            padding=dp(16), 
            md_bg_color=COR_CARD, 
            radius=[dp(12)]
        )

        self.label_times = MDLabel(
            text="Escolhe os piá, e eu faço as duplas!",
            theme_text_color="Custom",
            text_color=COR_TEXTO_SEC,
            halign="center",
            font_size="13sp"
        )

        self.card_times.add_widget(self.label_times)

        btn_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            spacing=dp(12),
            padding=[dp(16),dp(8)]
        )

        self.btn_sortear = MDButton(
            style="filled", 
            theme_width="Custom",
            height=dp(50)
        )

        self.btn_sortear.md_bg_color = COR_DOURADO_E

        self.btn_sortear.add_widget(MDButtonText(
            text=" Sortear",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )

        self.btn_sortear.bind(on_release=lambda x: self._sortear())

        self.btn_jogar = MDButton(
            style="filled", 
            theme_width="Custom",
            height=dp(50), 
            disabled=True
        )

        self.btn_jogar.md_bg_color = COR_VERDE

        self.btn_jogar.add_widget(MDButtonText(
            text="Começar!",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )

        self.btn_jogar.bind(on_release=lambda x: self._iniciar_partida())

        btn_box.add_widget(self.btn_sortear)

        btn_box.add_widget(self.btn_jogar)

        root.add_widget(header)

# ------- Modo de jogo -------
        root.add_widget(MDLabel(
            text="Modo de jogo:",
            theme_text_color="Custom",
            text_color=COR_TEXTO_SEC,
            halign="center",
            size_hint_y=None,
            height=dp(32),
        ))

        modo_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8),
            padding=[dp(12), dp(4)],
        )

        self.btn_1x1 = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint_x=0.33,
            height=dp(42),
        )
        self.btn_1x1.md_bg_color = COR_DOURADO_E
        self.btn_1x1.add_widget(
            MDButtonText(
                text="1 x 1",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )
        self.btn_1x1.bind(
            on_release=lambda x: self._selecionar_modo("1x1")
        )

        self.btn_2x2 = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint_x=0.33,
            height=dp(42),
        )
        self.btn_2x2.md_bg_color = COR_VERDE
        self.btn_2x2.add_widget(
            MDButtonText(
                text="2 x 2",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )
        self.btn_2x2.bind(
            on_release=lambda x: self._selecionar_modo("2x2")
        )

        self.btn_caranxo = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint_x=0.34,
            height=dp(42),
        )
        self.btn_caranxo.md_bg_color = COR_DOURADO_E
        self.btn_caranxo.add_widget(
            MDButtonText(
                text="Caranxo",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )
        self.btn_caranxo.bind(
            on_release=lambda x: self._selecionar_modo("caranxo")
        )

        modo_box.add_widget(self.btn_1x1)
        modo_box.add_widget(self.btn_2x2)
        modo_box.add_widget(self.btn_caranxo)

        root.add_widget(modo_box)

        root.add_widget(MDLabel(
            text="Selecione os Piá:",
            theme_text_color="Custom", 
            text_color=COR_TEXTO_SEC,
            halign="center",
            size_hint_y=None, 
            height=dp(36), 
            padding=[dp(16),0]
            )
        )

        root.add_widget(scroll)

        root.add_widget(MDLabel(
            size_hint_y=None, 
            height=dp(8)
            )
        )

        root.add_widget(self.card_times)
        root.add_widget(MDLabel(
            size_hint_y=None, 
            height=dp(8)
            )
        )

        root.add_widget(btn_box)
        self.add_widget(root)

    def on_enter(self):
        self.selecionados.clear()
        self.time1 = []
        self.time2 = []
        self.btn_jogar.disabled = True
        self.label_times.text = " Selecione os piá e sorteia!"
        self._carregar_jogadores()

    def _carregar_jogadores(self):

        self.lista.clear_widgets()
        jogadores = db.listar_jogadores()

        if not jogadores:
            self.lista.add_widget(MDLabel(
                text="Nenhum Piá!\nVai nos piá e adiciona esse gay.",
                halign="center", 
                theme_text_color="Custom", 
                text_color=COR_TEXTO_SEC,
                size_hint_y=None, 
                height=dp(60)
                )
            )
            return
        for j in jogadores:
            linha = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(48),
                padding=[dp(8),dp(4)]
            )

            cb = MDCheckbox(
                size_hint=(None,None), 
                size=(dp(36),dp(36)), 
                pos_hint={"center_y":0.5})

            cb.bind(active=lambda w, v, nome=j["nome"]: self._toggle(nome, v))

            nome_txt = j["nome"] if not j["apelido"] else f"{j['nome']} ({j['apelido']})"

            linha.add_widget(cb)
            linha.add_widget(MDLabel(
                        text=nome_txt,
                        theme_text_color="Custom", 
                        text_color=COR_TEXTO
                        )
                    )

            self.lista.add_widget(linha)

    def _selecionar_modo(self, modo):
        self.modo_jogo = modo

        self.selecionados.clear()
        self.time1 = []
        self.time2 = []
        self.btn_jogar.disabled = True

        if modo == "1x1":
            self.label_times.text = "1 x 1: escolha 2 piá!"
            _snack("Modo 1 x 1 selecionado!")

        elif modo == "2x2":
            self.label_times.text = "2 x 2: escolha 4 piá!"
            _snack("Modo 2 x 2 selecionado!")

        elif modo == "caranxo":
            self.label_times.text = "Caranxo: escolha 3 piá!"
            _snack("Modo Caranxo selecionado!")

        self._carregar_jogadores()

    def _toggle(self, nome, ativo):

        if ativo:
            self.selecionados.add(nome)
        else:
            self.selecionados.discard(nome)

        self.time1 = []
        self.time2 = []
        self.btn_jogar.disabled = True

        quantidade = {
            "1x1": 2,
            "2x2": 4,
            "caranxo": 3,
        }

        necessario = quantidade[self.modo_jogo]

        self.label_times.text = (
            f"Selecionados: {len(self.selecionados)}/{necessario}"
        )

    def _sortear(self):
        jogadores = list(self.selecionados)

        quantidade = {
            "1x1": 2,
            "2x2": 4,
            "caranxo": 3,
        }

        necessario = quantidade[self.modo_jogo]

        if len(jogadores) != necessario:
            _snack(
                f"Para {self.modo_jogo}, escolha exatamente "
                f"{necessario} piá!"
            )
            return

# ------- 1 x 1 -------
        if self.modo_jogo == "1x1":
            import random

            random.shuffle(jogadores)

            self.time1 = [jogadores[0]]
            self.time2 = [jogadores[1]]

            self.label_times.text = (
                f"{self.time1[0]}\n\n"
                f"VS\n\n"
                f"{self.time2[0]}"
            )

            self.btn_jogar.disabled = False
            _snack("1 x 1 sorteado!")
            return

# ------- 2 x 2 -------
        if self.modo_jogo == "2x2":
            historico = [
                (r["jogador1"], r["jogador2"])
                for r in db.ranking_duplas()
            ]

            self.time1, self.time2 = sortear_duplas_sem_repeticao(
                jogadores,
                historico
            )

            self.label_times.text = (
                f"{' & '.join(self.time1)}\n\n"
                f"VS\n\n"
                f"{' & '.join(self.time2)}"
            )

            self.btn_jogar.disabled = False
            _snack("Duplas sorteadas!")
            return

# ------- Caranxo -------
        if self.modo_jogo == "caranxo":
            import random

            random.shuffle(jogadores)

            self.time1 = jogadores
            self.time2 = []

            self.label_times.text = (
                f"{jogadores[0]}\n"
                f"{jogadores[1]}\n"
                f"{jogadores[2]}"
            )

            self.btn_jogar.disabled = False
            _snack("Caranxo sorteado!")
    
    def _iniciar_partida(self):

        if not self.time1:
            return

        if self.modo_jogo in ("1x1", "2x2") and not self.time2:
            return

        from kivy.app import App

        App.get_running_app().iniciar_partida(
            self.time1,
            self.time2,
            self.modo_jogo
        )

        self.manager.current = "game"