import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  
import os

def clear():
    """Limpia la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    """Reemplazo universal de msvcrt que funciona en Windows, Linux y Mac."""
    input("\nPresione Enter para volver al menú principal...")

# 1. Carga y Configuración Inicial de Datos
try:
    df = pd.read_excel('Datos Jugadores FIFA.xlsx', sheet_name='Datos')
except FileNotFoundError:
    print("Error: No se encontró el archivo 'Datos Jugadores FIFA.xlsx'")
    exit()

pd.options.display.float_format = '{:,.0f}'.format

# 2. Renombrado de Columnas (Formato Internacional)
df.rename(columns={
    'Nombre': 'Name', 'Nacionalidad': 'Nationality', 'Posición': 'Position',
    'Descripción Posición': 'Description_Posicion', 'Número Camiseta': 'Numero_camiseta',
    'Club': 'Club', 'Rating General': 'Overall_Rating', 'Altura (cm)': 'Height_cm',
    'Peso (kg)': 'Weight_kg', 'Pie Hábil': 'Pie_Habil', 'Año Nacimiento': 'Birth_Year',
    'Edad': 'Age', 'Work_Rate': 'Position_Work_Rate', 'Weak_Foot': 'Weak_Foot',
    'Skill_Moves': 'Skill_Moves', 'Ball_Control': 'Ball_Control', 'Dribbling': 'Dribbling',
    'Marking': 'Marking', 'Sliding_Tackle': 'Sliding_Tackle', 'Standing_Tackle': 'Standing_Tackle',
    'Aggression': 'Aggression', 'reactions': 'Reactions', 'Attacking_Position': 'Attacking_Position',
    'Interceptions': 'Interceptions', 'Vision': 'Vision', 'Composure': 'Composure',
    'Crossing': 'Crossing', 'Short_Pass': 'Short_Pass', 'Long_Pass': 'Long_Pass',
    'Acceleration': 'Acceleration', 'Speed': 'Speed', 'Stamina': 'Stamina',
    'Strength': 'Strength', 'Balance': 'Balance', 'Agility': 'Agility',
    'Jumping': 'Jumping', 'Heading': 'Heading', 'Shot_Power': 'Shot_Power',
    'Finishing': 'Finishing', 'Long_Shots': 'Long_Shots', 'Curve': 'Curve',
    'Freekick_Accuracy': 'Freekick_Accuracy', 'Penalties': 'Penalties', 'Volleys': 'Volleys',
    'GK_Positioning': 'GK_Positioning', 'GK_Diving': 'GK_Diving', 'GK_Kicking': 'GK_Kicking',
    'GK_Handling': 'GK_Handling', 'GK_Reflexes': 'GK_Reflexes', 
    'Rendimiento General (RGJ)': 'General_Performance_Rating'
}, inplace=True)

df.dropna(how='all', inplace=True)

# 3. Ingeniería de Variables - Creación de un nuevo atributo 'Player_Archetype' basado en habilidades clave
def categorizar_perfil(row):
    if row['GK_Positioning'] > 50: return 'Goalkeeper'
    elif (row['Speed'] > 75) and (row['Dribbling'] > 75): return 'Agile Winger/Attacker'
    elif (row['Strength'] > 75) and (row['Standing_Tackle'] > 70): return 'Defensive Anchor'
    elif (row['Vision'] > 70) and (row['Short_Pass'] > 70): return 'Playmaker'
    else: return 'Balanced / All-Rounder'

df['Player_Archetype'] = df.apply(categorizar_perfil, axis=1)

# 4. Interfaz interactiva por consola para mostrar resultados y gráficos
while True:
    clear()
    print("==================================================")
    print("     FIFA DATA ANALYSIS SYSTEM - INTERACTIVE MENU ")
    print("==================================================")
    print("1. Ejecutar Resumen Estadístico y Agregaciones")
    print("2. Generar Matriz de Correlación Avanzada (Heatmap)")
    print("3. Salir del Programa")
    print("==================================================")
    
    try:
        opcion = int(input("Selecciona una opción (1-3): "))
    except ValueError:
        print("Entrada inválida. Por favor, introduce un número.")
        pause()
        continue

    if opcion == 1:
        clear()
        print("--- 1. RESUMEN ESTADÍSTICO DE CAPACIDADES FÍSICAS Y TÉCNICAS ---")
        attributes_to_analyze = ['Age', 'Overall_Rating', 'Speed', 'Stamina', 'Strength', 'Composure']
        print(df[attributes_to_analyze].describe())
        print("\n" + "="*50 + "\n")

        print("--- 2. ANÁLISIS DE RENDIMIENTO POR CLUB Y PIE HÁBIL ---")
        club_ball_control = df.groupby(['Club', 'Pie_Habil'])['Ball_Control'].mean().unstack().fillna(0)
        print("Top 10 Clubes con mejor promedio de Ball Control (Dividido por Pie Hábil):")
        print(club_ball_control.sort_values(by='Derecho', ascending=False).head(10))
        print("\n" + "="*50 + "\n")

        print("--- 3. DISTRIBUCIÓN DE ARQUETIPOS DETECTADOS ---")
        print(df['Player_Archetype'].value_counts())
        print("\n" + "="*50 + "\n")

        print("--- 4. CORRELACIÓN CON EL RATING GENERAL ---")
        skills = ['Ball_Control', 'Dribbling', 'Short_Pass', 'Reactions', 'Vision', 'Composure']
        correlations = df[skills].corrwith(df['Overall_Rating']).sort_values(ascending=False)
        print(correlations)
        pause()

    elif opcion == 2:
        clear()
        print("Generando matriz de correlación visual... Cierre la ventana del gráfico para regresar.")
        columns_for_heatmap = ['Overall_Rating', 'Age', 'Speed', 'Stamina', 'Strength', 'Ball_Control', 'Dribbling', 'Short_Pass', 'Vision', 'Composure']
        correlation_matrix = df[columns_for_heatmap].corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, vmin=-1, vmax=1)
        plt.title('FIFA Players Attribute Correlation Matrix', fontsize=14, fontweight='bold', pad=15)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
        pause()

    elif opcion == 3:
        clear()
        print("¡Gracias por utilizar el sistema analítico!, espero te sirva como referencia")
        break
    else:
        print("Opción fuera de rango (Elige entre 1 y 3).")
        pause()
