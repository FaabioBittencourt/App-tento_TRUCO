import os
import random
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
 
try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    PYGAME_DISPONIVEL = True
except Exception:
    PYGAME_DISPONIVEL = False
    print("Pygame nao encontrado - reprodução desativada.")
 
# ------- Pasta raiz dos áudios -------
PASTA_SONS = os.path.join(os.path.dirname(__file__), "sounds")
 
# ------- Configuraçao de gravação -------
SAMPLE_RATE = 44100 # Hz
CANAIS = 1          # Mono
DURACAO_MAX = 5     # Tempo maxímo de gravação
 
# ------- Estrutura das pastas -------
def garantir_pasta_jogador(nome_jogador: str) -> str:
    nome_slug = nome_jogador.lower().replace(" ", "_")
    pasta = os.path.join(PASTA_SONS, nome_slug)
    os.makedirs(pasta, exist_ok=True)
    return pasta
 
def caminho_som(nome_jogador: str, tipo_som: str) -> str:
    pasta = garantir_pasta_jogador(nome_jogador)
    return os.path.join(pasta, f"{tipo_som}.wav")
 
# ------- Gravação -------
class GravadorAudio:
    def __init__(self):
        self._gravando = False
        self._frames: list = []
        self._stream = None
        self._lock = threading.Lock()
 
    def _callback(self, indata, frames, time_info, status):
        if self._gravando:
            with self._lock:
                self._frames.append(indata.copy())
 
    def iniciar(self): # OBS: Capturando o microfone.
        self._frames = []
        self._gravando = True
        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CANAIS,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()
 
    def parar(self) -> np.ndarray:  # OBS: Aqui ele para a gravação e retorna o array de amostras.
        self._gravando = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        with self._lock:
            if self._frames:
                return np.concatenate(self._frames, axis=0)
            return np.array([], dtype="float32")
 
    def salvar(self, dados: np.ndarray, caminho_destino: str) -> bool: # OBS: Salvando o aúdio em um arquivo .WAV .
        if dados is None or len(dados) == 0:
            print("Fala de novo! Não gravei esse tua voz paia.")
            return False
        try:
            sf.write(caminho_destino, dados, SAMPLE_RATE)
            print(f"Gravada essa tua voz de tchola, em: {caminho_destino}")
            return True
        except Exception as e:
            print(f"Não Gravei essas tuas palavras!{e}")
            return False
 
    def gravar_e_salvar(self, caminho_destino: str, duracao: float = 3.0) -> bool: # OBS: Grava por duração de segundos e salva automático.
        print(f"Gravando por {duracao}s...")
        dados = sd.rec(
            int(duracao * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CANAIS,
            dtype="float32",
        )
        sd.wait()
        return self.salvar(dados, caminho_destino)
 
# ------- Área de instância global reutilizável -------
gravador = GravadorAudio()
 
# ------- Reprodução do Áudio -------  # OBS: Reproduzindo um arquivo .wav .
def reproduzir_som(caminho: str):
    if not PYGAME_DISPONIVEL:
        return
    if not caminho or not os.path.isfile(caminho):
        return
 
    def _tocar():
        try:
            som = pygame.mixer.Sound(caminho)
            som.play()
        except Exception as e:
            print(f"Não consigo reproduzir {caminho}: {e}")
 
    threading.Thread(target=_tocar, daemon=True).start()
 
def reproduzir_som_jogador(nome_jogador: str, tipo_som: str): # OBS: Leva audio do jogador para a respectiva chamada(truco, ponto, flor, etc.).
    caminho = caminho_som(nome_jogador, tipo_som)
    reproduzir_som(caminho)
 
def reproduzir_som_time(time: list, tipo_som: str): # OBS: AHH rapaz, esse sorteia aleatoriamente um jogador e reproduz áudio dele. (100 tocar o msm)!
    jogadores_com_som = [
        j for j in time
        if os.path.isfile(caminho_som(j, tipo_som))
    ]
    if not jogadores_com_som:
        return
 
    escolhido = random.choice(jogadores_com_som)
    reproduzir_som_jogador(escolhido, tipo_som)
 
# ------- Eventos do jogo -------
class AudioJogo:
    def __init__(self, time1: list, time2: list):      # OBS: Organiza a reprodução dos áudios para cada evento do jogo.
        self.times = {"time1": time1, "time2": time2}
 
    def ponto_feito(self, time_vencedor: str):
        reproduzir_som_time(self.times[time_vencedor], "ponto")
 
    def truco_pedido(self, time_pedinte: str, jogador_especifico: str = None):
        if jogador_especifico:
            reproduzir_som_jogador(jogador_especifico, "truco")
        else:
            reproduzir_som_time(self.times[time_pedinte], "truco")
 
    def flor_cantada(self, time: str, jogador_especifico: str = None):
        if jogador_especifico:
            reproduzir_som_jogador(jogador_especifico, "flor")
        else:
            reproduzir_som_time(self.times[time], "flor")
 
    def partida_encerrada(self, time_vencedor: str, time_perdedor: str):
        reproduzir_som_time(self.times[time_vencedor], "ponto")
# OBS: Fiz uma pausa antes da derrota.
        import time as t
        t.sleep(1.5)
        reproduzir_som_time(self.times[time_perdedor], "derrota")
 
# ------- Próximas últimas linhas, vou chamar de utilitários!
def verificar_sons_jogador(nome_jogador: str) -> dict:
    tipos = ["ponto", "truco", "flor", "derrota"]
    return {
        tipo: os.path.isfile(caminho_som(nome_jogador, tipo))
        for tipo in tipos
    }
 
def sons_pendentes(nome_jogador: str) -> list:
    status = verificar_sons_jogador(nome_jogador)
    return [tipo for tipo, gravado in status.items() if not gravado]
 
# ------- TESTE RÁPIDO -------
if __name__ == "__main__":
    import sys
 
    print("  TESTE do AudioManager  ")
    nome = "teste"
    caminho = caminho_som(nome, "ponto")
    print(f"Lugar do som: {caminho}")
 
    resp = input("Gravar 3s de teste? [s/N] ").strip().lower()
    if resp == "s":
        ok = gravador.gravar_e_salvar(caminho, duracao=3.0)
        if ok:
            print("Reproduzindo...")
            reproduzir_som(caminho)
            import time
            time.sleep(4)
    else:
        print("Pulando gravação.")
 
    status = verificar_sons_jogador(nome)
    print(f"Sons do jogador '{nome}': {status}")