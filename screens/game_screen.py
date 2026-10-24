from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.clock import Clock
import time as _time
import database as db
import audio_manager as am
from colors import *
from game_logic import EstadoPartida

COR_FUNDO     = [0.08, 0.05, 0.02, 1]
COR_HEADER    = [0.12, 0.07, 0.02, 1]
COR_DOURADO   = [0.85, 0.65, 0.1,  1]
COR_DOURADO_E = [0.3,  0.2,  0.05, 1]
COR_VERDE     = [0.1,  0.45, 0.1,  1]
COR_VERMELHO  = [0.7,  0.15, 0.05, 1]
COR_AZUL      = [0.1,  0.25, 0.55, 1]
COR_CARD      = [0.14, 0.09, 0.03, 1]
COR_TEXTO     = [0.9,  0.8,  0.5,  1]
COR_TEXTO_SEC = [0.6,  0.5,  0.3,  1]

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
        pos_hint={"center_x": .5},
        y=dp(24),
        md_bg_color=[0.2, 0.14, 0.04, 1],
    )
    Window.add_widget(lbl)
    Clock.schedule_once(lambda dt: Window.remove_widget(lbl), 2.5)

def _btn(texto, cor, cb, size_x=.5, font="13sp"):
    b = MDButton(
        style="filled",
        theme_width="Custom",
        size_hint_x=size_x,
        size_hint_y=None,
        height=dp(46),
    )

    b.md_br_color = cor

    b.add_widget(
        MDButtonText(
            text=texto,
            font_size=font,
            pos_hint={"center_x": .5, "center_y": .5},
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
        )
    )

    b.bind(on_release=cb)

    return b

class GameScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name        = "game"
        self.estado      = None
        self.audio_jogo  = None
        self._inicio     = None
        self._dialog_fim = None
        self._build_ui()

# ------- Aqui jaz o UI -------
    def _build_ui(self):
        
        root = MDBoxLayout(
            orientation="vertical", 
            md_bg_color=COR_FUNDO,
            )

# ------- CabeçALHO -------
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            padding=[dp(4), dp(4)],
            md_bg_color=COR_HEADER,
        )
        
        btn_undo = MDIconButton(
            icon="undo-variant",
            theme_icon_color="Custom",
            icon_color=COR_DOURADO,
        )
        btn_undo.bind(on_release=lambda x: self._desfazer())

        self.label_mao = MDLabel(
            text="Mão 1",
            font_size="20sp",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
            valign="middle",
        )
        
        btn_flag = MDIconButton(
            icon="flag-checkered",
            theme_icon_color="Custom",
            icon_color=COR_VERMELHO,
        )
        btn_flag.bind(on_release=lambda x: self._confirmar_encerrar())
        
        header.add_widget(btn_undo)
        header.add_widget(self.label_mao)
        header.add_widget(btn_flag)
        
        root.add_widget(header)

# ------- Placar Central -------
        placar_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(150),
            padding=[dp(8), dp(8)],
            spacing=dp(8),
        )

# ------- Time 1 -------
        self.card_t1 = self._card_time("time1")
        placar_box.add_widget(self.card_t1)

# ------ Versus -------
        vs_box = MDBoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(32),
        )
        
        vs_box.add_widget(
            MDLabel(
                text="VS",
                font_size="13sp",
                theme_text_color="Custom",
                text_color=COR_TEXTO_SEC,
                halign="center",
                valign="middle",
            )
        )
        
        placar_box.add_widget(vs_box)

# ------- Time 2 -------
        self.card_t2 = self._card_time("time2")
        placar_box.add_widget(self.card_t2)
        
        root.add_widget(placar_box)

# ------- Valor da mão -------
        self.label_valor = MDLabel(
            text="Mão vale: 1 ponto",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
            valign="middle",
            font_size="14sp",
            size_hint_y=None,
            height=dp(28),
        )
        root.add_widget(self.label_valor)

