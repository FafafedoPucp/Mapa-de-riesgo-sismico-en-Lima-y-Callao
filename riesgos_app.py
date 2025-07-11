# ==============================================================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# ==============================================================================
# Se importan las librerías necesarias para el funcionamiento de la aplicación.

import streamlit as st               # Para crear y correr la aplicación web interactiva.
import geopandas as gpd              # Para leer y manipular datos geográficos (el archivo GeoJSON).
import plotly.express as px          # Para crear los gráficos y mapas interactivos de alta calidad.
import pandas as pd                  # Para la manipulación y análisis de datos en estructuras llamadas DataFrames.

# ==============================================================================
# 2. CONFIGURACIÓN DE LA PÁGINA
# ==============================================================================
# st.set_page_config() se usa para configurar atributos de la página como el título y el layout.
# Debe ser el primer comando de Streamlit en el script.
# layout="wide" hace que la aplicación ocupe todo el ancho de la pantalla para una mejor visualización del mapa.
st.set_page_config(layout="wide", page_title="Análisis de Riesgo Sísmico en Lima y Callao")

# --- Títulos y Descripción Principal ---
# st.title() y st.markdown() se usan para mostrar texto en la aplicación con diferente formato.
st.title("Análisis de Riesgo Sísmico en Lima Metropolitana y Callao 🗺️")
st.markdown("Visualización interactiva de diferentes variables de riesgo por distrito.")

# ==============================================================================
# 3. DICCIONARIOS DE DATOS
# ==============================================================================
# Aquí se almacenan todos los datos brutos en diccionarios de Python.
# Cada diccionario representa una variable diferente.
# Las claves (nombres de los distritos) están en mayúsculas y sin tildes para estandarizar y facilitar la unión de datos.
# Todos los diccionarios fueron filtrados con anterioridad para centrarse en Lima Metropolitana y Callao. Además nos hemos centrado desde los 2000 hasta la actualidad. Y con la información del último censo de INEI del 2017.

