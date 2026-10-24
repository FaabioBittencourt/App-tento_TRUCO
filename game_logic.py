import random
from dataclasses import dataclass, field
from typing import Optional

PONTOS_PARTIDA = 24 

MODOS_JOGO = {
    "1x1",
    "2x2",
    "caranxo",
}

# ------- Sorteio de duplas -------
def sortear_duplas(jogadores: list) -> tuple: # OBS: Sorteia aleatoriamente.
    
    if len(jogadores) < 2:
        raise ValueError("Precisa de no mínimo 2 cupinxa.")
    if len(jogadores) % 2 != 0:
        raise ValueError("A quantidade de madrinha e padrinho deve ser par.")
    
    embaralhados = jogadores.copy()
    random.shuffle(embaralhados)
    meio = len(embaralhados) // 2
    return embaralhados[:meio], embaralhados[meio:]

def sortear_duplas_sem_repeticao(jogadores: list, historico_duplas: list) -> tuple: # OBS: Aqui fiz para sortear duplas q não tenham jogado juntas (faz até 20 tentativas).

    duplas_anteriores = set(tuple(sorted(d)) for d in historico_duplas)
    for _ in range(20):
        time1, time2 = sortear_duplas(jogadores)
        par1 = tuple(sorted(time1[:2])) if len(time1) >= 2 else None
        par2 = tuple(sorted(time2[:2])) if len(time2) >= 2 else None
        if par1 not in duplas_anteriores and par2 not in duplas_anteriores:
            return time1, time2
    return sortear_duplas(jogadores)

# ------- Estado da rodada ------- 
PROGRESSAO_TRUCO = {
    "normal":  ("truco", 1, 2),
    "truco":   ("retruco", 3, 2),
    "retruco": ("vale4", 4, 3),
}

@dataclass
class EstadoPartida: # OBS: Mantendo o placar e os estados de aposta da partida em andamento.

    modo_jogo: str = "2x2"

    time1: list = field(default_factory=list) # TIMES
    time2: list = field(default_factory=list)

    pontos_time1: int = 0  # PLACAR (ATÉ 24 pts.)
    pontos_time2: int = 0

    _historico_placar: list = field(default_factory=list)  # HISTÓRICO PARA EXCLUIR

    estado_truco: str = "normal"
    quem_pediu_truco: Optional[str] = None
    aguardando_resposta_truco: bool = False
    time_mao: str = "time1"   # OBS: Pensando.... tive q fazer por causa do envido! Reconhece quem é o mão.
    numero_mao: int = 1
    partida_encerrada: bool = False
    vencedor_partida: Optional[str] = None
    partida_id: Optional[int] = None

# ------- Placar -------
    def pontos_faltando(self, time: str) -> int: # OBS: Para saber qnts pontos faltam para o time vencer.
        pts = self.pontos_time1 if time == "time1" else self.pontos_time2
        return max(0, PONTOS_PARTIDA - pts)
    
    def adicionar_pontos(self, time: str, pontos: int): # OBS: Fazendo com que add pontos ao time, salva e verifica se acabou a rodada.
        self._historico_placar.append((self.pontos_time1, self.pontos_time2))
       
        if time == ("time1"):
            self.pontos_time1 = min(PONTOS_PARTIDA, self.pontos_time1 + pontos)
        elif time == ("time2"):
            self.pontos_time2 = min(PONTOS_PARTIDA, self.pontos_time2 + pontos)

        if self.pontos_time1 >= PONTOS_PARTIDA:
            self.partida_encerrada = True
            self.vencedor_partida = "time1"
        elif self.pontos_time2 >= PONTOS_PARTIDA:
            self.partida_encerrada = True
            self.vencedor_partida = "time2"
    
    def desfazer_ultimo_ponto(self) -> bool:  # OBS: Desfaz a último ponto agregado.
        if not self._historico_placar:
            return False
        self.pontos_time1, self.pontos_time2 = self._historico_placar.pop()
        self.partida_encerrada = False
        self.vencedor_partida = None
        return True
    