# ------- Botões de ponto -------
        ponto_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(54),
            spacing=dp(8),
            padding=[dp(8), dp(2)],
        )
        self.btn_pt1 = _btn("+ Ponto T1", 
                            COR_VERDE,
                            lambda x: self._marcar_ponto("time1"), 
                            font="15sp",
                            )
        self.btn_pt2 = _btn("+ Ponto T2", 
                            COR_AZUL,
                            lambda x: self._marcar_ponto("time2"), 
                            font="15sp",
                            )

        ponto_box.add_widget(self.btn_pt1)
        ponto_box.add_widget(self.btn_pt2)

        root.add_widget(ponto_box)

# ------- Botões de TRUCO -------
        root.add_widget(MDLabel(
            text="TRUCO",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
            valign="middle",
            font_size="13sp",
            size_hint_y=None,
            height=dp(30),
        ))
        
        truco_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8),
            padding=[dp(8), dp(2)],
        )
        self.btn_tr1 = _btn("Truco T1",
                            COR_VERMELHO,
                            lambda x: self._pedir_truco("time1"),
                            font="13sp",
                            )
        self.btn_tr2 = _btn("Truco T2",
                            COR_VERMELHO,
                            lambda x: self._pedir_truco("time2"),
                            font="13sp",
                            )

        truco_box.add_widget(self.btn_tr1)
        truco_box.add_widget(self.btn_tr2)

        root.add_widget(truco_box)

# -------- Resposta Truco -------
        self.resp_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8),
            padding=[dp(8), dp(2)],
        )
        
        self.btn_quero  = _btn(
            "Quero",
            COR_VERDE,
            lambda x: self._aceitar_truco(),
            font="13sp",
            )
        self.btn_nquero = _btn(
            "Não Quero",
            COR_VERMELHO,
            lambda x: self._recusar_truco(),
            font="13sp",
            )

        self.resp_box.add_widget(self.btn_quero)
        self.resp_box.add_widget(self.btn_nquero)
        
        self.resp_box.opacity = 0

        root.add_widget(self.resp_box)

# ------- Envido -------
        root.add_widget(MDLabel(
            text="Envido",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
            valign="middle",
            font_size="13sp",
            size_hint_y=None,
            height=dp(30),
        )
    )
        
        envido_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(46),
            spacing=dp(8),
            padding=[dp(8), dp(2)],
        )

        btn_env_t1 = _btn(
            "Env T1",      
            COR_DOURADO_E, 
            lambda x: self._registrar_envido("time1", 2),
            font="12sp",
        )

        btn_env_t2 = _btn(
            "Env T1",      
            COR_DOURADO_E, 
            lambda x: self._registrar_envido("time2", 2),
            font="12sp",
        )

        envido_box.add_widget(btn_env_t1)
        envido_box.add_widget(btn_env_t2)

        root.add_widget(envido_box)

# -------- Falta Envidoooo -------
        falta_envido_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(46),
            spacing=dp(8),
            padding=[dp(8), dp(2)],
        )

        btn_fenv_t1 = _btn(
            "F. Env T1",      
            COR_DOURADO_E, 
            lambda x: self._registrar_falta_envido("time1"),
            font="12sp",
        )

        btn_fenv_t2 = _btn(
            "F. Env T2",      
            COR_DOURADO_E, 
            lambda x: self._registrar_falta_envido("time2"),
            font="12sp",
        )

        falta_envido_box.add_widget(btn_fenv_t1)
        falta_envido_box.add_widget(btn_fenv_t2)

        root.add_widget(falta_envido_box)

# ------- Espaço das cheirosas -----   => OBS: i love the flowers <=
        root.add_widget(MDLabel(
            text="FLOR",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
            valign="middle",
            font_size="13sp",
            size_hint_y=None,
            height=dp(30),
        )
    )

        flor_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8),
            padding=[dp(8), dp(2)],
        )

        self.btn_flor1 = _btn(
            "Flor T1", 
            COR_DOURADO_E,
            lambda x: self._registrar_flor("time1"),
            font="13sp",
        )

        self.btn_flor2 = _btn(
            "Flor T2",
            COR_DOURADO_E,
            lambda x: self._registrar_flor("time1"),
            font="13sp",
        )

        flor_box.add_widget(self.btn_flor1)
        flor_box.add_widget(self.btn_flor2)

        root.add_widget(flor_box)