poblacion = {
    'ANCON': 43400, 'ATE': 594529, 'BARRANCO': 36721, 'BRENA': 80912, 'CARABAYLLO': 360718, 'CHACLACAYO': 46225, 'CHORRILLOS': 342505, 'CIENEGUILLA': 34090, 'COMAS': 510828, 'EL AGUSTINO': 193319, 'INDEPENDENCIA': 227136, 'JESUS MARIA': 75359, 'LA MOLINA': 140679, 'LA VICTORIA': 192721, 'LIMA': 241783, 'LINCE': 58077, 'LOS OLIVOS': 326604, 'LURIGANCHO': 232730, 'LURIN': 83620, 'MAGDALENA DEL MAR': 60296, 'MIRAFLORES': 85065, 'PACHACAMAC': 90007, 'PUCUSANA': 13619, 'PUEBLO LIBRE': 82355, 'PUENTE PIEDRA': 234341, 'PUNTA HERMOSA': 15684, 'PUNTA NEGRA': 7702, 'RIMAC': 174789, 'SAN BARTOLO': 7746, 'SAN BORJA': 118490, 'SAN ISIDRO': 68966, 'SAN JUAN DE LURIGANCHO': 1038495, 'SAN JUAN DE MIRAFLORES': 404000, 'SAN LUIS': 58001, 'SAN MARTIN DE PORRES': 699492, 'SAN MIGUEL': 150367, 'SANTA ANITA': 205816, 'SANTA MARIA DEL MAR': 1294, 'SANTA ROSA': 15113, 'SANTIAGO DE SURCO': 354270, 'SURQUILLO': 92100, 'VILLA EL SALVADOR': 378472, 'VILLA MARIA DEL TRIUNFO': 398423,
    'CALLAO': 477743, 'BELLAVISTA': 78936, 'CARMEN DE LA LEGUA REYNOSO': 48331, 'LA PERLA': 61698, 'LA PUNTA': 4014, 'VENTANILLA': 424467, 'MI PERU': 51522
}
area = {
    'ANCON': 299, 'ATE': 78, 'BARRANCO': 3, 'BRENA': 3, 'CARABAYLLO': 347, 'CHACLACAYO': 39, 'CHORRILLOS': 38, 'CIENEGUILLA': 241, 'COMAS': 48, 'EL AGUSTINO': 13, 'INDEPENDENCIA': 15, 'JESUS MARIA': 5, 'LA MOLINA': 66, 'LA VICTORIA': 9, 'LIMA': 22, 'LINCE': 3, 'LOS OLIVOS': 19, 'LURIGANCHO': 236, 'LURIN': 181, 'MAGDALENA DEL MAR': 4, 'MIRAFLORES': 10, 'PACHACAMAC': 160, 'PUEBLO LIBRE': 5, 'PUCUSANA': 38, 'PUENTE PIEDRA': 71, 'PUNTA HERMOSA': 13, 'PUNTA NEGRA': 13, 'RIMAC': 12, 'SAN BARTOLO': 45, 'SAN BORJA': 10, 'SAN ISIDRO': 12, 'SAN JUAN DE LURIGANCHO': 131, 'SAN JUAN DE MIRAFLORES': 26, 'SAN LUIS': 4, 'SAN MARTIN DE PORRES': 41, 'SAN MIGUEL': 10, 'SANTA ANITA': 11, 'SANTA MARIA DEL MAR': 1, 'SANTA ROSA': 21, 'SANTIAGO DE SURCO': 35, 'SURQUILLO': 3, 'VILLA EL SALVADOR': 36, 'VILLA MARIA DEL TRIUNFO': 71,
    'CALLAO': 47, 'BELLAVISTA': 5, 'CARMEN DE LA LEGUA REYNOSO': 2, 'LA PERLA': 3, 'LA PUNTA': 0.75, 'VENTANILLA': 74, 'MI PERU': 3
}
suelos = {
    'ANCON': 'Mixto: Roca (S1) en cerros y Suelo Arenoso (S3) en pampas',
    'ATE': 'Mixto: Conglomerado (S2) en el oeste, transita a Roca (S1) al este',
    'BARRANCO': 'Suelo Rígido (Conglomerado S2)',
    'BRENA': 'Suelo Rígido (Conglomerado S2)',
    'CARABAYLLO': 'Mixto: Roca (S1) en laderas y Suelo Aluvial/Arenoso (S2-S3) en zonas bajas',
    'CHACLACAYO': 'Suelo Muy Rígido (Roca S1 y grava densa)',
    'CHORRILLOS': 'Mixto: Roca (S1 Morro Solar), Suelo Blando (S4 Pantanos), Conglomerado (S2 zona alta)',
    'CIENEGUILLA': 'Suelo Muy Rígido (Roca S1 y grava densa)',
    'COMAS': 'Mixto: Roca (S1) en laderas y Conglomerado (S2) en zonas planas',
    'EL AGUSTINO': 'Mixto: Roca (S1) en laderas y suelos de menor calidad en zonas bajas',
    'INDEPENDENCIA': 'Mixto: Roca (S1) en cerros y Conglomerado (S2) en la base',
    'JESUS MARIA': 'Suelo Rígido (Conglomerado S2)',
    'LA MOLINA': 'Suelo Muy Rígido (Roca S1 en cerros y suelo firme S1-S2 en valle)',
    'LA VICTORIA': 'Suelo Rígido (Conglomerado S2)',
    'LIMA': 'Suelo Rígido (Conglomerado S2), posibles rellenos en zona histórica',
    'LINCE': 'Suelo Rígido (Conglomerado S2)',
    'LOS OLIVOS': 'Suelo Rígido (Conglomerado S2 y suelo aluvial denso)',
    'LURIGANCHO': 'Suelo Muy Rígido (Roca S1 y conglomerados densos)',
    'LURIN': 'Mixto: Suelo Arenoso (S3) y suelo aluvial en el valle',
    'MAGDALENA DEL MAR': 'Suelo Rígido (Conglomerado S2)',
    'MIRAFLORES': 'Suelo Rígido (Conglomerado S2)',
    'PACHACAMAC': 'Mixto: Suelo aluvial en valle, zonas rocosas (S1) y arenosas (S3)',
    'PUEBLO LIBRE': 'Suelo Rígido (Conglomerado S2)',
    'PUCUSANA': 'Mixto: Roca (S1) en laderas y Suelo Arenoso (S3) en zonas bajas',
    'PUENTE PIEDRA': 'Predominantemente Suelo Arenoso y gravoso (S3)',
    'PUNTA HERMOSA': 'Mixto: Roca (S1) en laderas y Suelo Arenoso (S3)',
    'PUNTA NEGRA': 'Mixto: Roca (S1) en laderas y Suelo Arenoso (S3)',
    'RIMAC': 'Mixto: Roca (S1 Cerro San Cristóbal) y suelo aluvial (S2-S3) cerca al río',
    'SAN BARTOLO': 'Mixto: Roca (S1) en laderas y Suelo Arenoso (S3)',
    'SAN BORJA': 'Suelo Rígido (Conglomerado S2)',
    'SAN ISIDRO': 'Suelo Rígido (Conglomerado S2)',
    'SAN JUAN DE LURIGANCHO': 'Mixto: Roca (S1) en cerros y Conglomerado (S2) en zonas planas',
    'SAN JUAN DE MIRAFLORES': 'Mixto: Suelo Arenoso (S3) en zonas bajas y Roca (S1) en laderas',
    'SAN LUIS': 'Suelo Rígido (Conglomerado S2)',
    'SAN MARTIN DE PORRES': 'Suelo Rígido (Conglomerado S2 y suelo aluvial denso)',
    'SAN MIGUEL': 'Suelo Rígido (Conglomerado S2), con zonas arenosas hacia la costa',
    'SANTA ANITA': 'Suelo Rígido (Conglomerado S2)',
    'SANTA MARIA DEL MAR': 'Mixto: Roca (S1) en laderas y Suelo Arenoso (S3)',
    'SANTA ROSA': 'Predominantemente Suelo Arenoso (S3)',
    'SANTIAGO DE SURCO': 'Predominantemente Suelo Rígido (Conglomerado S2), con zonas de Roca (S1) al este',
    'SURQUILLO': 'Suelo Rígido (Conglomerado S2)',
    'VILLA EL SALVADOR': 'Predominantemente Suelo Arenoso de densidad media a suelta (S3/S4)',
    'VILLA MARIA DEL TRIUNFO': 'Mixto: Suelo Arenoso (S3) en zonas bajas y Roca (S1) en laderas',
    'CALLAO': 'Suelo Blando (S4) y rellenos artificiales',
    'BELLAVISTA': 'Suelo Blando (S4) y rellenos artificiales',
    'CARMEN DE LA LEGUA REYNOSO': 'Suelo Blando (S4) y rellenos artificiales',
    'LA PERLA': 'Suelo Blando (S4) y rellenos artificiales',
    'LA PUNTA': 'Suelo Arenoso y de grava (S3)',
    'VENTANILLA': 'Predominantemente Suelo Arenoso (S3)',
    'MI PERU': 'Predominantemente Suelo Arenoso (S3)'
}
# Se pidió a la IA determinar de una escala de 0 a 10 que tan riesgosa es el suelo predominante del distrito. Además se pidió agregar información de los distritos de CALLAO a la IA
peligrosidad_suelos = {
    'ANCON': 7, 'ATE': 3, 'BARRANCO': 3, 'BRENA': 3, 'CARABAYLLO': 7, 'CHACLACAYO': 2, 'CHORRILLOS': 9, 'CIENEGUILLA': 2, 'COMAS': 6, 'EL AGUSTINO': 6, 'INDEPENDENCIA': 6, 'JESUS MARIA': 3, 'LA MOLINA': 2, 'LA VICTORIA': 3, 'LIMA': 5, 'LINCE': 3, 'LOS OLIVOS': 4, 'LURIGANCHO': 2, 'LURIN': 7, 'MAGDALENA DEL MAR': 3, 'MIRAFLORES': 3, 'PACHACAMAC': 7, 'PUEBLO LIBRE': 3, 'PUCUSANA': 7, 'PUENTE PIEDRA': 8, 'PUNTA HERMOSA': 7, 'PUNTA NEGRA': 7, 'RIMAC': 7, 'SAN BARTOLO': 7, 'SAN BORJA': 3, 'SAN ISIDRO': 3, 'SAN JUAN DE LURIGANCHO': 6, 'SAN JUAN DE MIRAFLORES': 8, 'SAN LUIS': 3, 'SAN MARTIN DE PORRES': 4, 'SAN MIGUEL': 5, 'SANTA ANITA': 3, 'SANTA MARIA DEL MAR': 7, 'SANTA ROSA': 8, 'SANTIAGO DE SURCO': 4, 'SURQUILLO': 3, 'VILLA EL SALVADOR': 10, 'VILLA MARIA DEL TRIUNFO': 8,
    'CALLAO': 9, 'BELLAVISTA': 8, 'CARMEN DE LA LEGUA REYNOSO': 9, 'LA PERLA': 8, 'LA PUNTA': 7, 'VENTANILLA': 9, 'MI PERU': 8
}
material_precario = {
    'ANCON': 429, 'ATE': 4276, 'BARRANCO': 117, 'BRENA': 584, 'CARABAYLLO': 2118, 'CHACLACAYO': 84, 'CHORRILLOS': 2175, 'CIENEGUILLA': 475, 'COMAS': 2618, 'EL AGUSTINO': 564, 'INDEPENDENCIA': 1954, 'JESUS MARIA': 138, 'LA MOLINA': 101, 'LA VICTORIA': 869, 'LIMA': 3930, 'LINCE': 183, 'LOS OLIVOS': 389, 'LURIGANCHO': 1890, 'LURIN': 1212, 'MAGDALENA DEL MAR': 114, 'MIRAFLORES': 99, 'PACHACAMAC': 1254, 'PUEBLO LIBRE': 99, 'PUCUSANA': 1022, 'PUENTE PIEDRA': 2703, 'PUNTA HERMOSA': 982, 'PUNTA NEGRA': 76, 'RIMAC': 2442, 'SAN BARTOLO': 66, 'SAN BORJA': 27, 'SAN ISIDRO': 11, 'SAN JUAN DE LURIGANCHO': 11906, 'SAN JUAN DE MIRAFLORES': 3590, 'SAN LUIS': 78, 'SAN MARTIN DE PORRES': 1297, 'SAN MIGUEL': 145, 'SANTA ANITA': 406, 'SANTA MARIA DEL MAR': 9, 'SANTA ROSA': 188, 'SANTIAGO DE SURCO': 461, 'SURQUILLO': 176, 'VILLA EL SALVADOR': 3166, 'VILLA MARIA DEL TRIUNFO': 9506,
    'CALLAO': 8500, 'BELLAVISTA': 1500, 'CARMEN DE LA LEGUA REYNOSO': 1200, 'LA PERLA': 900, 'LA PUNTA': 50, 'VENTANILLA': 15000, 'MI PERU': 2500
}
damnificados_2000 = {
    'ANCON': 0, 'ATE': 117, 'BARRANCO': 8, 'BRENA': 0, 'CARABAYLLO': 4, 'CHACLACAYO': 0, 'CHORRILLOS': 0, 'CIENEGUILLA': 0, 'COMAS': 30, 'EL AGUSTINO': 68, 'INDEPENDENCIA': 10, 'JESUS MARIA': 0, 'LA MOLINA': 0, 'LA VICTORIA': 8, 'LIMA': 56, 'LINCE': 0, 'LOS OLIVOS': 0, 'LURIGANCHO': 0, 'LURIN': 0, 'MAGDALENA DEL MAR': 0, 'MIRAFLORES': 0, 'PACHACAMAC': 0, 'PUEBLO LIBRE': 0, 'PUCUSANA': 0, 'PUENTE PIEDRA': 5, 'PUNTA HERMOSA': 55, 'PUNTA NEGRA': 0, 'RIMAC': 4, 'SAN BARTOLO': 0, 'SAN BORJA': 0, 'SAN ISIDRO': 0, 'SAN JUAN DE LURIGANCHO': 4, 'SAN JUAN DE MIRAFLORES': 88, 'SAN LUIS': 0, 'SAN MARTIN DE PORRES': 0, 'SAN MIGUEL': 0, 'SANTA ANITA': 0, 'SANTA MARIA DEL MAR': 0, 'SANTA ROSA': 0, 'SANTIAGO DE SURCO': 0, 'SURQUILLO': 0, 'VILLA EL SALVADOR': 94, 'VILLA MARIA DEL TRIUNFO': 0,
    'CALLAO': 0, 'BELLAVISTA': 0, 'CARMEN DE LA LEGUA REYNOSO': 0, 'LA PERLA': 0, 'LA PUNTA': 0, 'VENTANILLA': 0, 'MI PERU': 0
}
viviendas_destruidas_2000 = {
    'ANCON': 0, 'ATE': 27, 'BARRANCO': 1, 'BRENA': 0, 'CARABAYLLO': 1, 'CHACLACAYO': 0, 'CHORRILLOS': 0, 'CIENEGUILLA': 0, 'COMAS': 4, 'EL AGUSTINO': 9, 'INDEPENDENCIA': 1, 'JESUS MARIA': 0, 'LA MOLINA': 0, 'LA VICTORIA': 1, 'LIMA': 9, 'LINCE': 0, 'LOS OLIVOS': 0, 'LURIGANCHO': 0, 'LURIN': 0, 'MAGDALENA DEL MAR': 0, 'MIRAFLORES': 0, 'PACHACAMAC': 0, 'PUEBLO LIBRE': 0, 'PUCUSANA': 0, 'PUENTE PIEDRA': 1, 'PUNTA HERMOSA': 18, 'PUNTA NEGRA': 0, 'RIMAC': 1, 'SAN BARTOLO': 0, 'SAN BORJA': 0, 'SAN ISIDRO': 0, 'SAN JUAN DE LURIGANCHO': 1, 'SAN JUAN DE MIRAFLORES': 22, 'SAN LUIS': 0, 'SAN MARTIN DE PORRES': 0, 'SAN MIGUEL': 0, 'SANTA ANITA': 0, 'SANTA MARIA DEL MAR': 0, 'SANTA ROSA': 0, 'SANTIAGO DE SURCO': 0, 'SURQUILLO': 0, 'VILLA EL SALVADOR': 52, 'VILLA MARIA DEL TRIUNFO': 0,
    'CALLAO': 0, 'BELLAVISTA': 0, 'CARMEN DE LA LEGUA REYNOSO': 0, 'LA PERLA': 0, 'LA PUNTA': 0, 'VENTANILLA': 0, 'MI PERU': 0
}

