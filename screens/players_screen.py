from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton, MDButtonIcon
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.dialog import (
    MDDialog, MDDialogHeadlineText,
    MDDialogContentContainer, MDDialogButtonContainer
)
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation

import os, shutil
import database as db
import audio_manager as am
from colors import *

try:
    from plyer import filechooser
    PLYER_OK = True
except Exception:
    PLYER_OK = False

PASTA_FOTOS = os.path.join(os.path.dirname(__file__), "..", "assets", "fotos")
os.makedirs(PASTA_FOTOS, exist_ok=True)

TIPOS_SOM = {
    "ponto":   "Ponto",
    "truco":   "Truco!",
    "flor":    "Flor!",
    "derrota": "Derrota",
}

def _snack(texto):
    from kivy.clock import Clock
    from kivymd.uix.label import MDLabel as ML
    lbl = ML(
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


class PlayersScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "players"
        self.dialog_limpar = None
        self.md_bg_color = COR_FUNDO
        self.dialog_add   = None
        self.dialog_audio = None
        self._build_ui()

# ------- ÓÓÓóóóhh o pau torando, eita porraaa!! Aqui jaz o UI !!! -------
    def _build_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=COR_FUNDO
            )

# ------- Óóh a cabeça -------
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            padding=[dp(8), dp(8)],
            md_bg_color=COR_HEADER,
        )
        btn_back = MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=COR_DOURADO
            )

        btn_back.bind(on_release=lambda x: 
                      setattr(self.manager, "current", "home")
                      )
        btn_add = MDIconButton(
            icon="account-plus",
            theme_icon_color="Custom",
            icon_color=COR_DOURADO
            )
        btn_add.bind(
            on_release=lambda x:
                    self._abrir_dialog_add()
        )

        header.add_widget(btn_back)

        header.add_widget(MDLabel(
            text="Jogadores",
            font_size="20sp",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
        ))
        header.add_widget(btn_add)

# -------- Apagando os jogadores --------
        btn_limpar = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint=(1,None),
            height=dp(46),
        )

        btn_limpar.md_bg_color = [0.7, 0.1, 0.1, 1]

        btn_limpar.add_widget(
            MDButtonText(
                text="LIMPAR JOGADORES",
                font_size="16sp",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
            )
        )

        btn_limpar.bind(
            on_release=lambda x: self._confirmar_limpeza()
        )

# -------- Ta na Lista agr bb !! -------
        scroll = MDScrollView()
        self.lista = MDList(
            padding=[dp(8), dp(8)]
        )
        scroll.add_widget(self.lista)

        root.add_widget(header)
        root.add_widget(btn_limpar)
        root.add_widget(scroll)
        
        self.add_widget(root)

    def on_enter(self):
        self._atualizar_lista()

    def _atualizar_lista(self):
        self.lista.clear_widgets()
        jogadores = db.listar_jogadores()

        if not jogadores:
            card = MDCard(
                orientation="vertical",
                size_hint=(0.85, None),
                height=dp(140),
                pos_hint={"center_x": 0.5},
                padding=dp(24),
                md_bg_color=COR_CARD,
                radius=[dp(16)],
            )
            card.add_widget(MDLabel(
                text="Nenhum palhaço aqui.\nClica nesse +boneco a tua direita, e coloca mais gente nessa merda!",
                halign="center",
                theme_text_color="Custom",
                text_color=COR_TEXTO_SEC
                )
            )
            self.lista.add_widget(card)
            return

        for j in jogadores:
            sons     = am.verificar_sons_jogador(j["nome"])
            gravados = sum(1 for v in sons.values() if v)

            card = MDCard(
                orientation="horizontal",
                size_hint=(1, None),
                height=dp(72),
                padding=[dp(12), dp(8)],
                md_bg_color=COR_CARD,
                radius=[dp(10)],
                spacing=dp(8),
            )
            foto = j.get("foto")
            if foto and os.path.isfile(foto):
                card.add_widget(AsyncImage(
                    source=foto,
                    size_hint=(None, None),
                    size=(dp(48), dp(48)),
                    pos_hint={"center_y": 0.5},
                    allow_stretch=True,
                    keep_ratio=True,
                    )
                )
            else:
                card.add_widget(MDLabel(
                    text="?",
                    font_size="32sp",
                    size_hint=(None, None),
                    size=(dp(48), dp(48)),
                    halign="center",
                    valign="middle",
                    )
                )
            info = MDBoxLayout(orientation="vertical")
            nome_txt = j["nome"] if not j["apelido"] else f"{j['nome']} ({j['apelido']})"
            info.add_widget(MDLabel(
                text=nome_txt,
                theme_text_color="Custom",
                text_color=COR_TEXTO,
                font_size="14sp",
                bold=True)
                )

            info.add_widget(MDLabel(
                text=f"{gravados}/4 audios gravados",
                theme_text_color="Custom",
                text_color=COR_TEXTO_SEC,
                font_size="12sp")
                )

            card.add_widget(info)

            btn_edit = MDIconButton(
                icon="pencil",
                theme_icon_color="Custom",
                icon_color=COR_DOURADO,
                size_hint=(None, None),
                size=(dp(40), dp(40)),
                pos_hint={"center_y": 0.5}
            )

            btn_edit.bind(
                on_release=lambda x,
                        jog=j: self._abrir_perfil(jog)
            )

            card.add_widget(btn_edit)
            self.lista.add_widget(card)

