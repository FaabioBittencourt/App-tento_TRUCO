from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.icon_definitions import md_icons
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivy.metrics import dp
from colors import *
import database as db

COR_FUNDO     = [0.08, 0.05, 0.02, 1]
COR_HEADER    = [0.12, 0.07, 0.02, 1]
COR_DOURADO   = [0.85, 0.65, 0.1,  1]
COR_CARD      = [0.14, 0.09, 0.03, 1]
COR_CARD2     = [0.10, 0.06, 0.02, 1]
COR_TEXTO     = [0.9,  0.8,  0.5,  1]
COR_TEXTO_SEC = [0.6,  0.5,  0.3,  1]
COR_VERDE     = [0.1,  0.45, 0.1,  1]
COR_VERMELHO  = [0.7,  0.15, 0.05, 1]

class HistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "history"
        self.md_bg_color = COR_FUNDO
        self._build_ui()

    def _build_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=COR_FUNDO
            )
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
            icon_color=COR_DOURADO,
            size_hint=(None, None),
            width=dp(48),
            height=dp(48),
        )

        btn_back.bind(on_release=lambda x: setattr(self.manager, "current", "home"))
        header.add_widget(btn_back)

        header.add_widget(MDLabel(
            text="Histórico & Ranking",
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

        scroll = MDScrollView()

        self.conteudo = MDList(
            padding=[dp(8),dp(8)],
            spacing=dp(8)
            )
        scroll.add_widget(self.conteudo)
        root.add_widget(header)
        root.add_widget(scroll)
        self.add_widget(root)

    def on_enter(self):
        self.conteudo.clear_widgets()
        self._ranking_duplas()
        self._ultimas_partidas()

    def _ranking_duplas(self):
        self.conteudo.add_widget(MDLabel(
            text="Ranking de Duplas",
            font_size="20sp",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            size_hint_y=None,
            height=dp(40),
            padding=[dp(8),0]
            )
        )

        duplas = db.ranking_duplas()
        if not duplas:
            self.conteudo.add_widget(MDLabel(
                text="Nada, te some daqui.",
                theme_text_color="Custom",
                text_color=COR_TEXTO_SEC,
                halign="center",
                size_hint_y=None,
                height=dp(40)
                )
            )
            return

        for i, d in enumerate(duplas[:10]):
            medalha = [i]
            if i < 3:
                posicao = f"{i + 1}º" 
            else:
                posicao = f"{i + 1}º"
            aproveit = d["aproveitamento"] or 0

            card = MDCard(
                orientation="vertical",
                size_hint=(1,None),
                height=dp(80),
                md_bg_color=COR_CARD,
                radius=[dp(10)],
                padding=[dp(12),dp(8)]
            )

            l1 = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(28)
            )

            l1.add_widget(MDLabel(
                text=f"{medalha}  {d['jogador1']} & {d['jogador2']}",
                theme_text_color="Custom",
                text_color=COR_TEXTO,
                font_size="14sp",
                bold=True)
            )

            l1.add_widget(MDLabel(
                text=f"{aproveit}%",
                theme_text_color="Custom",
                text_color=COR_VERDE if aproveit>=50 else COR_VERMELHO,
                halign="right",
                font_size="14sp",
                bold=True
                )
            )
            
            l2 = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(24)
            )

            l2.add_widget(MDLabel(
                text=f" {d['vitorias']}V   {d['derrotas']}D   {d['partidas']}P",
                theme_text_color="Custom", 
                text_color=COR_TEXTO_SEC,
                font_size="12sp"
                )
            )

            card.add_widget(l1); card.add_widget(l2)
            self.conteudo.add_widget(card)

    def _ultimas_partidas(self):
        self.conteudo.add_widget(MDLabel(
            text="Últimas Partidas", 
            font_size="20sp",
            theme_text_color="Custom", 
            text_color=COR_DOURADO,
            size_hint_y=None, 
            height=dp(40), 
            padding=[dp(8),0]))

        partidas = db.listar_partidas(apenas_finalizadas=True)

        if not partidas:
            self.conteudo.add_widget(MDLabel(
                text="Nenhuma partida finalizada.",
                theme_text_color="Custom", 
                text_color=COR_TEXTO_SEC,
                halign="center", 
                size_hint_y=None, 
                height=dp(40)
                )
            )
            return

        for p in partidas[:15]:
            t1 = p["time1_jogadores"].replace(",", " & ")
            t2 = p["time2_jogadores"].replace(",", " & ")
            venc = t1 if p["vencedor"] == "time1" else t2
            data = p["data"][:10] if p["data"] else "?"
            dur  = f"{p['duracao_minutos']}min" if p["duracao_minutos"] else "?"

            card = MDCard(
                orientation="vertical",
                size_hint=(1,None), 
                height=dp(90),
                md_bg_color=COR_CARD2,
                radius=[dp(10)], 
                padding=[dp(12),dp(8)]
            )
            card.add_widget(MDLabel(
                text=f"🏆 {venc}", 
                theme_text_color="Custom",
                text_color=COR_VERDE, 
                font_size="13sp", 
                bold=True,
                size_hint_y=None, 
                height=dp(24)
                )
            )
            card.add_widget(MDLabel(
                text=f"{t1}  {p['placar_time1']} x {p['placar_time2']}  {t2}",
                theme_text_color="Custom", 
                text_color=COR_TEXTO,
                font_size="12sp", 
                size_hint_y=None, 
                height=dp(22)
                )
            )

            card.add_widget(MDLabel(
                text=f" {data}    {dur}",
                theme_text_color="Custom", 
                text_color=COR_TEXTO_SEC,
                font_size="11sp", 
                size_hint_y=None, 
                height=dp(20)
                )
            )

            self.conteudo.add_widget(card)