# ==============================================================================
# 4. FUNCIÓN DE PROCESAMIENTO DE DATOS
# ==============================================================================

# El decorador @st.cache_data le dice a Streamlit que "memorice" el resultado de esta función.
# La función solo se volverá a ejecutar si los datos de entrada (los diccionarios) cambian.
# Esto hace que la aplicación sea mucho más rápida, ya que no tiene que recargar y procesar los archivos cada vez.
@st.cache_data
def load_and_process_data(poblacion_data, area_data, peligrosidad_data, material_data, damnificados_data, viviendas_data):
    # Calcula la densidad poblacional (Población / Área) para cada distrito.
    densidad_poblacional = {distrito: round(poblacion_data[distrito] / area_data[distrito]) for distrito in poblacion_data if distrito in area_data and area_data[distrito] > 0}
    
    # Carga el archivo GeoJSON que contiene las formas (polígonos) de los distritos.
    try:
        mapa_gdf = gpd.read_file('lima_callao_distritos_simple.geojson')
    except Exception as e:
        # Si el archivo no se encuentra, muestra un error claro y detiene la ejecución.
        st.error(f"🚨 **Error al cargar el archivo GeoJSON:** `{e}`")
        st.warning("Asegúrate de que el archivo `lima_callao_distritos_simple.geojson` esté en la misma carpeta que tu script.")
        st.stop()
    
    # Convierte cada diccionario de datos en un DataFrame de Pandas para poder unirlos.
    df_peligrosidad = pd.DataFrame(list(peligrosidad_data.items()), columns=['distrito_data', 'peligrosidad'])
    df_densidad = pd.DataFrame(list(densidad_poblacional.items()), columns=['distrito_data', 'densidad'])
    df_material = pd.DataFrame(list(material_data.items()), columns=['distrito_data', 'material_precario'])
    df_damnificados = pd.DataFrame(list(damnificados_data.items()), columns=['distrito_data', 'damnificados'])
    df_viviendas = pd.DataFrame(list(viviendas_data.items()), columns=['distrito_data', 'viviendas_destruidas'])

    # Une todos los DataFrames en uno solo usando el nombre del distrito como clave común.
    df = pd.merge(df_peligrosidad, df_densidad, on='distrito_data', how='outer')
    df = pd.merge(df, df_material, on='distrito_data', how='outer')
    df = pd.merge(df, df_damnificados, on='distrito_data', how='outer')
    df = pd.merge(df, df_viviendas, on='distrito_data', how='outer')

    # --- Cálculo del Índice de Riesgo Combinado ---
    # Para poder combinar variables con diferentes unidades (ej. personas vs. número de viviendas),
    # primero se normalizan. Esto convierte todos los valores a una escala común de 0 a 1.
    for column in ['peligrosidad', 'densidad', 'material_precario', 'damnificados', 'viviendas_destruidas']:
        min_val = df[column].min()
        max_val = df[column].max()
        if (max_val - min_val) > 0: # Evita la división por cero si todos los valores son iguales.
            df[f'norm_{column}'] = (df[column] - min_val) / (max_val - min_val)
        else:
            df[f'norm_{column}'] = 0

    # El índice de riesgo se calcula como el promedio de todas las variables normalizadas,
    # y se multiplica por 10 para tener una escala más intuitiva (de 0 a 10).
    df['riesgo_combinado'] = df[['norm_peligrosidad', 'norm_densidad', 'norm_material_precario', 'norm_damnificados', 'norm_viviendas_destruidas']].mean(axis=1) * 10
    
    # --- Fusionar Datos Geográficos y de Riesgo ---
    # Se define el nombre de la columna en el GeoJSON que contiene los nombres de los distritos.
    NOMBRE_COLUMNA_GEOJSON = 'distrito' 

    # Se estandarizan los nombres en ambos DataFrames (mayúsculas, sin espacios) para asegurar una unión correcta.
    mapa_gdf[NOMBRE_COLUMNA_GEOJSON] = mapa_gdf[NOMBRE_COLUMNA_GEOJSON].str.upper().str.strip()
    df['distrito_data'] = df['distrito_data'].str.upper().str.strip()

    # Se unen los datos geográficos (mapa_gdf) con los datos de riesgo (df).
    # 'how="left"' asegura que todos los distritos del mapa se conserven, incluso si no tienen datos de riesgo.
    merged_gdf = mapa_gdf.merge(df, left_on=NOMBRE_COLUMNA_GEOJSON, right_on='distrito_data', how="left")
    
    # Para los distritos que no tenían datos (ej. del Callao en algunas variables), se rellenan los valores nulos con 0.
    for col in ['peligrosidad', 'densidad', 'material_precario', 'damnificados', 'viviendas_destruidas', 'riesgo_combinado']:
        merged_gdf[col] = merged_gdf[col].fillna(0)
        
    return merged_gdf

