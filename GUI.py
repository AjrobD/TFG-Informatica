import tkinter as tk
from tkinter import ttk
from tkinter import Text
from tkinter import Checkbutton
from tkinter import Label
from tkinter import StringVar
import pandas as pd



def show_selection():
  # Obtener la opción seleccionada.
  categories = []
  for var in all_var:
    if var.get():
      categories.append(var.get())
  
  
  switch_position = {
    'Defensa': 'DF',
    'Mediocentro': 'MF',
    'Delantero': 'FW'
  }
  
  pareto = pareto_position_country_season(df, switch_position.get(combo_pos.get()), combo_country.get(), combo_season.get(), categories)
  if pareto != "None":
    pareto_names = ', '.join(list(map(lambda x : x[0][3], pareto)))
  else:
    pareto_names = pareto
  text_box.config(state='normal')
  text_box.delete('1.0', 'end')
  #text_box.insert('end',pareto)
  text_box.insert('end',pareto_names)
  text_box.config(state='disabled')

def pareto_position_country_season(df,position,country,season,categories):
  data = df.loc[df['nacionalidad'] == country].loc[df[position] == 1].loc[df['temporada'] == season]
  if data.empty:
    return "None"
  
  ids = ['jugador_id','id_campeonato','temporada','nombre']
  ids_points = data[ids].to_numpy().tolist()
    
  points = data[categories].to_numpy().tolist()
  input_points = list(zip(ids_points,points))
  pareto, dominated = simple_cull(input_points)
  
  return pareto

def dominates(row, candidateRow):
    return sum([row[x] >= candidateRow[x] for x in range(len(row))]) == len(row) 
  
  
def simple_cull(inputPoints):
    paretoPoints = set()
    candidateRowNr = 0
    dominatedPoints = set()
    while True:
        candidateRow = inputPoints[candidateRowNr]
        inputPoints.remove(candidateRow)
        rowNr = 0
        nonDominated = True
        while len(inputPoints) != 0 and rowNr < len(inputPoints):
            row = inputPoints[rowNr]
            if dominates(candidateRow[1], row[1]):
                # If it is worse on all features remove the row from the array
                inputPoints.remove(row)
                dominatedPoints.add(tuple(tuple(i) for i in row))
            elif dominates(row[1], candidateRow[1]):
                nonDominated = False
                dominatedPoints.add(tuple(tuple(i) for i in candidateRow))
                rowNr += 1
            else:
                rowNr += 1

        if nonDominated:
            # add the non-dominated point to the Pareto frontier
            paretoPoints.add(tuple(tuple(i) for i in candidateRow))

        if len(inputPoints) == 0:
            break
    return paretoPoints, dominatedPoints



df = pd.read_json('players_categories.json')

ventana = tk.Tk()
ventana.title("Configurador de selecciones")
ventana.config(width=1000, height=600)

Label(ventana,text="Posición:").place(x=50,y=25)
combo_pos = ttk.Combobox()
combo_pos = ttk.Combobox(
  state="readonly",
  values=["Defensa", "Mediocentro", "Delantero"]
)
combo_pos.place(x=50, y=50)
combo_pos.current(0)

Label(ventana,text="País:").place(x=300,y=25)
combo_country = ttk.Combobox()
combo_country = ttk.Combobox(
  state="readonly",
  values =  list(dict.fromkeys(df['nacionalidad']))
)
combo_country.place(x=300, y=50)
combo_country.current(0)

Label(ventana,text="Temporada:").place(x=550,y=25)
combo_season = ttk.Combobox()
combo_season = ttk.Combobox(
  state="readonly",
  values = list(dict.fromkeys(df['temporada']))
)
combo_season.place(x=550, y=50)
combo_season.current(0)

text_box = Text(
    ventana,
    height=12,
    width=80
)

label_ataque = Label(ventana,text="Fase Ofensiva:").place(x=50,y=90)
var_tiro = StringVar()
tiro_cb = Checkbutton(ventana,text='Tiro',variable=var_tiro,onvalue='tiro',offvalue='').place(x=150,y=90)
var_pases = StringVar()
pases_cb = Checkbutton(ventana,text='Pases',variable=var_pases,onvalue='pases',offvalue='').place(x=220,y=90)
var_conduccion_regate = StringVar()
conduccion_regate_cb = Checkbutton(ventana,text='Conducción y regate',variable=var_conduccion_regate,onvalue='conduccion_regate',offvalue='').place(x=300,y=90)
var_posesion_balon = StringVar()
posesion_balon_cb = Checkbutton(ventana,text='Posesión de balón',variable=var_posesion_balon,onvalue='posesion_balon',offvalue='').place(x=450,y=90)
var_otro_ataque = StringVar()
otro_ataque_cb = Checkbutton(ventana,text='Otros ataque',variable=var_otro_ataque,onvalue='otro_ataque',offvalue='').place(x=650,y=90)


label_ataque = Label(ventana,text="Fase Defensiva:").place(x=50,y=140)
var_entradas = StringVar()
entradas_cb = Checkbutton(ventana,text='Entradas',variable=var_entradas,onvalue='entradas',offvalue='').place(x=150,y=140)
var_presion = StringVar()
presion_cb = Checkbutton(ventana,text='Presión',variable=var_presion,onvalue='presion',offvalue='').place(x=220,y=140)
var_tarjetas_faltas = StringVar()
tarjetas_faltas_cb = Checkbutton(ventana,text='Tarjetas y faltas',variable=var_tarjetas_faltas,onvalue='tarjetas_faltas',offvalue='').place(x=300,y=140)
var_bloqueos_intercepciones = StringVar()
bloqueos_intercepciones_cb = Checkbutton(ventana,text='Bloqueos e interceptaciones',variable=var_bloqueos_intercepciones,onvalue='bloqueos_intercepciones',offvalue='').place(x=450,y=140)
var_recuperaciones = StringVar()
recuperaciones_cb = Checkbutton(ventana,text='Recuperaciones',variable=var_recuperaciones,onvalue='recuperaciones',offvalue='').place(x=650,y=140)
var_otro_defensa = StringVar()
otro_defensa_cb = Checkbutton(ventana,text='Otros Defensa',variable=var_otro_defensa,onvalue='otro_defensa',offvalue='').place(x=800,y=140)

label_ataque = Label(ventana,text="Otros:").place(x=50,y=190)
var_aereo = StringVar()
aereo = Checkbutton(ventana,text='Aéreo',variable=var_aereo,onvalue='aereo',offvalue='').place(x=150,y=190)


all_var = [var_tiro,var_pases,var_conduccion_regate,var_posesion_balon,var_otro_ataque,var_entradas,var_presion,var_tarjetas_faltas,var_bloqueos_intercepciones,var_recuperaciones,var_otro_defensa,var_aereo]

text_box.config(state='disabled')
text_box.place(x=50,y=300)

boton_pareto = ttk.Button(text="Mostrar frontera de pareto", command=show_selection)
boton_pareto.place(x=50, y=250)


ventana.mainloop()