# Planteamiento del proyecto

**Título tentativo:** Diseño e implementación de una plataforma de analítica de partidas de League of Legends con predicción de resultados a partir de datos de la API de Riot Games.

**Autor:** David Felipe Barragán Bustos
**Programa:** Ingeniería de Sistemas
**Universidad:** Universidad Libre
**Director del programa:** Mauricio Antonio Alonso Moncada
**Decana:** Nidia María Jirado Taján
**Director del proyecto:** [Por definir]
**Versión:** borrador 0.1

## 1. Planteamiento del problema

League of Legends genera una gran cantidad de datos por partida: oro, experiencia, objetivos, eliminaciones y visión, registrados minuto a minuto. Sin embargo, las herramientas habituales para jugadores se limitan a estadísticas agregadas como el winrate y el KDA, que describen lo ocurrido pero no explican en qué momento ni por qué factores se decide una partida.

No se cuenta con una plataforma abierta y reproducible que integre la recolección de estos datos, su almacenamiento estructurado y un modelo que estime la probabilidad de victoria durante la partida, explicando qué variables pesan más en cada fase del juego.

**Pregunta de investigación:** ¿Con qué antelación y con qué precisión puede predecirse el resultado de una partida a partir de las variables de su línea de tiempo, y qué factores tienen mayor peso en cada fase?

## 2. Justificación

- **Técnica:** el proyecto exige resolver problemas reales de ingeniería de sistemas: ingesta de datos con límites de peticiones, modelado de datos relacional, arquitectura por capas, API, pruebas automatizadas y despliegue.
- **Analítica:** permite aplicar aprendizaje automático supervisado sobre un conjunto de datos propio, con métricas objetivas de evaluación.
- **Práctica:** ofrece a los jugadores información sobre qué variables influyen más en el resultado, con una herramienta reproducible.

## 3. Objetivos

**Objetivo general**

Diseñar e implementar una plataforma que recolecte, almacene y analice datos de partidas de League of Legends, e incorpore un modelo de predicción del resultado a partir de la línea de tiempo de cada partida.

**Objetivos específicos**

1. Diseñar una arquitectura de ingesta que respete los límites de la API de Riot Games y permita recolectar partidas de forma sostenida.
2. Construir un almacén de datos relacional para partidas, participantes y líneas de tiempo, con control de duplicados y versionado de parches.
3. Definir las variables (features) por minuto y entrenar modelos de clasificación, comparando su desempeño con métricas como AUC, exactitud y calibración.
4. Analizar la importancia de las variables por fase de la partida y, si el tiempo lo permite, por rol y por rango.
5. Exponer los resultados mediante una API y un panel de visualización.
6. Validar el sistema con pruebas funcionales, de rendimiento y de calidad del modelo.

## 4. Alcance y limitaciones

**Alcance**

- Partidas de la API oficial de Riot Games (ACCOUNT-V1, LEAGUE-V4 y MATCH-V5).
- Análisis posterior a la partida y estimación de probabilidad con datos hasta un minuto dado, sin ofrecer asistencia en tiempo real durante el juego.
- Un conjunto limitado de colas (por ejemplo, clasificatoria solo/dúo) y de regiones.

**Limitaciones**

- Los límites de peticiones de la API condicionan el volumen de datos y el tiempo de recolección.
- Las claves de desarrollo expiran cada 24 horas; se solicitará una clave personal.
- Los cambios de parche alteran el equilibrio del juego, por lo que los modelos se evalúan por versión.
- El proyecto cumple las políticas de desarrolladores de Riot Games y no está respaldado por Riot Games.

## 5. Metodología

- **Plataforma:** desarrollo iterativo e incremental con tablero de tareas en GitHub, ramas por funcionalidad e integración continua.
- **Datos y modelo:** CRISP-DM (comprensión del problema, comprensión y preparación de datos, modelado, evaluación y despliegue).
- **Calidad:** pruebas automatizadas con pytest, revisión de estilo con ruff y registro de decisiones técnicas en `docs/decisiones`.

## 6. Cronograma preliminar

| Fase | Actividades | Duración estimada |
|---|---|---|
| 1. Datos | Clave personal, ingesta masiva, timelines, limpieza | 1 a 2 meses |
| 2. Modelo | Features, entrenamiento, evaluación, importancia de variables | 1 a 2 meses |
| 3. Plataforma | API de predicción, panel, CI/CD, despliegue | 1 a 2 meses |
| 4. Cierre | Pruebas finales, documento y sustentación | 1 mes |