# Se llama a la función para cargar y procesar todos los datos. El resultado se guarda en 'merged_gdf'.
merged_gdf = load_and_process_data(poblacion, area, peligrosidad_suelos, material_precario, damnificados_2000, viviendas_destruidas_2000)

# ==============================================================================
# 5. INTERFAZ DE USUARIO (BOTONES)
# ==============================================================================
st.write("### Selecciona una variable para visualizar en el mapa:")

# st.session_state se usa para guardar el estado de la aplicación, como qué botón está presionado.
# Esto evita que la selección se reinicie cada vez que el usuario interactúa.
if 'vista_seleccionada' not in st.session_state:
    st.session_state['vista_seleccionada'] = 'Riesgo Combinado' # Vista por defecto al abrir la app.

# Diccionario que mapea el nombre del botón a la columna de datos correspondiente.
vistas = {
    "Peligrosidad Suelos": "peligrosidad",
    "Densidad Poblacional": "densidad",
    "Material Precario": "material_precario",
    "Damnificados": "damnificados",
    "Viviendas Destruidas": "viviendas_destruidas",
    "Riesgo Combinado": "riesgo_combinado"
}

# st.columns(6) crea 6 columnas de igual ancho para colocar los botones horizontalmente.
cols = st.columns(6)

# Itera sobre los primeros 5 botones para crearlos con el estilo estándar.
for i, (nombre_vista, _) in enumerate(list(vistas.items())[:-1]):
    if cols[i].button(nombre_vista, use_container_width=True, key=f"btn_{i}"):
        st.session_state['vista_seleccionada'] = nombre_vista