# ------- Achei bom fazer esse espaço entre eles -------
        root.add_widget(
            MDLabel(
                size_hint_y=None,
                height=dp(6),
            )
        )

# ------- Aqui uma nova mão -------
        b_nm = MDButton(
            style="filled",
            size_hint=(0.6, None),
            height=dp(44),
            pos_hint={"center_x": 0.5}
            )
        b_nm.md_bg_color = COR_DOURADO_E
        
        b_nm.add_widget(
            MDButtonText(
            text="Nova Mão",
            font_size="13sp",
            pos_hint={"center_x": .5, "center_y": .5},
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            )
        )
        b_nm.bind(on_release=lambda x: self._nova_mao())

        root.add_widget(b_nm)

# ------- Espaço final -------

        root.add_widget(
            MDLabel(
                size_hint_y=None,
                height=dp(8)
            )
        )
        
        self.add_widget(root)

    def _card_time(self, time_id: str) -> MDCard:

        card = MDCard(
            orientation="vertical",
            md_bg_color=COR_CARD,
            radius=[dp(8)],
            padding=dp(8),
        )
        nome_label = MDLabel(
            text="Time",
            theme_text_color="Custom",
            text_color=COR_TEXTO_SEC,
            halign="center",
            font_size="12sp",
            size_hint_y=None,
            height=dp(24),
        )
        pts_label = MDLabel(
            text="0",
            font_size="32sp",
            theme_text_color="Custom",
            text_color=COR_DOURADO,
            halign="center",
            bold=True,
        )
        falta_label = MDLabel(
            text="falta 24",
            theme_text_color="Custom",
            text_color=COR_TEXTO_SEC,
            halign="center",
            font_size="11sp",
            size_hint_y=None,
            height=dp(20),
        )

        card.add_widget(nome_label)
        card.add_widget(pts_label)
        card.add_widget(falta_label)

        if time_id == "time1":
            self.nome_t1  = nome_label
            self.pts_t1   = pts_label
            self.falta_t1 = falta_label
        else:
            self.nome_t2  = nome_label
            self.pts_t2   = pts_label
            self.falta_t2 = falta_label
        return card

# ------- Rodando a parada, iniciando -------
    def iniciar(self, estado: EstadoPartida, audio_jogo):
        self.estado     = estado
        self.audio_jogo = audio_jogo
        self._inicio    = _time.time()
        self._atualizar_ui()

    def on_enter(self):
        if self.estado:
            self._atualizar_ui()

