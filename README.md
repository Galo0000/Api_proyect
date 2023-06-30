<h1 style="text-align:center">API de consulta y recomendacion de peliculas</h1>

<h4><span style="font-size:16px">El proyecto consiste en crear una API que reponda consultas y recomiende 5 peliculas en base a una ingresada, la api buscara la informacion en un base de datos que previamente paso por un proceso de ETL y de EDA para la creacion del modelo de ML.</span></h4>

<h2><strong><span style="font-size:26px">Requerimientos:</span></strong></h2>

<p><span style="font-size:20px">Lenguaje de programacion: Python 3.8 (etl y eda) y Python 3.7 (API)</span></p>

<p><span style="font-size:20px">Librerias: </span></p>

<ul>
	<li><span style="font-size:18px">FastAPI: Un marco web r&aacute;pido y f&aacute;cil de usar para crear APIs en Python.</span></li>
	<li><span style="font-size:18px">Pandas: Una libreria para an&aacute;lisis y manipulaci&oacute;n de datos en Python.</span></li>
	<li><span style="font-size:18px">NumPy: Una libreria para procesamiento num&eacute;rico en Python.</span></li>
	<li><span style="font-size:18px">Scikit-learn (Sklearn): Una libreria de aprendizaje autom&aacute;tico en Python.</span></li>
	<li><span style="font-size:18px">SciPy: Una libreria para procesamiento y an&aacute;lisis cient&iacute;fico en Python.</span></li>
	<li><span style="font-size:18px">Seaborn: Una libreria de visualizaci&oacute;n de datos en Python basada en Matplotlib.</span></li>
	<li><span style="font-size:18px">Uvicorn: Un servidor web de alto rendimiento para aplicaciones web en Python.</span></li>
	<li><span style="font-size:18px">Wordcloud: Una libreria para crear nubes de palabras en Python.</span></li>
	<li><span style="font-size:18px">Picke: Una libreria ya incorporada&nbsp;en Python para archivos tipo pickle.</span></li>
</ul>

<p><strong><span style="font-size:26px">Estructura de carpetas</span></strong></p>

<p><span style="font-size:20px">Data: Contiene los datasets confeccionados.</span></p>

<p><span style="font-size:20px">ETL_EDA: Contiene los notebooks en donde se realizo el ETL y el EDA</span></p>

<p><span style="font-size:20px">Model: Esta carpeta guarda las dependencias del proyecto.</span></p>

<p><span style="font-size:20px">main.py: Archivo de Python donde se encuentra el motor de la api.</span></p>

<p><span style="font-size:20px">requirements.txt: Contiene la lista de librerias necesarias para el entorno virtual de render.</span></p>

<p><span style="font-size:20px">Models: Esta carpeta contiene archivos pkl de los modelos entrenados de machine learning.</span></p>

<p><span style="font-size:20px">Images: Esta carpeta contiene imagenes de la etapa de EDA.</span></p>

<p>&nbsp;</p>

<p><span style="font-size:26px"><strong>Descripci&oacute;n del Proyecto</strong></span></p>

<p><span style="font-size:20px">Recursos</span></p>

<p style="text-align:center"><span style="font-size:18px">Se nos proporcionaron dos archivos CSV llamados movies_dataset y credits, los cuales conten&iacute;an la informaci&oacute;n necesaria para iniciar el proyecto.</span></p>

<ul>
	<li><span style="font-size:18px">movies_dataset: Este archivo contiene informaci&oacute;n sobre pel&iacute;culas, como t&iacute;tulos, productoras, datos estad&iacute;sticos, costos, etc.</span></li>
	<li><span style="font-size:18px">credits: En este archivo se encuentran columnas de IDs que est&aacute;n relacionadas con las columnas de IDs del archivo movies_dataset. Tambi&eacute;n contiene una columna llamada &quot;crew&quot; con informaci&oacute;n organizacional de cada pel&iacute;cula, y la columna &quot;cast&quot; con informaci&oacute;n sobre los actores de cada pel&iacute;cula.</span></li>
</ul>

<p style="text-align:center"><span style="font-size:18px">Para comenzar el proyecto, se cargaron estos dos archivos como dataframes de Pandas, permitiendo iniciar la etapa de ETL.</span></p>

<p style="text-align:center"><span style="font-size:18px">ETL (Extract, Transform, Load)</span></p>

<p style="text-align:center"><span style="font-size:18px">En primer lugar, se abordaron los requerimientos m&iacute;nimos trabajando con el archivo movies_dataset, el cual fue cargado en una variable llamada df_movies.</span></p>

<p style="text-align:center"><span style="font-size:18px">Se analizaron los tipos de datos de cada columna y se realizaron las transformaciones necesarias para su mejor aprovechamiento.</span></p>

<p style="text-align:center"><span style="font-size:18px">Adem&aacute;s, se encontraron columnas que conten&iacute;an listas con diccionarios o simplemente diccionarios, pero ambos estaban almacenados como texto. Por lo tanto, se crearon funciones para transformar los valores de esas columnas al tipo de dato correcto, y luego se extrajeron los datos m&aacute;s relevantes seg&uacute;n el objetivo del proyecto.</span></p>

