# Gêmeo Digital de Paletização Robotizada (UR10)

Um projeto de integração e simulação de paletização industrial utilizando um braço Universal Robots UR10. O sistema opera como um Gêmeo Digital, sincronizando o controlador nativo (URSim) com uma simulação gráfica 3D (RoboDK) em tempo real, sob a coordenação de um CLP virtual (CODESYS) via protocolo Modbus TCP.

## 🛠️ Tecnologias Utilizadas

* **Universal Robots (URSim):** Controlador atuando como Mestre Modbus e executando a lógica de movimentação nativa e cinemática em URScript.
* **RoboDK:** Ambiente de simulação 3D, espelhando os movimentos do robô através de um script Python rodando em *background*.
* **CODESYS:** CLP virtual gerenciando a lógica de controle do processo (Slave Modbus), gerando gatilhos de esteira e seleção de receitas.
* **Python (Sockets TCP/IP):** Script de monitoramento contínuo operando na porta `30003` (Secondary Client Interface) para sincronizar as juntas do robô em milissegundos.

## ⚙️ Funcionalidades e Soluções

* **Sincronismo em Tempo Real:** O modelo 3D no RoboDK espelha exata e instantaneamente a cinemática calculada pelo URSim ignorando delays gráficos.
* **Comunicação Modbus TCP:** O URSim intertrava os status de I/O industriais (sensores da esteira, acionamento do vácuo da garra VG10) diretamente com o CODESYS.
* **Troca de Receitas Dinâmica:** O usuário pode alternar a lógica de produção entre paletizar "1 Camada" ou "2 Camadas" a partir de uma variável no CLP, mudando a rotina do robô no meio do processo.
* **Tratamento de Arquitetura de Rede:** Mapeamento cruzado e mitigação do fenômeno de *Byte Swap* (inversão de bytes Big-Endian vs Little-Endian) entre o padrão do robô e a memória do CLP.

## 🚀 Como Rodar o Projeto

Para testar o sistema localmente, siga esta ordem exata de inicialização:

1. **Inicie o CODESYS (CLP):**
   * Carregue o projeto lógico.
   * Coloque o CLP em modo `Run` para ativar o Servidor Modbus (Slave) na rede local.
2. **Inicie o URSim (Controlador do Robô):**
   * Carregue o arquivo `.script` da paletização.
   * Na aba `Installation` > `Modbus`, verifique se o sinal está verde, confirmando a conexão com o IP do CODESYS.
   * Dê o "Play" no painel. O robô irá iniciar e aguardar o sinal do sensor de presença da esteira.
3. **Inicie o RoboDK (Gêmeo Digital):**
   * Abra a estação da célula (robô, palete e esteira).
   * Rode o script Python de monitoramento (ex: `Monitor_URSim.py`). O robô 3D irá se mover para a posição exata atual do URSim.
4. **Operação:**
   * Vá até o ambiente do CODESYS e force o estado da entrada digital "Sensor da Esteira" para `TRUE`.
   * Acompanhe a operação: O URSim calculará a trajetória, os sinais Modbus sincronizarão a garra, e o RoboDK fará a animação completa de *Pick and Place*!

## 🎥 Demonstração em Vídeo

Assista ao vídeo abaixo para uma explicação detalhada da arquitetura, incluindo a estrutura do código, mapeamento das portas Modbus e o sistema completo operando as receitas em tempo real:

[![Demonstração RoboDK | Codesys | URSIM - UR10](https://i.ytimg.com/vi/TiKgjd4ohG4/maxresdefault.jpg)](https://www.youtube.com/watch?v=TiKgjd4ohG4)