# Crea el último botón ("Riesgo Combinado") con un estilo primario para destacarlo.
if cols[5].button("Riesgo Combinado", use_container_width=True, type="primary", key="btn_riesgo"):
    st.session_state['vista_seleccionada'] = "Riesgo Combinado"

# ==============================================================================
# 6. CREACIÓN Y VISUALIZACIÓN DEL MAPA
# ==============================================================================
# Se obtiene la selección actual del usuario desde el session_state.
vista_actual = st.session_state['vista_seleccionada']
columna_color = vistas[vista_actual]

st.subheader(f"Mapa de Calor: {vista_actual}")

# Se crea la figura del mapa de calor con Plotly Express.
fig = px.choropleth_mapbox(
    merged_gdf,
    geojson=merged_gdf.geometry,          # Las formas de los distritos.
    locations=merged_gdf.index,           # Identificador único para cada forma.
    color=columna_color,                  # La columna de datos que definirá el color.
    mapbox_style="carto-positron",        # Estilo del mapa base (minimalista).
    center={"lat": -12.0464, "lon": -77.0428}, # Coordenadas para centrar el mapa en Lima.
    zoom=8.5,                             # Nivel de zoom inicial.
    opacity=0.7,                          # Transparencia de los colores.
    color_continuous_scale="YlOrRd",      # Escala de colores (Amarillo -> Naranja -> Rojo).
    labels={columna_color: vista_actual}, # Etiqueta para la leyenda de colores.
    hover_name='distrito',                # Columna que se mostrará como título al pasar el mouse.
    hover_data={columna_color: ':.2f'}    # Datos adicionales a mostrar en el hover, con formato de 2 decimales.
)
# Ajusta los márgenes para que el mapa ocupe todo el espacio posible.
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# Muestra la figura de Plotly en la aplicación de Streamlit.
st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# 7. SECCIONES DE TEXTO INFORMATIVO
# ==============================================================================
st.write("---") # Separador visual.
st.subheader(f"Descripción de la variable: {vista_actual}")

