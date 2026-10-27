# Cruzamento de Retas — reconstrução 2D e 3D

Aplicativo gráfico em Python para visualizar o cruzamento de retas em três projeções e estimar um ponto 3D. A lógica segue a planilha `cruzreta.xlsx`: calcula os cruzamentos XY, XZ e ZY e combina as coordenadas correspondentes pela média.

## Como executar

1. Instale Python 3.10 ou superior.
2. Baixe `cruzamento_de_retas.py` deste repositório.
3. Execute no terminal:

   ```bash
   python cruzamento_de_retas.py
   ```

O aplicativo usa apenas bibliotecas incluídas no Python (Tkinter). Em Linux, instale também o pacote Tkinter da sua distribuição se ele não vier com Python.

## Usar o aplicativo

- Em cada vista (XY, XZ e ZY), informe as coordenadas X/Y da câmera e do pixel para as duas retas.
- Clique em **Calcular reconstrução** para obter os três cruzamentos e a estimativa (X, Y, Z).
- O gráfico mostra as retas, os pontos de câmera/pixel e o cruzamento de cada vista.
- Clique em **Restaurar exemplo** para retornar aos valores da planilha original.

Os valores iniciais são os dados do arquivo de referência. Coordenadas de um ponto real não são necessárias para calcular a reconstrução.