# -------- Metodo para excluir tudo do jogador --------
    def _confirmar_limpeza(self):

        btn_cancelar = MDButton(
            style="text",
        )

        btn_cancelar.add_widget(
            MDButtonText(
                text="CANCELAR",
            )
        )

        btn_apagar = MDButton(
            style="filled",
            theme_width="Custom",
        )

        btn_apagar.md_bg_color = [0.7, 0.1, 0.1, 1]

        btn_apagar.add_widget(
            MDButtonText(
                text="APAGAR",
            )
        )

        self.dialog_limpar = MDDialog(
            MDDialogHeadlineText(
                text="Limpar jogadores?"
            ),

            MDDialogContentContainer(
                MDLabel(
                    text="Todos os jogadores cadastrados serão apagados.",
                    theme_text_color="Custom",
                    text_color=COR_TEXTO,
                    halign="center",
                ),
                orientation="vertical",
            ),

            MDDialogButtonContainer(
                btn_cancelar,
                btn_apagar,
                spacing=dp(8),
            ),
        )

        btn_cancelar.bind(
            on_release=lambda x: self.dialog_limpar.dismiss()
        )

        btn_apagar.bind(
            on_release=lambda x: self._executar_limpeza()
        )

        self.dialog_limpar.open()

    def _executar_limpeza(self):

        try:
            db.limpar_jogadores()

            if self.dialog_limpar:
                self.dialog_limpar.dismiss()
                self.dialog_limpar = None

            self._atualizar_lista()

        except Exception as e:
            print(f"Erro ao limpar jogadores: {e}")
        
# ------- Adicionando jogador -------
    def _abrir_dialog_add(self):
        self.campo_nome    = MDTextField(
             MDTextFieldHintText(
                text="Nome"
                ),
            mode="outlined",
            )
        self.campo_apelido = MDTextField(
             MDTextFieldHintText(
                text="Apelido"
                ),
            mode="outlined",
            )

        btn_cancel = MDButton(style="text")
        btn_cancel.add_widget(MDButtonText(
            text="CANCELAR",
            theme_width="Custom",
            theme_text_color="Custom",
            text_color=COR_TEXTO_SEC,
            halign="center")
            )
        btn_salvar = MDButton(style="filled")
        btn_salvar.md_bg_color = COR_DOURADO
        btn_salvar.add_widget(
            MDButtonText(text="SALVAR")
            )

        self.dialog_add = MDDialog(
            MDDialogHeadlineText(
                text="Novo Jogador"),
            MDDialogContentContainer(
                self.campo_nome,
                self.campo_apelido,
                orientation="vertical",
                spacing=dp(12),
            ),
            MDDialogButtonContainer(
                btn_cancel,
                btn_salvar,
                spacing=dp(8),
            ),
        )
        btn_cancel.bind(
            on_release=lambda x: 
                    self.dialog_add.dismiss()
        )

        btn_salvar.bind(
            on_release=lambda x: 
                    self._salvar_jogador()
        )

        self.dialog_add.open()

    def _salvar_jogador(self):
        nome    = self.campo_nome.text.strip()
        apelido = self.campo_apelido.text.strip()
        if not nome:
            _snack("Digita teu nome pia de merda!")
            return
        try:
            db.cadastrar_jogador(nome, apelido)
            self.dialog_add.dismiss()
            self._atualizar_lista()
            _snack(f"{nome}, ta agr vai jogar. pnc!")
        except ValueError as e:
            _snack(str(e))