# ------- Ações do jogo -------
    def _marcar_ponto(self, time: str):
        if not self.estado or self.estado.partida_encerrada:
            return
        pontos = self.estado.valor_atual_truco()
        self.estado.adicionar_pontos(time, pontos)
        db.atualizar_placar(
            self.estado.partida_id,
            self.estado.pontos_time1,
            self.estado.pontos_time2,
        )
        if self.audio_jogo:
            self.audio_jogo.ponto_feito(time)
        self._atualizar_ui()
        if self.estado.partida_encerrada:
            Clock.schedule_once(lambda dt: self._tela_vitoria(), 0.5)

    def _pedir_truco(self, time: str):

        if not self.estado:
            return

        if not self.estado.pode_pedir_truco(time):
            _snack("Não é mais possível pedir Truco!")

            return

        novo, aceito, recusado = self.estado.pedir_truco(time)
        nomes = {"truco": "TRUCO", "retruco": "RETRUCO", "vale4": "VALE 4"}

        _snack(f"{nomes[novo]}! Aceito={aceito}pts | Recusado={recusado}pts")

        if self.audio_jogo:
            self.audio_jogo.truco_pedido(time)

        self.resp_box.opacity = 1

        self._atualizar_ui()

    def _aceitar_truco(self):

        if not self.estado:
            return

        pts = self.estado.aceitar_truco()
        self.resp_box.opacity = 0

        _snack(f"Truco aceito! Vale {pts} pontos.")
        self._atualizar_ui()

    def _recusar_truco(self):

        if not self.estado:
            return

        time_leva, pts = self.estado.recusar_truco()
        self.resp_box.opacity = 0

        nomes = self._nomes_times()

        _snack(f"{nomes[time_leva]} leva {pts} ponto(s)! (não quis)")

        db.atualizar_placar(
            self.estado.partida_id,
            self.estado.pontos_time1,
            self.estado.pontos_time2,
        )

        self._atualizar_ui()

        if self.estado.partida_encerrada:
            Clock.schedule_once(lambda dt: self._tela_vitoria(), 0.5)

    def _registrar_envido(self, time_vencedor: str, valor: int):

        if not self.estado:
            return

        self.estado.adicionar_pontos(time_vencedor, valor)

        db.atualizar_placar(
            self.estado.partida_id,
            self.estado.pontos_time1,
            self.estado.pontos_time2,
        )
        nomes = self._nomes_times()

        _snack(f"Envido: {nomes[time_vencedor]} ganha {valor} ponto(s)!")

        self._atualizar_ui()

    def _registrar_falta_envido(self, time_vencedor: str):

        if not self.estado:
            return

        valor = self.estado.valor_falta_envido(time_vencedor)

        self.estado.adicionar_pontos(time_vencedor, valor)

        db.atualizar_placar(
            self.estado.partida_id,
            self.estado.pontos_time1,
            self.estado.pontos_time2,
        )
        nomes = self._nomes_times()

        _snack(f"Falta Envido: {nomes[time_vencedor]} ganha {valor} ponto(s)!")

        self._atualizar_ui()

        if self.estado.partida_encerrada:
            Clock.schedule_once(lambda dt: self._tela_vitoria(), 0.5)

    def _registrar_flor(self, time: str):

        if not self.estado:
            return

        outro = "time2" if time == "time1" else "time1"  # Peça q verifica se ambos tem flor, no caso, flor ao resto!

        valor = self.estado.valor_flor_ao_resto()

        self.estado.adicionar_pontos(time, 3)

        db.atualizar_placar(
            self.estado.partida_id,
            self.estado.pontos_time1,
            self.estado.pontos_time2,
        )
        nomes = self._nomes_times()

        _snack(f"Flor! {nomes[time]} ganha 3 pontos.")

        if self.audio_jogo:
            self.audio_jogo.flor_cantada(time)

        self._atualizar_ui()

    def _nova_mao(self):

        if not self.estado:
            return

        self.estado.resetar_mao()
        self.resp_box.opacity = 0

        _snack(f"Mão {self.estado.numero_mao}! Vez do {self._nomes_times()[self.estado.time_mao]}.")

        self._atualizar_ui()

    def _desfazer(self):

        if not self.estado:
            return

        if self.estado.desfazer_ultimo_ponto():

            _snack("↩ Último ponto desfeito!")

            db.atualizar_placar(
                self.estado.partida_id,
                self.estado.pontos_time1,
                self.estado.pontos_time2,
            )

            self._atualizar_ui()

        else:
            _snack("Nada para desfazer.")

# ------- Atualização da UI -------
    def _atualizar_ui(self):

        if not self.estado:
            return

        e     = self.estado
        nomes = self._nomes_times()

# ------- Placar -------
        self.nome_t1.text  = nomes["time1"]
        self.pts_t1.text   = str(e.pontos_time1)
        self.falta_t1.text = f"falta {e.pontos_faltando('time1')}"
        self.nome_t2.text  = nomes["time2"]
        self.pts_t2.text   = str(e.pontos_time2)
        self.falta_t2.text = f"falta {e.pontos_faltando('time2')}"

# ------- Mão e valores -------
        self.label_mao.text   = f"Mão {e.numero_mao}"
        self.label_valor.text = f"Mão vale: {e.valor_atual_truco()} ponto(s)."