# ------- Aqui é peleia, TRUCO / RETRUCO / VALE 4 -------
    def pode_pedir_truco(self, time_solicitante: str) -> bool: # OBS: Check, time pode ou nao chamar truco, ou aumentar.
        if self.aguardando_resposta_truco:
            return False
        if self.quem_pediu_truco == time_solicitante:
            return False
        if self.estado_truco == "vale4":
            return False
        return True
    
    def pedir_truco(self, time_solicitante: str) -> tuple: # OBS: Registra o pedido de truco.
        novo_estado, pts_aceito, pts_recusado = PROGRESSAO_TRUCO[self.estado_truco]
        self.estado_truco = novo_estado
        self.quem_pediu_truco = time_solicitante
        self.aguardando_resposta_truco = True
        return novo_estado, pts_aceito, pts_recusado
    
    def aceitar_truco(self) -> int: # OBS: Time adv aceitando o truco, essa parte ta na responsa.
        self.aguardando_resposta_truco = False
        valores = {"truco": 2, "retruco": 3, "vale4": 4}
        return valores.get(self.estado_truco, 1)
    
    def recusar_truco(self) -> tuple: # OBS: Sem comentários... Nem precisa.
        pontos_ao_recusar = {
            "truco": 1,
            "retruco": 2,
            "vale4": 3,
        }
        time_que_leva = self.quem_pediu_truco
        pontos = pontos_ao_recusar.get(self.estado_truco, 1)
        self.adicionar_pontos(time_que_leva, pontos)   # OBS: Add pontos automático.
        self.resetar_mao()
        return time_que_leva, pontos
    
    def valor_atual_truco(self) -> int:
        valores = {
            "normal": 1, 
            "truco": 2, 
            "retruco": 3, 
            "vale4": 4
        }
        
        return valores.get(self.estado_truco, 1)
    
# ------- Envido -------
# OBS IMPORTANTE, SÉRIO MSM!! Aqui o UX informa quem ganhou, o app calcula o valor.
    def valor_falta_envido(self, time_vencedor: str) -> int:
        return self.pontos_faltando(time_vencedor)
    
    def valor_flor_ao_resto(self) -> int:
        time_na_frente = "time1" if self.pontos_time1 >= self.pontos_time2 else "time2"
        return self.pontos_faltando(time_na_frente)
    
    def resetar_mao(self):
        self.estado_truco = "normal"
        self.quem_pediu_truco = None
        self.aguardando_resposta_truco = False
        self.time_mao = "time2" if self.time_mao == "time1" else "time1"
        self.numero_mao += 1

    def resumo(self) -> dict:   # OBS: Essa parte aqui pia, é pra exibição na tela.
        return {
            "mao":            self.numero_mao,
            "pontos_time1":   self.pontos_time1,
            "pontos_time2":   self.pontos_time2,
            "falta_time1":    self.pontos_faltando("time1"),
            "falta_time2":    self.pontos_faltando("time2"),
            "estado_truco":   self.estado_truco,
            "valor_mao":      self.valor_atual_truco(),
            "aguard_truco":   self.aguardando_resposta_truco,
            "quem_pediu":     self.quem_pediu_truco,
            "time_mao":       self.time_mao,
            "encerrada":      self.partida_encerrada,
            "vencedor":       self.vencedor_partida,
            "pode_undo":      len(self._historico_placar) > 0,
        }
    
# ------- Opção de TESTE -------
if __name__ == "__main__":
    jogadores = ["Jão", "Macuna", "Babili", "Faisca"]
    t1, t2 = sortear_duplas(jogadores)
    print(f"Time 1: {t1}")
    print(f"Time 2: {t2}")

    p = EstadoPartida(time1=t1, time2=t2)
    p.pontos_time1 = 10
    p.pontos_time2 = 8

    print("\n =>> TESTE TRUCO e RECUSA <<=")
    print(f"Pode pedir truco (time1)? {p.pode_pedir_truco('time1')}")
    estado,aceito, recusado = p.pedir_truco("time1")
    print(f"Time1 pediu truco → estado: {estado}, aceito={aceito}pts, recusado{recusado}pts")
    time_ganha, pts = p.recusar_truco()
    print(f"Time2 recusou → {time_ganha} leva {pts}, | PLACAR: {p.pontos_time1}x{p.pontos_time2}")

    print("\n =>> Teste Retruco e Não aceito <<=")
    p.pontos_time1 = 10
    p.pontos_time2 = 8
    p.resetar_mao()
    p.pedir_truco("time1")
    p.aceitar_truco()
    estado, aceito, recusado = p.pedir_truco("time2")  # retruco
    print(f"Time2 pediu retruco → aceito={aceito}pts, recusado={recusado}pts")
    time_ganha, pts = p.recusar_truco()
    print(f"Time1 recusou retruco → {time_ganha} leva {pts}pts | PLACAR: {p.pontos_time1}x{p.pontos_time2}")

    print("\n =>> Teste Undo <<=")
    print(f"Placar antes undo: {p.pontos_time1}x{p.pontos_time2}")
    p.desfazer_ultimo_ponto()
    print(f"Placar após undo: {p.pontos_time1}x{p.pontos_time2}")

    print("\n =>> Teste Falta envido / Flor ao resto <<=")
    p.pontos_time1 = 18
    p.pontos_time2 = 14
    print(f"Falta envido se time1 ganhar: {p.valor_falta_envido('time1')}pts")
    print(f"Flor ao resto (time1 na frente): {p.valor_flor_ao_resto()}pts")

    print("\n =>> Resumo <<=")
    for k, v in p.resumo().items():
        print(f"   {k}:   {v}")