# Diccionario con los textos explicativos para cada vista.
descripciones = {
    "Riesgo COmbinado": "Este índice es un promedio normalizado de todas las variables, ofreciendo una visión general del riesgo sísmico. Un valor más alto indica una mayor vulnerabilidad combinada.",
    "Peligrosidad Suelos": "Mide la probabilidad de que el suelo predominante del distrito amplifique las ondas sísmicas. Los valores más altos (suelos arenosos o blandos) son más peligrosos que los valores bajos (roca o conglomerado).",
    "Densidad Poblacional": "Representa la cantidad de habitantes por kilómetro cuadrado. Una mayor densidad puede complicar la evacuación y aumentar el número de personas afectadas.",
    "Material Precario": "Indica el número de viviendas construidas con materiales vulnerables (como adobe o quincha). A mayor número, mayor es el riesgo de colapso.",
    "Damnificados": "Muestra el número histórico de personas damnificadas por eventos sísmicos desde el año 2000 hasta 2025. Sirve como un indicador de vulnerabilidad pasada.",
    "Viviendas Destruidas": "Indica el número histórico de viviendas destruidas por eventos sísmicos desde el año 2000 hasta 2025, reflejando la fragilidad de las construcciones en esa zona años pasados."
}

descripcion_actual = descripciones.get(vista_actual, "No hay descripción disponible para esta vista.")

