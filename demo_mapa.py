# Demonstração 5 · Um mapa a partir de uma tabela (Python / Spyder)
# Antes da sessão (uma só vez), no Anaconda Prompt:  pip install folium
# O ficheiro "locais.csv" (colunas nome, tipo, lat, lon) fica ao lado deste script.
# Correr célula a célula com Ctrl+Enter (cada "# %%" é uma célula).

# %% 0. Preparação
from pathlib import Path
import pandas as pd

PASTA = Path(__file__).parent if "__file__" in globals() else Path(".")

# %% 1. Ler a tabela
locais = pd.read_csv(PASTA / "locais.csv")
print(locais)

# %% 2. Mapa interativo com Folium (abre no navegador; precisa de internet para o fundo)
import folium
import webbrowser

cores = {"Universidade": "red", "Monumento": "blue", "Jardim": "green"}

mapa = folium.Map(location=[locais.lat.mean(), locais.lon.mean()], zoom_start=15,
                  tiles="CartoDB Voyager")
for _, l in locais.iterrows():
    folium.Marker(
        [l.lat, l.lon],
        popup=f"<b>{l.nome}</b><br>{l.tipo}",
        tooltip=l.nome,
        icon=folium.Icon(color=cores.get(l.tipo, "gray")),
    ).add_to(mapa)

saida = PASTA / "mapa.html"
mapa.save(saida)
webbrowser.open(saida.resolve().as_uri())

# %% 3. Plano B sem internet: mapa estático com matplotlib (aparece no painel Plots)
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 6))
for tipo, grupo in locais.groupby("tipo"):
    ax.scatter(grupo.lon, grupo.lat, s=80, label=tipo)
for _, l in locais.iterrows():
    ax.annotate(l.nome, (l.lon, l.lat), xytext=(5, 5), textcoords="offset points", fontsize=8)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Locais (coordenadas aproximadas)")
ax.legend()
ax.set_aspect(1 / 0.766)   # corrige a deformação à latitude de Coimbra (cos 40°)
plt.tight_layout()
plt.show()