<p style="text-align:center"><span style="font-size:18px">Despu&eacute;s de trabajar en el dataframe df_movies, se analiz&oacute; el contenido del archivo credits, donde se observ&oacute; el mismo problema de almacenamiento incorrecto de grandes cantidades de informaci&oacute;n. Se abord&oacute; de manera similar, aplicando las transformaciones necesarias.</span></p>

<p style="text-align:center"><span style="font-size:18px">Se decidi&oacute; unir los dos dataframes para reducir la complejidad a la hora de realizar consultas a trav&eacute;s de la API.</span></p>

<p style="text-align:center"><span style="font-size:18px">Una vez finalizada la etapa de ETL, se guard&oacute; el dataframe resultante en un archivo pickle. Posteriormente, se cre&oacute; otro dataframe con la informaci&oacute;n que ser&iacute;a solicitada por la API, con el objetivo de reducir el tama&ntilde;o del archivo llamado &quot;api.pickle&quot;. Finalmente, se gener&oacute; otro dataframe orientado al uso del modelo de machine learning llamado &quot;ML.pickle&quot;.</span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><strong><span style="font-size:28px">EDA</span></strong></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:18px">El EDA (An&aacute;lisis Exploratorio de Datos) es una t&eacute;cnica utilizada en ciencia de datos para explorar, analizar y comprender los datos antes de realizar an&aacute;lisis m&aacute;s avanzados. Ayuda a identificar patrones, detectar anomal&iacute;as y obtener informaci&oacute;n relevante para investigaciones posteriores.</span></p>

<p style="text-align:center"><span style="font-size:18px">Analisis de los datos numericos del dataframe</span></p>

<p style="text-align:center"><span style="font-size:18px">Grafico de correlacion</span></p>

<p style="text-align:center"><span style="font-size:18px">Un gr&aacute;fico de correlaci&oacute;n muestra la relaci&oacute;n entre dos variables. Los puntos en el gr&aacute;fico representan las observaciones y su ubicaci&oacute;n indica los valores de las variables. Se utiliza para identificar la fuerza y direcci&oacute;n de la relaci&oacute;n entre las variables.</span></p>

<p style="text-align:center">&nbsp;</p>

<p><img src="https://github.com/Galo0000/Api_proyect/blob/main/Images/corr.jpg" /></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:18px">Se puede observar que los columnas con mayor correlacion son budget, popularity, revenue, vote_count.</span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:18px">Grafico nube de palabras</span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:18px">Un gr&aacute;fico de nubes de palabras es una representaci&oacute;n visual que muestra las palabras m&aacute;s frecuentes en un texto o conjunto de datos. En este tipo de gr&aacute;fico, las palabras se presentan en tama&ntilde;o y posici&oacute;n seg&uacute;n su importancia o frecuencia, siendo las palabras m&aacute;s comunes m&aacute;s grandes y destacadas. Es una forma r&aacute;pida y visualmente atractiva de resumir y visualizar los t&eacute;rminos clave o temas dominantes en un conjunto de texto.</span></p>

<p style="text-align:center">&nbsp;</p>

<p><img src="https://github.com/Galo0000/Api_proyect/blob/main/Images/nubepalabras.jpg" /></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:18px">Aqui se muestra las palabras en los nombres de cada pelicula que mas se repiten en la base de datos</span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:18px">Matriz de graficos de dispersion</span></p>

<p style="text-align:center"><span style="font-size:18px">Una matriz de gr&aacute;ficos de dispersi&oacute;n es una representaci&oacute;n visual que muestra m&uacute;ltiples gr&aacute;ficos de dispersi&oacute;n en una matriz. Cada gr&aacute;fico de dispersi&oacute;n compara la relaci&oacute;n entre dos variables diferentes. Esta matriz permite una r&aacute;pida comparaci&oacute;n y an&aacute;lisis de m&uacute;ltiples relaciones entre variables al mismo tiempo.</span></p>

<p style="text-align:center">&nbsp;</p>

<p><img src="https://github.com/Galo0000/Api_proyect/blob/main/Images/pairplt.jpg" /></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:18px">Grafico de cajas</span></p>

<p style="text-align:center"><span style="font-size:18px">Un gr&aacute;fico de cajas, tambi&eacute;n conocido como diagrama de caja y bigotes, es una representaci&oacute;n visual que muestra la distribuci&oacute;n de un conjunto de datos mediante una caja y l&iacute;neas llamadas &quot;bigotes&quot;. La caja representa el rango intercuart&iacute;lico, es decir, el 50% central de los datos, mientras que los bigotes representan el m&iacute;nimo y m&aacute;ximo no considerados como valores at&iacute;picos. Adem&aacute;s, una l&iacute;nea dentro de la caja marca la mediana. Este gr&aacute;fico es &uacute;til para analizar la dispersi&oacute;n y la simetr&iacute;a de los datos, as&iacute; como para identificar valores at&iacute;picos potenciales.</span></p>

<p style="text-align:center">&nbsp;</p>

<p><img src="https://github.com/Galo0000/Api_proyect/blob/main/Images/popularity.jpg" /></p>

<p style="text-align:center"><span style="font-size:18px">Grafico de cajas de popularity donde se observo la mayor distancia entre los valores</span></p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p style="text-align:center"><span style="font-size:18px">Video de demostracion</span></p>

<p style="text-align:center"><span style="font-size:18px">https://drive.google.com/file/d/1YsZ5kiKXRAjKQwt2JpgNH8QUQQWhvB7w/view?usp=drive_link</span></p>