# ------- Aqui surge o perfl do atleta completo (foto and audios) -------
    def _abrir_perfil(self, jogador: dict):
        self._jogador_atual = jogador
        sons = am.verificar_sons_jogador(jogador["nome"])

# ------- Foto da carunxa ------
        foto_path = jogador.get("foto")
        self._img_perfil = AsyncImage(
            source=foto_path if foto_path and os.path.isfile(foto_path) else "",
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            keep_ratio=True,
        )
        btn_foto = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint=(None, None),
            height=dp(40), 
            width=dp(160),
            pos_hint={"center_x": 0.5}
        )

        btn_foto.md_bg_color = COR_DOURADO_E

        btn_foto.add_widget(MDButtonText(
            text="Escolher foto"
            )
        )

        btn_foto.bind(
            on_release=lambda x: 
                    self._escolher_foto(jogador)
        )

        foto_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(136)
        )

        foto_box.add_widget(self._img_perfil)
        foto_box.add_widget(btn_foto)

# ------- separador -------
        sep = MDLabel(
            text="Audios do pia",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            font_size="14sp",
            size_hint_y=None,
            height=dp(28)
        )

# ------- Linhas dos áudios -------
        audio_box = MDBoxLayout(
            orientation="vertical", 
            spacing=dp(4),
            size_hint_y=None,
            height=dp(len(TIPOS_SOM) * 56))

        for tipo, label in TIPOS_SOM.items():
            gravado = sons.get(tipo, False)
            audio_box.add_widget(_LinhaAudio(
                jogador=jogador,
                tipo=tipo,
                label=label,
                gravado=gravado,
                on_atualizar=self._atualizar_lista,
            )
        )

        btn_fechar = MDButton(
            style="text",
            theme_width="Custom",
            )

        btn_fechar.add_widget(MDButtonText(
            text="FECHAR",
            theme_text_color="Custom",
            text_color=COR_TEXTO_SEC,
            halign="center"
            )
        )

        self.dialog_audio = MDDialog(
            MDDialogHeadlineText(text=jogador["nome"]),
            MDDialogContentContainer(
                foto_box, sep, audio_box,
                orientation="vertical",
                spacing=dp(8),
            ),
            MDDialogButtonContainer(btn_fechar),
        )
        btn_fechar.bind(
            on_release=lambda x: 
                    self.dialog_audio.dismiss()
        )
        
        self.dialog_audio.bind(
            on_dismiss=lambda *a: [l.cancelar() for l in audio_box.children]
        )
        
        self.dialog_audio.open()

# ------- Aqui resgatando a foto da galeria -------
    def _escolher_foto(self, jogador: dict):
        if not PLYER_OK:
            _snack("Bah cupinxa, muito feio, nem coloca foto tua!")
            return

        def _on_selection(selection):
            if not selection:
                return
            caminho_original = selection[0]

# ------- Este copia a foto para a pasta do app -------
            ext      = os.path.splitext(caminho_original)[1].lower() or ".jpg"
            nome_slug = jogador["nome"].lower().replace(" ", "_")
            destino  = os.path.join(PASTA_FOTOS, f"{nome_slug}{ext}")
            try:
                shutil.copy(caminho_original, destino)
                db.atualizar_foto_jogador(jogador["id"], destino)

# ------- Atualizando a foto c/dialog aberto -------
                self._img_perfil.source = destino
                self._img_perfil.reload()
                self._atualizar_lista()
                _snack("Ta ai, que carunxa em!")
            except Exception as e:
                _snack(f"Nao vi, faz de novo! {e}")

        filechooser.open_file(
            on_selection=_on_selection,
            filters=["*.png", "*.jpg", "*.jpeg"],
            title="Escolher foto de perfil",
        )