# ------- Botões de truco OBS: atualiza label com estado atual -------
        estados     = {"normal": "Truco", "truco": "Retruco", "retruco": "Vale 4", "vale4": "Vale 4"}
        label_truco = estados.get(e.estado_truco, "Truco")
        pode_t1     = e.pode_pedir_truco("time1")
        pode_t2     = e.pode_pedir_truco("time2")
        for w in self.btn_tr1.children:
            if hasattr(w, 'text'): w.text = f"{label_truco} T1"
        for w in self.btn_tr2.children:
            if hasattr(w, 'text'): w.text = f"{label_truco} T2"
        self.btn_tr1.disabled = not pode_t1
        self.btn_tr2.disabled = not pode_t2

    def _nomes_times(self) -> dict:
        if not self.estado:
            return {"time1": "Time 1", "time2": "Time 2"}
        return {
            "time1": " & ".join(self.estado.time1),
            "time2": " & ".join(self.estado.time2),
        }

# ------- Fim de partidaaaa -------
    def _tela_vitoria(self):
        if not self.estado:
            return
        vencedor = self.estado.vencedor_partida
        nomes    = self._nomes_times()
        perdedor = "time2" if vencedor == "time1" else "time1"

        duracao = int((_time.time() - self._inicio) / 60) if self._inicio else 0
        db.finalizar_partida(self.estado.partida_id, vencedor, duracao)

        for jog in self.estado.time1:
            for par in self.estado.time1:
                if jog < par:
                    db.registrar_resultado_dupla(jog, par, vencedor == "time1")
        for jog in self.estado.time2:
            for par in self.estado.time2:
                if jog < par:
                    db.registrar_resultado_dupla(jog, par, vencedor == "time2")

        if self.audio_jogo:
            self.audio_jogo.partida_encerrada(vencedor, perdedor)

        from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer

        btn_hist = MDButton(style="text")
        btn_hist.add_widget(MDButtonText(text="HISTORICO"))

        btn_nova = MDButton(style="filled")
        btn_nova.md_bg_color = COR_VERDE

        btn_nova.add_widget(MDButtonText(text="NOVA PARTIDA"))

        self._dialog_fim = MDDialog(
            MDDialogHeadlineText(text=f"{nomes[vencedor]} Venceu!"),
            MDDialogSupportingText(
                text=(
                    f"{nomes[vencedor]}: {self.estado.pontos_time1 if vencedor == 'time1' else self.estado.pontos_time2} pts\n"
                    f"{nomes[perdedor]}: {self.estado.pontos_time2 if vencedor == 'time1' else self.estado.pontos_time1} pts\n"
                    f"Duracao: {duracao} min."
                ),
            ),
            MDDialogButtonContainer(btn_hist, btn_nova, spacing=dp(8)),
        )

        btn_hist.bind(on_release=lambda x: self._ir_historico())
        btn_nova.bind(on_release=lambda x: self._nova_partida())

        self._dialog_fim.open()

    def _ir_historico(self):

        if self._dialog_fim:
            self._dialog_fim.dismiss()
        self.manager.current = "history"

    def _nova_partida(self):

        if self._dialog_fim:
            self._dialog_fim.dismiss()
        self.manager.current = "setup"

# ----- etapa de cancelamento da partida, tio!!  -------
    def _confirmar_encerrar(self):

        from kivymd.uix.dialog import MDDialog

        btn_cancel = MDButton(style="text")
        btn_cancel.add_widget(MDButtonText(text="CANCELAR"))

        btn_enc = MDButton(style="filled")
        btn_enc.md_bg_color = COR_VERMELHO
        btn_enc.add_widget(MDButtonText(text="ENCERRAR"))

        d = MDDialog(
             MDLabel(
                text="Saporra vai ser finalizada sem registrar vencedor.",
                theme_text_color="Custom", 
                text_color=COR_TEXTO, 
                halign="center",
            ),

            buttons=[btn_cancel, btn_enc],
        )

        btn_cancel.bind(on_release=lambda x: d.dismiss())
        
        btn_enc.bind(on_release=lambda x: (d.dismiss(), 
                                           setattr(self.manager,
                                                    "current", "home")
                                            )
        )

        d.open()

# ------- sei lá, vou chamar de Utilitário -------
    def _snack(self, texto: str):

        from kivymd.uix.snackbar import MDSnackbar
        MDSnackbar(
            MDLabel(
             text=texto,
             theme_text_color="Custom",
             text_color=[1, 1, 1, 1]),
             md_bg_color=[0.2, 0.14, 0.04, 1],
        ).open()