# Se usa st.markdown con HTML y CSS para crear un cuadro de texto con un color de fondo personalizado.
st.markdown(
    f"""
    <div style="background-color: #FFF3E0; padding: 1rem; border-radius: 0.5rem; border: 1px solid #FFE0B2;">
        <p style="color: #333; margin-bottom: 0;">{descripcion_actual}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Conclusiones Dinámicas ---
# st.expander crea una sección desplegable que está colapsada por defecto.
with st.expander("Ver Conclusiones Detalladas"):
    conclusiones = {
        "Riesgo Combinado": """
        El Índice de Resumen de Riesgo consolida múltiples factores para identificar las zonas con mayor y menor vulnerabilidad ante un sismo. Este análisis revela patrones claros en la distribución del riesgo en Lima y Callao.

        **Distritos de Mayor Riesgo:**
        - **1. Ventanilla:** Se posiciona como el distrito de más alto riesgo debido a la peor combinación de factores: una cantidad extremadamente alta de material precario (el mayor de todos con 15,000 viviendas) y una peligrosidad de suelo muy elevada (calificación de 9 sobre 10). Esta combinación lo hace excepcionalmente vulnerable a daños estructurales severos.
        - **2. Villa El Salvador:** Su riesgo se debe principalmente a tener la peor calidad de suelo de toda el área metropolitana (calificación de 10 sobre 10), lo que magnifica drásticamente cualquier sismo. Además, presenta el historial más alto de viviendas destruidas y damnificados, evidenciando una fragilidad estructural y social recurrente.
        - **3. San Juan de Lurigancho:** Aunque su suelo es moderadamente peligroso, su riesgo se dispara por tener la segunda mayor cantidad de viviendas precarias (casi 12,000) y una densidad poblacional considerable, lo que aumenta masivamente la exposición de su más de un millón de habitantes.

        **Distritos de Menor Riesgo:**
        - **1. La Molina:** Es consistentemente el distrito más seguro. Su bajo riesgo se debe a una excelente calidad de suelo (rocoso, con calificación de 2 sobre 10), una baja densidad poblacional y una cantidad mínima de construcciones precarias (solo 101).
        - **2. San Borja:** Similar a La Molina, se beneficia de un suelo rígido y estable (calificación de 3 sobre 10), junto con una cantidad ínfima de material precario (solo 27 viviendas) y un historial de daños casi nulo, lo que lo convierte en una zona de muy baja vulnerabilidad.
        - **3. San Isidro:** Su perfil de bajo riesgo se atribuye a un suelo de buena calidad, una planificación urbana que limita el material precario al mínimo (solo 11 viviendas) y una densidad poblacional moderada en comparación con los distritos más críticos.
        """,
        "Peligrosidad Suelos": "La peligrosidad de los suelos es un factor geológico clave. Distritos como Villa El Salvador, Chorrillos, Ventanilla y Callao son intrínsecamente más riesgosos debido a que sus suelos arenosos y blandos amplifican las ondas sísmicas. En contraste, La Molina y Chaclacayo, asentados sobre roca, son los más seguros en este aspecto.",
        "Densidad Poblacional": "Distritos como Breña, Lince y Surquillo, a pesar de su pequeño tamaño, tienen una concentración de población extremadamente alta. Esto, si bien no es un factor de daño directo, representa un riesgo social enorme, dificultando la evacuación y la respuesta de emergencia.",
        "Material Precario": "La vulnerabilidad de las construcciones es crítica. Ventanilla y San Juan de Lurigancho lideran negativamente en esta categoría, con miles de viviendas que podrían no resistir un sismo de gran magnitud. Esto indica una necesidad urgente de programas de reforzamiento estructural en estas áreas.",
        "Damnificados": "Teniendo en cuenta los hehcos históricos de los últimos 25 años por sismos, distritos como Villa El Salvador y Ate muestran una alta vulnerabilidad social pasada. Esto sugiere que, sin una intervención adecuada, estos distritos podrían volver a ser los más afectados en términos de población desplazada.",
        "Viviendas Destruidas": "Similar a los damnificados, el número de viviendas destruidas en el pasado en distritos como Villa El Salvador y Punta Hermosa señala las áreas donde la infraestructura ha sido históricamente más frágil. Es un llamado de atención sobre la calidad de construcción en estas zonas."
    }
    conclusion_actual = conclusiones.get(vista_actual, "")
    # Se usa HTML para justificar el texto y mejorar la legibilidad.
    st.markdown(f"<p style='text-align: justify;'>{conclusion_actual}</p>", unsafe_allow_html=True)


# ==============================================================================
# 8. FOOTER
# ==============================================================================
st.markdown("---")
# Se usa st.markdown con HTML para crear un pie de página con formato personalizado y enlaces.
st.markdown(
    """
    <div style="text-align: center; color: grey; font-size: 0.9em;">
        <p>Para más información frente a un sismo: <a href="https://www.gob.pe/1053-que-hacer-en-caso-de-sismo" target="_blank">https://www.gob.pe/1053-que-hacer-en-caso-de-sismo</a></p>
        <p>Aplicación desarrollada por <strong>Erick Farfan</strong> y <strong>Ayni Abad</strong><br>
        Pontificia Universidad Católica del Perú</p>
        <p><strong>Fuentes de datos:</strong> 
            <a href="https://www.inei.gob.pe/" target="_blank">INEI</a> | 
            <a href="https://www.indeci.gob.pe/" target="_blank">INDECI</a> | 
            <a href="https://github.com/joseluisq/peru-geojson-datasets/tree/master" target="_blank">GeoJSON Datasets</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