# ------- Componente linha do audio -------
class _LinhaAudio(MDBoxLayout):

    DURACAO = 4  # segundos

    def __init__(self, jogador, tipo, label, gravado, on_atualizar, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height      = dp(52)
        self.spacing     = dp(4)
        self.padding     = [dp(4), dp(4)]

        self.jogador      = jogador
        self.tipo         = tipo
        self.gravado      = gravado
        self.on_atualizar = on_atualizar
        self._gravando    = False
        self._evento      = None
        self._tick_ev     = None
        self._play_ev     = None
        self._restante    = 0

# ------- Nome do áudio -------
        self.add_widget(MDLabel(
            text=label,
            size_hint_x=0.52,
            theme_text_color="Custom",
            text_color=COR_TEXTO if gravado else COR_TEXTO_SEC,
            font_size="12sp",
        ))

# ------- Botão gravar -------
        self.btn = MDButton(
            style="filled",
            theme_width="Custom",
            theme_bg_color="Custom",
            md_bg_color=COR_DOURADO_E if gravado else COR_VERMELHO,
            size_hint_x=0.30,
            size_hint_y=None,
            height=dp(42),
        )
        self._icone = MDButtonIcon(
            icon="microphone",
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
        )
        self.btn.add_widget(self._icone)
        self._lbl_btn = MDButtonText(
            text="Regravar" if gravado else "Gravar"
        )
        self.btn.add_widget(self._lbl_btn)
        self.btn.bind(on_release=lambda x: self._iniciar())
        self.add_widget(self.btn)

# ------- Botão ouvir -------
        self.btn_play = MDIconButton(
            icon="play-circle-outline",
            theme_icon_color="Custom",
            icon_color=COR_DOURADO,
            size_hint_x=0.18,
            disabled=not gravado,
        )
        self.btn_play.bind(on_release=lambda x: self._tocar())
        self.add_widget(self.btn_play)

# ---------- efeito de pulso ----------
    def _pulsar(self, widget):
        Animation.cancel_all(widget, "opacity")
        anim = (Animation(opacity=0.25, d=0.5, t="in_out_quad") +
                Animation(opacity=1.0,  d=0.5, t="in_out_quad"))
        anim.repeat = True
        anim.start(widget)

    def _parar_pulso(self, widget):
        Animation.cancel_all(widget, "opacity")
        widget.opacity = 1

# ---------- gravar ----------
    def _iniciar(self):
        if self._gravando:
            return
        self._gravando       = True
        self._restante       = self.DURACAO
        self._lbl_btn.text   = f"{self._restante}s..."
        self.btn.disabled    = True
        self.btn.md_bg_color = COR_VERMELHO
        self._pulsar(self._icone)
        am.gravador.iniciar()
        self._evento  = Clock.schedule_once(self._parar, self.DURACAO)
        self._tick_ev = Clock.schedule_interval(self._tick, 1)

    def _tick(self, dt):
        self._restante -= 1
        if self._restante > 0:
            self._lbl_btn.text = f"{self._restante}s..."

    def _parar(self, dt=None):
        if self._evento:
            self._evento.cancel()
            self._evento = None
        if self._tick_ev:
            self._tick_ev.cancel()
            self._tick_ev = None
        self._parar_pulso(self._icone)

        dados   = am.gravador.parar()
        caminho = am.caminho_som(self.jogador["nome"], self.tipo)
        ok      = am.gravador.salvar(dados, caminho)

        if ok:
            db.atualizar_som_jogador(self.jogador["id"], self.tipo, caminho)
            self.gravado           = True
            self._lbl_btn.text     = "Regravar"
            self.btn.md_bg_color   = COR_DOURADO_E
            self.btn_play.disabled = False
        else:
            self._lbl_btn.text   = "Gravar"
            self.btn.md_bg_color = COR_VERMELHO
        self.btn.disabled = False
        self._gravando    = False

        if self.on_atualizar:
            self.on_atualizar()

# ---------- reproduzindo ----------
    def _tocar(self):
        am.reproduzir_som_jogador(self.jogador["nome"], self.tipo)
        self.btn_play.icon = "volume-high"
        self._pulsar(self.btn_play)
        if self._play_ev:
            self._play_ev.cancel()
        self._play_ev = Clock.schedule_once(self._fim_play, self.DURACAO + 0.3)

    def _fim_play(self, dt):
        self._parar_pulso(self.btn_play)
        self.btn_play.icon = "play-circle-outline"
        self._play_ev = None

# ---------- chamado quando o diálogo fecha ----------
    def cancelar(self):
        for ev in (self._evento, self._tick_ev, self._play_ev):
            if ev:
                ev.cancel()
        self._evento = self._tick_ev = self._play_ev = None
        if self._gravando:
            am.gravador.parar()   # descarta sem salvar
            self._gravando = False
        self._parar_pulso(self._icone)
        self._parar_pulso(self.btn_play)