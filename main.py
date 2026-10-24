from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

import database as db
import audio_manager as am
from game_logic import EstadoPartida
from screens.home_screen    import HomeScreen
from screens.players_screen import PlayersScreen
from screens.setup_screen   import SetupScreen
from screens.game_screen    import GameScreen
from screens.history_screen import HistoryScreen
 
class TrucoApp(MDApp):
 
    def build(self):
# ------- Inicializa banco de dados -------
        db.inicializar_banco()
 
        self.theme_cls.theme_style   = "Dark"
        self.theme_cls.primary_color = "#D4A017"   # dourado
 
# ------- Gerenciador de telas -------
        sm = MDScreenManager()
        sm.add_widget(HomeScreen())
        sm.add_widget(PlayersScreen())
        sm.add_widget(SetupScreen())
        sm.add_widget(GameScreen())
        sm.add_widget(HistoryScreen())
        sm.current = "home"
        return sm
 
    def iniciar_partida(self, time1: list, time2: list, modo_jogo):

# ------- Cria partida no banco -------
        partida_id = db.criar_partida(time1, time2)
 
# ------- Estado do jogo -------
        estado = EstadoPartida(
            modo_jogo=modo_jogo,
            time1=time1,
            time2=time2,
            partida_id=partida_id,
        )
 
# ------- Sistema de áudio -------
        jogadores_db = {j["nome"]: j for j in db.listar_jogadores()}
        nomes_t1 = [j for j in time1 if j in jogadores_db]
        nomes_t2 = [j for j in time2 if j in jogadores_db]
        audio_jogo = am.AudioJogo(nomes_t1, nomes_t2)
 
# ------- Passa pro GameScreen -------
        game = self.root.get_screen("game")
        game.iniciar(estado, audio_jogo)
 
if __name__ == "__main__":
    TrucoApp().run()