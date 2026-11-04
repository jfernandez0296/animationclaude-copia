<callout icon="🎯" color="blue_bg">
	**Resultado:** dos versiones del mismo video, una de 30 s y otra de 60 s para YouTube (prompts 1 y 2 más abajo), en 1920×1080, 30 fps, en español, con la identidad de marca de ScalyAI. Cuenta una historia en cinco actos (de una venta perdida de noche a un negocio que responde y mide solo), con profundidad 3D, transiciones de letras y un celular con chatbot. Se hace con Claude Code + HyperFrames: el video se escribe como HTML y se renderiza a MP4.
</callout>
<table_of_contents/>
---
## Cómo evolucionó el video
<table header-row="true">
<tr>
<td>Versión</td>
<td>Qué tenía</td>
</tr>
<tr>
<td>10 s</td>
<td>Cuatro escenas con la paleta inventada (fondo oscuro)</td>
</tr>
<tr>
<td>12 s</td>
<td>Colores reales de la marca, transiciones, entradas distintas y celular con chatbot</td>
</tr>
<tr>
<td>30 s</td>
<td>Tres escenas de automatización, transiciones de letras, fondo en capas, profundidad 3D y una historia con hilo conductor</td>
</tr>
<tr>
<td>60 s (YouTube)</td>
<td>Diez escenas: se suman la presentación de la marca, "cómo trabajamos", "hecho para PyMEs" y un cierre largo y tranquilo; nueve transiciones y sin rótulo en la esquina superior izquierda</td>
</tr>
</table>
## Prompt 1: el video de 30 s, de una sola vez
El video se fue construyendo en muchas vueltas (ver "Los prompts, en orden" al final). Este es un único prompt que reúne todo lo aprendido, para obtener el mismo resultado desde cero. Se pega en Claude Code con las skills de HyperFrames instaladas.
<callout icon="📋" color="green_bg">
	Antes de pegarlo: ten a mano una captura de la web de la marca (para colores y tipografía) y el texto real de su propuesta. Reemplaza los datos de ScalyAI por los de tu cliente.
</callout>
```plain text
Usa /hyperframes y crea un video de producto de 30 segundos para ScalyAI (scalyai.dev), en español, sin narración ni música, en 16:9 (1920×1080, 30 fps). Debe contar una historia en cinco actos, con coherencia entre escenas y sin verse plano.

=== 1. IDENTIDAD DE MARCA (la sacas de la captura adjunta, no la inventes) ===
- Fondo crema #F0F0E8, titulares azul marino #061A36, acento verde azulado #007A82, texto secundario gris pizarra #4F626B, degradado del botón #0E3A5E, #20748C, #42CFD2.
- Tipografía Manrope. Guarda los .woff2 dentro del proyecto. Guarda también GSAP dentro del proyecto (sin CDN) para que el render funcione sin red.
- La escena nocturna es la única oscura (azul marino). El resto usa la paleta clara de la marca.

=== 2. CONTENIDO REAL (no inventes datos de la empresa) ===
- Lema: "Software e IA a la medida de tu negocio".
- Conecta CRM, WhatsApp, hojas de cálculo (Excel) y ERP. Chatbot que atiende en WhatsApp y registra en el CRM.
- Implementación en 2 semanas, ROI medible en 6 semanas.
- Botón de la web: "Conversemos de tu próximo piloto" y "30 minutos · sin tarjeta · sin compromiso".
- Las cifras de las escenas de automatización (12 h, 18 h, 1.240 pedidos, 0 errores, el gráfico) son ilustrativas: ponlas, pero con el aviso "Datos ilustrativos" escrito en pantalla.

=== 3. HISTORIA Y COHERENCIA ===
- Hilo conductor: un cliente escribe a las 11:40 p. m. "Hola, ¿tienen stock de la talla M?" y nadie responde, así que se pierde la venta. Con ScalyAI, ese mismo mensaje recibe respuesta en 2 segundos y el pedido #1042 recorre un flujo conectado hasta cerrar la venta mientras el dueño duerme.
- Usa el mismo ejemplo de punta a punta: el mensaje de la talla M, la hora 11:40 p. m. (visible también en el celular del chatbot) y el pedido #1042 deben reaparecer en varias escenas.
- El color cuenta la historia: noche oscura al inicio, y un amanecer que revela el mundo claro de la marca.
- Un hilo visible: un chip de capítulo arriba a la izquierda ("El problema", "El cambio", "La automatización", "El resultado", "Tu turno", con puntos de avance) y una barra de progreso inferior con una marca por acto. Cada etiqueta entra y sale letra a letra.

=== 4. ESCENAS (tiempos en segundos; las escenas se solapan durante las transiciones) ===
ACTO 1 · El problema (0 a 5): escena nocturna oscura con estrellas que titilan y una luna.
  - Reloj con tarjetas que se voltean en 3D: "11 : 40 p. m." y la etiqueta "MARTES POR LA NOCHE".
  - Notificación de WhatsApp que entra con inclinación 3D, anillo de aviso (ping), vibración y una insignia roja "1": "Cliente nuevo · Hola, ¿tienen stock de la talla M?".
  - Tres frases que se reemplazan, cada una con un efecto de letras distinto: "Un cliente escribe." (letras que suben en ola), "Nadie responde." (máquina de escribir con destello cian) y "Ya le compró a otro." (letras que caen y rebotan, "otro" en coral).
  - Un recuadro "Sin respuesta: [contador que gira de 0 a 8] h". La notificación se apaga en gris y cae el sello "VENTA PERDIDA" con sacudida.
ACTO 2 · El cambio (4,3 a 14,9):
  a) Tareas (4,3 a 10,5): amanece con un reveal circular que sale de la luna. Titular "De día, todo a mano." y una tarjeta 3D con 5 tareas pendientes (Copiar el pedido #1042 a Excel, Responder: ¿hay talla M?, Pasar el #1042 al CRM, Enviar recordatorio de pago, Armar el reporte semanal), con alertas rojas que rebotan y filas nerviosas. Luego el titular cambia letra a letra a "Ahora, se hacen solas.", aparece la etiqueta "ScalyAI activado", pasa un destello por la tarjeta y una franja de luz recorre la lista: cada tarea se marca, su etiqueta cambia de "Pendiente" a "Automático" y sale una ráfaga de chispas. Al final, "Todo al día" y un contador "Tiempo recuperado" que gira hasta 12 h por semana.
  b) Chatbot (9,9 a 14,9): título "Conectamos tus herramientas" y la frase "Ese mensaje de las 11:40 p. m. ahora recibe respuesta al instante."; píldoras CRM, WhatsApp, Excel, ERP que se voltean en 3D desde el centro y se conectan con una línea. A la derecha, un celular dibujado en HTML y CSS que gira en 3D y flota, con un halo que late, y tres insignias flotantes (chat, hoja de cálculo, persona) con rebote elástico. Chat "ScalyAI Bot" con la hora 11:40 p. m.: el cliente pregunta por la talla M, el bot escribe (tres puntos), responde "¡Sí! Quedan 8 unidades. ¿Te la reservo?" con la etiqueta "Respondió en 2 segundos", el cliente dice "Sí, por favor" y el bot confirma con el recibo "Pedido #1042 · CRM". Cada burbuja sale de la esquina de su colita.
ACTO 3 · La automatización (14,4 a 20,1): título "Un solo flujo. Cero copiar y pegar." (letras que brotan del centro y se voltean al salir). Cinco nodos conectados: "Llega un mensaje (Pedido #1042)", "La IA responde", "Crea el pedido", "Actualiza stock", "Avisa al equipo". El plano completo se levanta en 3D y la cámara se desplaza para dar paralaje. Un punto de luz viaja entre los nodos y cada uno se enciende con una onda y una marca de verificación. Una rama punteada dice "Si hay una duda, pasa a una persona". Cierra con el banner "Mientras dormías, la venta se cerró."
ACTO 4 · El resultado (19,5 a 26,6):
  a) Panel (19,5 a 24,3): reveal circular desde el centro. Título "A la mañana, todo se mide." (máquina de escribir con destello de color) y un sol "8:00 a. m." con rayos que giran. Cuatro tarjetas que se voltean en 3D con números que giran como tragamonedas: 18 h ahorradas por semana, 1.240 pedidos sin tocar a mano, 0 errores al copiar datos, 24/7 atención a clientes. Debajo, un gráfico de barras de horas manuales (grises, bajan) contra automatizadas (verde azulado, suben) en 8 semanas, con barras que rebotan.
  b) Promesa (23,7 a 26,65): "Listo en 2 semanas." y "ROI medible en 6." con dígitos tragamonedas, máscara de izquierda a derecha, brillo sobre el texto, entrada en 3D y, al caer el "6", tres anillos de choque y una ráfaga de chispas.
ACTO 5 · Tu turno (26,6 a 30): barrido diagonal con el degradado de la marca que descubre el logo. "ScalyAI." letra a letra con el punto final en acento, el lema palabra por palabra saliendo de un desenfoque, "scalyai.dev", anillos y chispas al caer el punto, un destello que cruza el logo y el botón "Conversemos de tu próximo piloto →" que salta con resorte, con "30 minutos · sin tarjeta · sin compromiso" debajo.

=== 5. TRANSICIONES (seis distintas, todas con solape entre escenas) ===
1) Noche a día: círculo de luz que crece desde la luna. 2) Tareas a chatbot: zoom que atraviesa. 3) Chatbot a flujo: empuje lateral con desenfoque. 4) Flujo a panel: círculo que crece desde el centro. 5) Panel a promesa: empuje hacia abajo con desenfoque. 6) Promesa a logo: barrido diagonal con el degradado del botón.
La escena que entra con un reveal circular debe tener fondo opaco propio que se desvanezca después, para que vuelva el fondo en capas. Si una escena tiene salida propia y la transición también la mueve, quita la salida propia.

=== 6. PROFUNDIDAD (que no se vea plano) ===
- Fondo en capas: tres luces suaves que se desplazan por rutas distintas, un piso de cuadrícula en perspectiva que avanza hacia la cámara, anillos punteados que giran y unas 34 partículas que suben y titilan.
- Tarjetas, celular y plano del flujo inclinados en 3D (transformPerspective) que flotan despacio. Sombras en dos capas.
- Cámara: cada escena avanza un 3 a 5 % durante toda su duración.
- Energía: ondas al encenderse los nodos, chispas al marcar tareas, anillos de choque, barras con rebote elástico, destellos de luz.
- Cada escena entra con un movimiento dominante distinto. Evita repetir el mismo efecto en escenas vecinas.

=== 7. REGLAS TÉCNICAS DE HYPERFRAMES ===
- Escenas como sub-composiciones (data-composition-src) con su contenido dentro de template, una sola línea de tiempo GSAP pausada por composición y tl.seek(0) al final.
- Todo determinista: nada de Math.random ni Date.now. El azar con un generador de semilla fija.
- Colores solo en variables CSS. Fuente local con @font-face. El título y el contenido sin br.
- El index.html solo monta las escenas y anima las transiciones. Cada escena anima lo suyo. Las ranuras duran hasta que termina su transición de salida.
- Contraste mínimo 4,5 a 1 en textos. Los textos grises no deben quedar demasiado claros.

=== 8. PROCESO Y ENTREGA ===
- Crea el proyecto en videos/scalyai-intro con hyperframes init (motion-graphics) y guarda un shot-plan.json con la historia, las escenas, la paleta y los tiempos.
- Busca primero en el catálogo (hyperframes catalog) y usa bloques existentes solo si encajan (por ejemplo logo-brand-close para el cierre).
- Ejecuta hyperframes check hasta que pase. Saca snapshots de cada escena y de cada transición y MÍRALOS antes de renderizar. Corrige huecos vacíos, textos que se tapan o elementos cortados.
- Instala ffmpeg si falta, renderiza con hyperframes render a renders/video.mp4 y comprueba que dure 30,0 s. Si pesa más de 30 MB, crea renders/video-compartir.mp4 con ffmpeg (libx264, crf 23, yuv420p, faststart).
- Haz commit y push a la rama indicada después de cada cambio importante. No abras PR salvo que te lo pida.
- Al terminar, resume escena por escena qué hay, avisa qué datos son ilustrativos y adjunta el video.
```
<callout icon="💡" color="yellow_bg">
	**Versión corta** (si prefieres ir por vueltas): 1) video de 10 s con /hyperframes, 2) colores y tipografía de la marca desde una captura, 3) transiciones y entradas distintas, 4) celular con chatbot, 5) alargar a 30 s con escenas de automatización, 6) transiciones de letras y profundidad 3D, 7) historia y coherencia. Cada vuelta se revisa y se exporta antes de pasar a la siguiente.
</callout>
## Prompt 2: la versión de 60 s para YouTube
Es la segunda vuelta: parte del proyecto de 30 s (se copia la carpeta a `videos/scalyai-60s/`) y lo amplía a diez escenas con la marca, el "cómo trabajamos" y un cierre largo. Se pega en Claude Code con las skills instaladas y el proyecto de 30 s ya en el repositorio.
<callout icon="⚠️" color="yellow_bg">
	Antes de publicar: los precios ("desde S/1.500") y el rango de PyMEs (S/10k a S/500k al mes) salen de la ficha pública del buscador, no de la web de ScalyAI. Confírmalos. La escena lleva la nota "Referencial: consulta condiciones en [scalyai.dev](http://scalyai.dev)".
</callout>
```plain text
Usa /hyperframes y crea un video de 60 segundos para ScalyAI (scalyai.dev), en español, 16:9 (1920×1080, 30 fps), pensado para YouTube, sin audio. Objetivo: presentar la marca, explicar su propuesta de valor y destacar sus 3 características principales. Parte del proyecto de 30 s que ya existe en videos/scalyai-intro: cópialo a videos/scalyai-60s y reutiliza sus escenas (noche, tareas, chatbot, flujo, panel, promesa y cierre). Deja intacta la versión de 30 s.

=== 1. PROCESO (en este orden) ===
1) Primero entrégame el guion por escenas con tiempos y el storyboard, y espera mi aprobación. Luego construye.
2) Ejecuta hyperframes check hasta que pase, saca snapshots de cada escena y de cada transición y MÍRALOS antes de renderizar.
3) Renderiza y comprueba que dure exactamente 60,0 s. Haz commit y push después de cada hito. No abras PR.

=== 2. DATOS (no inventes nada) ===
- Reales: lema "Software e IA a la medida de tu negocio"; conecta CRM, WhatsApp, hojas de cálculo y ERP; chatbot que atiende en WhatsApp; las tres promesas de la web: "Automatizamos lo repetitivo", "Ponemos tus datos a trabajar", "Ordenamos tu operación"; implementación en 2 semanas y ROI medible en 6; botón "Conversemos de tu próximo piloto" con "30 minutos · sin tarjeta · sin compromiso".
- Por verificar (de la ficha pública): paquetes desde S/1.500 y PyMEs que facturan entre S/10k y S/500k al mes. Muéstralos con la nota "Referencial: consulta condiciones en scalyai.dev".
- Ilustrativos, con el aviso "Datos ilustrativos" en pantalla: el caso de las 11:40 p. m., el pedido #1042, las 12 h y 18 h, los 1.240 pedidos, el gráfico.
- No uses logos de clientes ni inventes testimonios. (Con el logo oficial ya disponible, ver el paso 17b.) Sin el SVG oficial del logo, usa el nombre "ScalyAI." con la tipografía de la marca.

=== 3. MARCA ===
- Fondo crema #F0F0E8, titulares azul marino #061A36, acento verde azulado #007A82, texto secundario #4F626B, degradado del botón #0E3A5E, #20748C, #42CFD2. Tipografía Manrope con los .woff2 dentro del proyecto. La escena nocturna es la única oscura.

=== 4. HISTORIA EN DIEZ ESCENAS (tiempos en segundos; se solapan durante las transiciones) ===
01 · 0 a 5, GANCHO: noche oscura, reloj "11:40 p. m.", notificación de WhatsApp "Hola, ¿tienen stock de la talla M?", contador "Sin respuesta" hasta 8 h y sello VENTA PERDIDA. Sin logo todavía.
02 · 4,3 a 10,5, PROBLEMA: amanece con un círculo de luz desde la luna. "De día, todo a mano." con tareas pendientes y alertas; el titular cambia letra a letra a "Ahora, se hacen solas."; una franja de luz marca cada tarea como Automático con chispas.
03 · 10 a 18, LA MARCA (nueva): "Esto es ScalyAI." con las letras que se voltean desde el centro, el lema palabra por palabra y las tres promesas de la web como tarjetas 3D que se resaltan una a una.
04 · 17,5 a 22,5, SOLUCIÓN A: "Conectamos tus herramientas"; el celular con el chatbot responde el mismo mensaje de las 11:40 p. m. en 2 segundos y aparece el recibo "Pedido #1042 · CRM".
05 · 22 a 27,7, SOLUCIÓN B: "Un solo flujo. Cero copiar y pegar." Cinco nodos conectados por los que viaja el pedido #1042; "Mientras dormías, la venta se cerró."
06 · 27,1 a 31,9, SOLUCIÓN C: "A la mañana, todo se mide." (8:00 a. m.), cuatro indicadores y gráfico de barras manual contra automatizado.
07 · 31,4 a 40, CÓMO TRABAJAMOS (nueva): "Sin proyectos eternos." Tres pasos con un punto que recorre la línea: 1 Elegimos un proceso, 2 Lo conectamos y lo ponemos a funcionar, 3 Medimos el retorno. Banner "Empezamos con un piloto, no con una apuesta."
08 · 39,5 a 42,45, LA PROMESA: "Listo en 2 semanas. ROI medible en 6." con anillos de choque.
09 · 41,9 a 49,1, HECHO PARA PyMEs (nueva): título "Hecho para PyMEs.", control deslizante de S/10k a S/500k y tarjeta "Paquetes desde S/1.500" con las cifras que giran, más "Se empieza con un piloto" y la nota de referencial.
10 · 49,2 a 60, TU TURNO: "ScalyAI." letra a letra, lema, scalyai.dev y el botón "Conversemos de tu próximo piloto" con "30 minutos · sin tarjeta · sin compromiso". Los últimos 10 s quedan tranquilos para las pantallas finales de YouTube (solo el botón respira).

=== 5. NUEVE TRANSICIONES DISTINTAS ===
1) Noche a día: círculo de luz desde la luna. 2) Tareas a marca: zoom que atraviesa. 3) Marca a chatbot: empuje hacia arriba con desenfoque. 4) Chatbot a flujo: empuje lateral con desenfoque. 5) Flujo a panel: círculo desde el centro. 6) Panel a "cómo trabajamos": barrido diagonal. 7) "Cómo trabajamos" a promesa: empuje hacia abajo. 8) Promesa a PyMEs: apertura horizontal como puertas. 9) PyMEs a cierre: barrido con el degradado del botón. Las escenas que entran con apertura o barrido tienen fondo opaco propio que se desvanece medio segundo después.

=== 6. MOVIMIENTO Y PROFUNDIDAD ===
- Los títulos entran y salen letra por letra, con un estilo distinto por escena. Fondo en capas de 60 s (luces que se desplazan, piso en perspectiva, anillos que giran, polvo), elementos inclinados en 3D, avance suave de cámara en cada escena, destellos, ondas y chispas.
- NO pongas ningún rótulo ni chip en la esquina superior izquierda. Solo una barra de progreso fina abajo.

=== 7. REGLAS TÉCNICAS ===
- Escenas como sub-composiciones con su contenido dentro de template; una línea de tiempo GSAP pausada por composición con tl.seek(0). Todo determinista: el azar con generador de semilla fija.
- No animes letterSpacing ni left/top: usa transformaciones (scaleX, x, y). Los destellos que cruzan la pantalla deben desvanecerse al terminar, o se quedan como una franja pálida.
- Las ranuras de cada escena duran hasta que acaba su transición de salida. El cierre usa logo-brand-close con una duración de 10,8 s (queda quieto).
- Contraste mínimo 4,5 a 1. Fija la versión del programa: npx --yes hyperframes@0.8.96 (la última puede no estar disponible y falla con un 404).

=== 8. ENTREGA ===
- El render de 60 s tarda unos 6 minutos: lánzalo en segundo plano. Comprueba que dure 60,0 s.
- El archivo pesa unos 60 MB: crea renders/video-compartir.mp4 con ffmpeg (libx264, crf 24, yuv420p, faststart, sin audio), que queda en unos 12 MB.
- Al terminar, resume escena por escena, avisa qué datos son ilustrativos y cuáles hay que verificar, y adjunta la copia ligera.
```
<callout icon="💡" color="blue_bg">
	**Diferencias con el prompt 1:** pide primero el guion y el storyboard para aprobarlos, parte del proyecto existente en vez de empezar de cero, separa los datos reales, los que hay que verificar y los ilustrativos, y prohíbe el rótulo de la esquina superior izquierda.
</callout>
## Qué necesitas antes de empezar
- Claude Code (en la nube o local) con acceso a la terminal.
- Node 18 o superior y `ffmpeg` instalado (sin ffmpeg no se puede exportar el MP4).
- Un repositorio donde guardar el proyecto.
- Una captura de pantalla de la web del cliente si el entorno no puede entrar al sitio (de ahí salen colores y tipografía).
- Opcional: clave o sesión de HeyGen para voz en off con IA.
## Paso 1. Instalar las skills de HyperFrames
Las skills son instrucciones que Claude consulta para construir el video correctamente. Se instalan en el proyecto, no en la carpeta de usuario, para que no se pierdan cuando termina la sesión.
```bash
npx skills add heygen-com/hyperframes -a claude-code -s '*' -y --copy
```
- Quedan en `.claude/skills/` (21 skills, unos 19 MB).
- Se ejecutan con permisos completos del agente: revísalas antes de confiar en ellas.
- Se activan en la **siguiente** sesión. Dentro de la actual se invocan por nombre.
## Paso 2. Pedir el video con /hyperframes
Prompt usado:
```plain text
Using /hyperframes, make a 10-second product intro for http://scalyai.dev/ en español
```
`/hyperframes` es la puerta de entrada. Decide la ruta según lo que pides:
<table header-row="true">
<tr>
<td>Lo que pides</td>
<td>Ruta</td>
</tr>
<tr>
<td>Promo larga de una web (30 a 90 s)</td>
<td>product-launch-video</td>
</tr>
<tr>
<td>Pieza corta, sin narración, donde el movimiento es el mensaje</td>
<td>motion-graphics</td>
</tr>
<tr>
<td>Presentación o deck</td>
<td>slideshow</td>
</tr>
<tr>
<td>Cualquier otra cosa</td>
<td>general-video</td>
</tr>
</table>
Se usó **motion-graphics** (categoría kinetic-type). Llega hasta unos 30 s sin narración, por eso sirvió también para la versión final. Esa ruta es autónoma: como mucho hace una pregunta.
## Paso 3. Conseguir el contenido de la marca
El entorno en la nube bloqueó `scalyai.dev` (política de red). Qué se hizo:
1. Se buscó la web con búsqueda y se sacaron los datos públicos: lema, herramientas que conecta, 2 semanas de implementación, ROI en 6 semanas, paquetes desde S/1.500, PyMEs de S/10k a S/500k al mes.
2. Se pidió una captura de la web a la persona y de ahí se sacó la identidad visual y el texto del botón ("Conversemos de tu próximo piloto · 30 minutos · sin tarjeta · sin compromiso").
<callout icon="💡" color="yellow_bg">
	Si quieres que Claude lea la web directamente: menú del entorno, Edit, Network access, y añade el dominio a los permitidos.
</callout>
## Paso 4. Sacar colores y tipografía de una captura
Sin acceso al sitio, los colores se miden en la imagen. Con `ffmpeg` se recorta una zona pequeña y se promedia a 1 píxel:
```bash
ffmpeg -v error -i captura.jpg -vf "crop=5:5:X:Y,scale=1:1" -f rawvideo -pix_fmt rgb24 - | od -An -tx1
```
Paleta resultante de ScalyAI:
<table header-row="true">
<tr>
<td>Uso</td>
<td>Color</td>
</tr>
<tr>
<td>Fondo crema</td>
<td>#F0F0E8</td>
</tr>
<tr>
<td>Titulares (azul marino)</td>
<td>#061A36</td>
</tr>
<tr>
<td>Acento (verde azulado)</td>
<td>#007A82</td>
</tr>
<tr>
<td>Texto secundario (gris pizarra)</td>
<td>#4F626B</td>
</tr>
<tr>
<td>Degradado del botón</td>
<td>#0E3A5E, #20748C, #42CFD2</td>
</tr>
</table>
Tipografía: **Manrope** (la que parece usar la web). Se descarga de `@fontsource/manrope` y se guardan los `.woff2` dentro del proyecto para que el render sea idéntico siempre.
```bash
npm pack @fontsource/manrope
```
<callout icon="⚠️" color="red_bg">
	**Error común:** el primer borrador se hizo con un fondo oscuro inventado. Antes de diseñar, pide la identidad real de la marca. Corregirlo después cuesta un render entero.
</callout>
## Paso 5. Crear el proyecto
```bash
npx hyperframes init videos/scalyai-intro --non-interactive --example=blank --skill=motion-graphics
```
Nunca hagas `init` en la raíz del repo ni dentro de otro proyecto. Estructura final:
```plain text
videos/scalyai-intro/
  index.html                  ← línea de tiempo principal (solo transiciones)
  shot-plan.json              ← plan del video (historia, escenas, paleta, tiempos)
  compositions/
    stage-bg.html             ← fondo en capas (luces, piso en perspectiva, anillos, polvo)
    scene-night.html          ← acto 1: la noche y el mensaje sin respuesta
    scene-auto-tasks.html     ← acto 2: del caos manual a las tareas que se hacen solas
    scene-tools.html          ← acto 2: celular con el chatbot respondiendo
    scene-workflow.html       ← acto 3: flujo de nodos conectados
    scene-dashboard.html      ← acto 4: panel de resultados
    scene-roi.html            ← acto 4: 2 semanas / ROI en 6
    brand-wipe.html           ← barrido de transición con el degradado de marca
    logo-fx.html              ← acto 5: ondas, destellos y botón de acción
    story-chrome.html         ← capítulos y barra de progreso
    components/               ← piezas del catálogo (logo-brand-close, headline-slam)
  assets/fonts/  assets/vendor/gsap.min.js
  renders/video.mp4  renders/video-compartir.mp4
```
## Paso 6. Definir la historia antes de diseñar
Con 30 s, apilar escenas bonitas no basta: se siente como un catálogo. Primero se decide un arco y un hilo conductor.
<table header-row="true">
<tr>
<td>Acto</td>
<td>Minutos</td>
<td>Qué cuenta</td>
</tr>
<tr>
<td>1. El problema</td>
<td>0 a 5 s</td>
<td>11:40 p. m.: un cliente escribe y nadie responde. Se pierde la venta.</td>
</tr>
<tr>
<td>2. El cambio</td>
<td>4,3 a 14,9 s</td>
<td>De día todo es manual, hasta que ScalyAI activa la automatización. El mismo mensaje de la noche ahora recibe respuesta en 2 s.</td>
</tr>
<tr>
<td>3. La automatización</td>
<td>14,4 a 20,1 s</td>
<td>El pedido #1042 recorre un solo flujo. "Mientras dormías, la venta se cerró."</td>
</tr>
<tr>
<td>4. El resultado</td>
<td>19,5 a 26,6 s</td>
<td>A la mañana todo se mide. Listo en 2 semanas, ROI medible en 6.</td>
</tr>
<tr>
<td>5. Tu turno</td>
<td>26,6 a 30 s</td>
<td>Logo, lema y "Conversemos de tu próximo piloto".</td>
</tr>
</table>
Reglas que dan coherencia:
- **Un mismo ejemplo de punta a punta:** el mensaje "¿tienen stock de la talla M?" y el pedido #1042 aparecen en la noche, en las tareas, en el chat y en el flujo.
- **Una apertura con un cierre:** lo que falla a las 11:40 p. m. se resuelve en el chat (con la hora 11:40 p. m. visible en el celular).
- **El color cuenta el cambio:** la noche es azul marino oscuro y el día usa la paleta clara de la marca. Entre ambos, un amanecer circular que sale de la luna.
- **Un hilo visible:** un chip de capítulo arriba a la izquierda y una barra de progreso inferior, con una marca por acto.
- **Lo ilustrativo se avisa:** las cifras inventadas llevan "Datos ilustrativos" en pantalla.
## Paso 7. Escribir el guion por escenas
Primero se decide el guion, después el código. Versión de 30 s:
<table header-row="true">
<tr>
<td>Tiempo</td>
<td>Escena</td>
<td>Texto en pantalla</td>
<td>Cómo aparece</td>
</tr>
<tr>
<td>0 a 5 s</td>
<td>Noche</td>
<td>11:40 p. m. / Un cliente escribe. / Nadie responde. / Ya le compró a otro.</td>
<td>Reloj que se voltea, notificación en 3D, contador de horas, sello VENTA PERDIDA</td>
</tr>
<tr>
<td>4,3 a 10,5 s</td>
<td>Tareas</td>
<td>De día, todo a mano. / Ahora, se hacen solas.</td>
<td>Caos con alertas, titular que cambia letra a letra, luz que marca las tareas con chispas</td>
</tr>
<tr>
<td>9,9 a 14,9 s</td>
<td>Chatbot</td>
<td>Conectamos tus herramientas</td>
<td>Celular que gira en 3D, burbujas de chat, insignias flotantes</td>
</tr>
<tr>
<td>14,4 a 20,1 s</td>
<td>Flujo</td>
<td>Un solo flujo. Cero copiar y pegar.</td>
<td>Plano que se levanta en 3D, nodos que se encienden con ondas</td>
</tr>
<tr>
<td>19,5 a 24,3 s</td>
<td>Panel</td>
<td>A la mañana, todo se mide.</td>
<td>Escritura con destello, tarjetas que se voltean, barras que rebotan</td>
</tr>
<tr>
<td>23,7 a 26,65 s</td>
<td>Promesa</td>
<td>Listo en 2 semanas. ROI medible en 6.</td>
<td>Entrada en 3D, dígitos tragamonedas, ondas de choque</td>
</tr>
<tr>
<td>26,6 a 30 s</td>
<td>Cierre</td>
<td>ScalyAI. + lema + botón de acción</td>
<td>Letras en cascada, destellos, botón que salta con resorte</td>
</tr>
</table>
Regla: **un movimiento dominante por escena**, y cada escena entra de forma distinta.
## Paso 8. Buscar piezas en el catálogo antes de programar
HyperFrames tiene cerca de 400 bloques listos. La regla es buscar primero y escribir a mano solo lo que no exista.
```bash
npx hyperframes catalog --query "kinetic typography word slam title" --json
npx hyperframes add logo-brand-close
```
Piezas usadas: `logo-brand-close` (cierre con logo) y `headline-slam` (primer gancho, ya reemplazado por la escena nocturna). Se guardan en `compositions/components/`. Todo lo demás se escribió a mano porque ningún bloque cubría esa historia.
## Paso 9. Construir la composición
Reglas del contrato que hay que respetar:
- Una sola línea de tiempo GSAP pausada por composición, registrada en `window.__timelines["id"]`, y terminar con `tl.seek(0)`.
- Cada elemento con tiempo lleva `class="clip"`, `data-start`, `data-duration` y un `id` único.
- Todo determinista: nada de `Math.random()`, `Date.now()` ni descargas de red al renderizar. Para el azar (letras, chispas, polvo) se usa un generador con semilla fija.
- Las escenas van como sub-composiciones (`data-composition-src`), con su contenido **dentro** de `<template>`.
- Los colores viven en un solo sitio (variables CSS en `:root`).
- Las escenas se solapan en el tiempo: la ranura de cada escena debe durar hasta que termine su transición de salida.
El `index.html` monta las escenas y solo anima las transiciones. Cada escena anima sus propios elementos. Encima de todo van dos capas: los efectos del cierre y el hilo de la historia.
## Paso 10. Transiciones entre escenas
Seis cortes, todos distintos, para que dos vecinos nunca se sientan igual:
<table header-row="true">
<tr>
<td>Corte</td>
<td>Transición</td>
</tr>
<tr>
<td>Noche a día</td>
<td>Amanecer: círculo de luz que crece desde la luna</td>
</tr>
<tr>
<td>Tareas a chatbot</td>
<td>Zoom que atraviesa (la escena crece y se desenfoca, la nueva se asienta)</td>
</tr>
<tr>
<td>Chatbot a flujo</td>
<td>Empuje lateral con desenfoque de movimiento</td>
</tr>
<tr>
<td>Flujo a panel</td>
<td>Círculo que crece desde el centro</td>
</tr>
<tr>
<td>Panel a promesa</td>
<td>Empuje hacia abajo</td>
</tr>
<tr>
<td>Promesa a logo</td>
<td>Barrido diagonal con el degradado del botón de la marca</td>
</tr>
</table>
Detalles clave:
- Si una escena tiene su propia animación de salida **y** la transición la mueve, se pelean. Quita la salida propia y deja que la transición sea la salida.
- Un reveal circular solo se nota si la escena que entra tiene fondo **opaco**. Se le pone un fondo propio que se desvanece medio segundo después, para que vuelva el fondo en capas.
## Paso 11. Transiciones de letras
Los títulos entran y salen letra por letra, cada escena con su propio estilo:
<table header-row="true">
<tr>
<td>Escena</td>
<td>Entrada</td>
<td>Salida</td>
</tr>
<tr>
<td>Noche (línea 1)</td>
<td>Ola: las letras suben con rebote</td>
<td>Se elevan y desaparecen</td>
</tr>
<tr>
<td>Noche (línea 2)</td>
<td>Máquina de escribir con destello cian</td>
<td>Se apagan de derecha a izquierda</td>
</tr>
<tr>
<td>Noche (línea 3)</td>
<td>Caen pesadas y rebotan</td>
<td>Se cubren con el amanecer</td>
</tr>
<tr>
<td>Tareas</td>
<td>Caen con inclinación aleatoria</td>
<td>Vuelan hacia arriba y se desenfocan, y entra el titular nuevo girando en 3D</td>
</tr>
<tr>
<td>Chatbot</td>
<td>Ola elástica</td>
<td>Se dispersan en todas direcciones</td>
</tr>
<tr>
<td>Flujo</td>
<td>Brotan desde el centro</td>
<td>Se voltean como paletas</td>
</tr>
<tr>
<td>Panel</td>
<td>Escritura con destello de color</td>
<td>Se hunden</td>
</tr>
<tr>
<td>Cierre</td>
<td>Cascada de letras y lema palabra por palabra</td>
<td>Se queda</td>
</tr>
</table>
Cómo se hace: una función divide el texto en palabras y letras (cada letra es un `span` en línea) y se anima cada una con un retraso calculado con el generador de semilla fija. Cambiar un titular letra a letra (de "todo a mano" a "se hacen solas") es un gran momento de historia.
## Paso 12. Cómo quitarle lo plano
- **Fondo en capas:** tres luces suaves que se desplazan por rutas distintas, un piso con cuadrícula en perspectiva que avanza hacia la cámara, anillos punteados que giran y 34 partículas que suben.
- **3D real:** tarjeta, celular y plano del flujo se inclinan con `rotationX` y `rotationY`, y flotan despacio. Se usa `transformPerspective` en cada elemento.
- **Cámara:** cada escena avanza un 3 a 5 % durante todo su tiempo, para que nunca haya un cuadro estático.
- **Profundidad entre capas:** insignias flotantes con rebote elástico, nodos adelantados en z, sombras en dos capas.
- **Energía:** ondas al encenderse cada nodo, chispas al marcar cada tarea, anillos de choque cuando aterriza el "6" y barras que rebotan al crecer.
- **Luz:** destello que cruza la tarjeta y el logo, y halo que late detrás del celular.
## Paso 13. El celular con el chatbot
Es HTML y CSS, no una foto. Así queda nítido y con los colores de la marca.
- Marco del celular (bordes redondeados, muesca), cabecera con el degradado de la marca y un hilo de mensajes.
- Es el **mismo mensaje de la noche**: la cabecera muestra "11:40 p. m." y bajo la respuesta aparece "Respondió en 2 segundos".
- Conversación: cliente pregunta por la talla M, el bot escribe (tres puntitos), responde que quedan 8 unidades, el cliente acepta y aparece el recibo **Pedido #1042 · CRM**.
- Cada burbuja sale desde la esquina de su colita (`transformOrigin`) con un rebote corto.
- Tamaño de letra grande (unos 29 px en el celular): en video se lee mucho peor que en pantalla.
## Paso 14. Las escenas de automatización
- **Tareas que se marcan solas:** una tarjeta con cinco tareas (copiar el pedido #1042 a Excel, responder, pasar al CRM, recordatorio de pago, reporte). Primero se ven pendientes, con alertas. Entra "ScalyAI activado" y una franja de luz las recorre: cada tarea se marca, su etiqueta pasa a "Automático" y salen chispas. El contador "Tiempo recuperado" llega a 12 h.
- **Flujo conectado:** cinco nodos (mensaje, IA, pedido en CRM, stock en Excel y ERP, aviso al equipo). Un punto de luz viaja entre ellos y va encendiendo cada uno. Hay una rama que dice "Si hay una duda, pasa a una persona".
- **Panel de resultados:** cuatro indicadores (18 h, 1.240 pedidos, 0 errores, 24/7), la hora "8:00 a. m." y un gráfico de horas manuales contra automatizadas por semana.
<callout icon="📌" color="yellow_bg">
	Las cifras de estas escenas son **ilustrativas**, no son de ScalyAI. Llevan el aviso "Datos ilustrativos" en pantalla. Los únicos datos reales son 2 semanas, ROI en 6 semanas y los textos de la web. Si tienes cifras de un cliente, se cambian y se quita el aviso.
</callout>
## Paso 15. Verificar antes de exportar
```bash
npx hyperframes check .
npx hyperframes snapshot --at 1.0,3.5,6.6,10.5,16,21,25,28 --no-end
```
- `check` revisa formato, tiempos, choques entre textos y contraste.
- `snapshot` saca fotogramas y hojas de contactos: **hay que mirarlas**. Varios errores (escenas pegadas arriba, huecos vacíos, texto que se tapa) solo se ven en la imagen.
- Los avisos informativos de texto fuera de pantalla a mitad de transición son normales.
## Paso 16. Exportar el MP4 y compartirlo
```bash
apt-get install -y ffmpeg        # si no está instalado
npx hyperframes render . --skill=motion-graphics -q high -o ./renders/video.mp4
ffprobe -v error -show_entries format=duration -of default=nw=1 renders/video.mp4
```
Se comprueba que el archivo exista, pese algo y dure lo esperado (30,0 s). El render de 30 s con todos los efectos tarda unos 3 minutos.
El archivo maestro pesa unos 31 MB y el envío por chat tiene un límite de 30 MB. Para compartir se hace una copia comprimida:
```bash
ffmpeg -i renders/video.mp4 -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -movflags +faststart -an renders/video-compartir.mp4
```
Queda en unos 7 MB con la misma resolución.
## Paso 17. Cómo se fue alargando
No se estira todo por igual. Se reparte el tiempo donde más hace falta.
- **De 10 a 12 s:** +1,4 s para el chat (los mensajes respiran y el último se lee), +0,3 s para el resultado y +0,3 s para el logo.
- **De 12 a 30 s:** se añadieron la noche, las tareas, el flujo y el panel. Se rehízo el reparto de tiempos con las escenas solapadas.
- Siempre se mueven a la vez: duración de la raíz, del fondo, de cada escena y los tiempos de las transiciones.
## Paso 17b. Poner el logo oficial
Primero se usó el nombre escrito porque no había logo. Después se subió la guía de identidad (un HTML con el logo, la paleta y la tipografía) y se pidió: "este es el logo de Scaly AI, reemplaza donde corresponda".
- **Cómo se leyó la guía:** el archivo venía empaquetado (recursos en base64 comprimidos). Se descomprimió con Python para sacar el SVG del logo, los colores y las reglas de uso.
- **El logo:** tres barras redondeadas (la de arriba con degradado #007B83 a #47D4D4, la del medio #007B83, la de abajo #041B3D) más "Scaly" en Manrope 800 y "AI" en peso 500 color #007B83. Sin punto final.
- **Dónde se reemplazó:** la escena de presentación de la marca (10 a 18 s) y el cierre (49 a 60 s), y también el cierre del video de 30 s. Las barras salen deslizándose desde la izquierda y después entran las letras.
- **Detalles:** el espacio entre "Scaly" y "AI" se hace con un elemento propio (un espacio suelto en flex se colapsa), y en el cierre se bajó el tamaño del logo al 60 % del ancho para que quepa junto al símbolo.
- **Pendiente:** la guía pide respetar estrictamente la identidad. Los colores del video se midieron de una captura (#061A36, #007A82, #42CFD2) y difieren un poco de los oficiales (#041B3D, #007B83, #47D4D4). Se pueden alinear.
## Paso 18. Voz en off (hecha con ElevenLabs)
Guion de unas 75 palabras para 30 s, uno por acto:
> **Acto 1:** Son las once y cuarenta de la noche. Un cliente pregunta por la talla M. Nadie responde.
> **Acto 2:** De día, todo es manual. Hasta que ScalyAI lo conecta, y ese mensaje recibe respuesta en segundos.
> **Acto 3:** Un solo flujo, sin copiar ni pegar. Mientras dormías, la venta se cerró.
> **Acto 4:** Por la mañana, todo se mide. Listo en dos semanas, retorno medible en seis.
> **Acto 5:** ScalyAI. Software e IA a la medida de tu negocio. Conversemos de tu próximo piloto.
**Cómo se hizo sin salir de Claude (versión de 60 s):** se usó una API de voz con la clave guardada como credencial del entorno. Claude nunca ve la clave: el sistema la añade a cada petición hacia el dominio permitido.
1. **Guion:** `videos/scalyai-60s/audio/guion-voz.txt` (124 palabras, una frase por tramo del video).
2. **Credencial:** en el menú del entorno, Edit, API credentials. Nombre de la credencial libre; sitio permitido `api.elevenlabs.io`; encabezado `xi-api-key` con prefijo vacío y la clave como valor. Para Gemini fue `generativelanguage.googleapis.com` con el encabezado `x-goog-api-key`. La credencial solo se carga en una sesión nueva.
3. **Voz:** `generar-voz-elevenlabs.sh` llama a la API con el modelo `eleven_multilingual_v2` en español. También quedó `generar-voz.sh` para Gemini TTS (probado con la voz Kore, dura 58,5 s).
4. **Elección:** se generaron dos voces predeterminadas de ElevenLabs (George y Sarah) y se eligió George.
5. **Ajuste:** se aceleró un 7 % con `ffmpeg atempo=1.07` (de 57,7 s a 53,9 s) para que termine antes del final del video.
6. **Montaje:** una etiqueta `<audio id="voz-en-off" src="audio/voz-george-1.07.wav" data-start="0.6" data-duration="54.0" data-track-index="6">` en el `index.html`. Todo `<audio>` necesita un `id`; sin él el render queda mudo.
7. **Render:** el video con voz tarda unos 8 a 9 minutos y se comprime con `-c:a aac -b:a 128k`.
<callout icon="⚠️" color="yellow_bg">
	Límites del plan gratuito de ElevenLabs: unos 10.000 caracteres al mes (cada versión del guion gasta unos 730), las voces de la biblioteca pública (por ejemplo "Jaider - Narration Spanish") dan error de pago por API, y el uso comercial normalmente exige un plan de pago. Confirma las condiciones vigentes en su web.
</callout>
Esta fue la primera versión (una sola pista de voz). La versión 2 la mejoró: ver el paso 18b.
Opciones:
<table header-row="true">
<tr>
<td>Opción</td>
<td>Requisito</td>
</tr>
<tr>
<td>Voz de HeyGen</td>
<td>CLI de HeyGen instalado y sesión iniciada con `heygen auth login --oauth` (abre el navegador, no se puede hacer desde la nube)</td>
</tr>
<tr>
<td>Voz propia</td>
<td>Grabar el guion y subir el audio</td>
</tr>
<tr>
<td>Gemini TTS</td>
<td>Clave de API de Google</td>
</tr>
<tr>
<td>Kokoro (local)</td>
<td>Descargar el modelo, puede estar bloqueado por la red</td>
</tr>
</table>
Estado: la página de instalación de HeyGen estaba bloqueada por la red del entorno. Camino más rápido: generar el MP3 en HeyGen, subirlo, y dejar que Claude lo sincronice con las escenas y vuelva a exportar.
## Paso 19. Copy para LinkedIn
Se pidió el texto promocional, luego con emojis, luego más interesante y sin mencionar el video, y por último se le pasó el humanizador. Versión final:
<details>
<summary>Ver el post final</summary>
	Son las 11:40 p.m. y un cliente escribe por WhatsApp 🌙: "¿Tienen la talla M?"
	Nadie le contesta hasta el día siguiente. Para entonces ya le compró a otro.
	Esto me lo cuentan casi todos los dueños de PyME con los que hablo, y casi siempre con la misma cara de resignación. Como si perder ventas de noche fuera parte del negocio.
	De día el problema cambia de forma. El pedido entra por WhatsApp, alguien lo copia a un Excel y otra persona lo vuelve a pasar al CRM. Cada vez que un dato se reescribe, alguien puede equivocarse (y alguien se equivoca).
	Por eso en Scaly AI hacemos software e IA a la medida ⚙️.
	Con un chatbot conectado, ese mensaje de las 11:40 p.m. termina así: el bot responde que quedan 8 unidades y ofrece reservar. El cliente dice que sí y el pedido aparece en el CRM. En la mañana tu equipo encuentra la venta cerrada y un café pendiente ☀️.
	No intentamos automatizar todo de golpe, porque eso suele terminar en proyectos que nunca salen. Empezamos por un solo proceso, lo dejamos funcionando en 2 semanas y medimos si vale la pena. La meta es ROI medible en 6 semanas 📈.
	Si estás pensando que tu negocio es muy chico para esto, trabajamos con PyMEs que facturan entre S/10k y S/500k al mes, con paquetes desde S/1.500.
	¿Tienes un proceso que tu equipo repite a mano todos los días? Cuéntamelo en una llamada de 30 minutos ☕. No te pido tarjeta ni ningún compromiso.
	👉 [scalyai.dev](http://scalyai.dev)
	#PyMEs #Automatizacion #WhatsAppBusiness
</details>
Cómo se llegó ahí: empezar con una escena concreta en vez de una afirmación, y quitar frases de remate y listas con emojis para que suene a persona. El post y el video cuentan la **misma historia** (11:40 p. m., la talla M, el pedido en el CRM), así que se refuerzan si se publican juntos. La frase en primera persona hay que confirmarla o cambiarla por algo que de verdad te pase.
## Paso 18b. Versión 2: voz por escena, sonido y menos efectos
Tras una crítica de dirección creativa se aplicaron cinco mejoras al video de 60 s (archivo `renders/video-v2-compartir.mp4`):
- **Voz por escena:** en vez de una sola pista, hay diez segmentos (`audio/segmentos.json`), cada uno con su texto, su hora de inicio y el tiempo máximo del hueco. `generar-segmentos.sh` los genera con ElevenLabs (voz George), mide cada uno y lo ajusta con `atempo` (nunca más de 1,3). Si un segmento no cabe, se acorta el texto en lugar de acelerarlo más. El script admite regenerar solo algunos (`./generar-segmentos.sh <voz> v9`). Cada segmento es una etiqueta `<audio>` con su `data-start`.
- **Pronunciación:** la voz leyendo "PyMEs" no sonaba bien. En el guion hablado se escribe "Pimes" (en pantalla sigue "PyMEs"). Regla: lo que se oye puede escribirse distinto a lo que se ve.
- **Música y efectos sintetizados** con ffmpeg (`audio/sonido.sh`, sin archivos de terceros): pad ambiental en cuatro acordes con pulso suave, "whoosh" en cada empuje, ascenso en los círculos, barrida larga antes del cierre y campanita al logo. Se mezclan como dos pistas `<audio>` (música a 0,9 y efectos a 0,5 de volumen). Es sonido sencillo; con una pista con licencia suena mejor.
- **Menos texto en pantalla:** se quitaron las descripciones bajo los tres pasos de "cómo trabajamos", para que la pantalla no repita lo que dice la voz.
- **Tres familias de transición** en lugar de nueve distintas: círculos de luz (cambios de tiempo: noche a día, flujo a panel), empujes (seis cortes a izquierda o hacia arriba) y el barrido de marca del cierre. Encima de cada empuje cruza el símbolo de las tres barras del logo (`compositions/sym-sting.html`).
- **Tipografía:** los textos pequeños subieron un 25 % (mínimo 28 px). Quedan chicos solo los de las maquetas internas (celular, tarjetas, panel).
- **Paleta oficial** de la guía de identidad: #041B3D, #007B83, #47D4D4, #F0F1E8 y #2F4560. Los degradados con texto blanco ya no terminan en cian claro, porque el contraste no pasaba.
Lección: la crítica (¿qué mejorarías?) se pide después de ver el video; la IA no lo ve de corrido, así que las impresiones de ritmo y sonido se confirman escuchándolo.
## Segundo caso: video promocional de Warmi Academy (50 s, voz de mujer)
Mismo método aplicado a otro cliente, partiendo de una grabación de pantalla de su web en lugar de una URL. Proyecto: `videos/warmi-promo/`. Resultado: `renders/warmi-promo-compartir.mp4` (11 MB, 1920×1080, 30 fps, con audio).
### Cómo se hizo
1. **Leer la grabación:** la grabación (un recorrido por la página, sin audio) se analizó con `ffprobe` y se sacaron fotogramas con `ffmpeg` cada 3 s y a tamaño completo en los momentos clave. De ahí salieron todos los datos reales: programa, resultados, público, módulos, fechas, precio y facilitador. Si algo no se vio completo en la grabación (por ejemplo la dirección web), no se inventa.
2. **Paleta y tipografía:** se midieron colores de la captura (violeta #5421A6 a rosa #D74AC5, fondo #FAF7FF) y se identificaron las fuentes (Space Grotesk para titulares y DM Sans para texto). Los `.woff2` se descargan de `@fontsource` con `npm pack` y se guardan en el proyecto.
3. **Guión en ocho escenas** (50 s): gancho, el programa, resultados, para quién es, módulos y sesiones, facilitador, precio y cierre con llamada a la acción.
4. **Voz de mujer:** ElevenLabs con la voz predeterminada Sarah (las voces de biblioteca no funcionan por API en el plan gratuito). Un segmento por escena, con el mismo script que el video de ScalyAI (`generar-segmentos.sh`).
5. **Ajuste de voz:** Sarah habla más lento que George. En la primera vuelta casi todas las frases pedían `atempo` 1,3 (sonaba apurado) y aun así no cabían. La solución fue acortar los textos y ampliar un poco los huecos, hasta quedar entre 1,0 y 1,18.
6. **Sonido:** la misma música y los mismos efectos sintetizados con ffmpeg (`audio/sonido.sh`), con los efectos puestos en las horas de las transiciones de este video.
7. **Transiciones:** dos familias, círculos de luz (apertura y final) y empujes (izquierda o arriba). Todas las escenas tienen elementos 3D que flotan y avance suave de cámara.
8. **Generación del código:** las escenas se escriben con un script de Python (`build/scenes.py` y `build/common.py`) que emite los HTML de cada sub-composición. Así, un cambio de texto o de estilo se aplica y se vuelve a generar en segundos.
### Errores nuevos de este caso
<table header-row="true">
<tr>
<td>Problema</td>
<td>Causa</td>
<td>Solución</td>
</tr>
<tr>
<td>`text_not_painted` en los titulares con degradado</td>
<td>Con `background-clip: text` en un padre, las letras separadas en `span` pierden el degradado y quedan transparentes</td>
<td>Al separar las letras, darle a cada una un color calculado por interpolación entre los extremos del degradado, y quitar el fondo del padre</td>
</tr>
<tr>
<td>Contraste insuficiente (2,93 a 1) en la última letra rosa</td>
<td>El extremo rosa del degradado era demasiado claro sobre fondo lila</td>
<td>Oscurecer el extremo del degradado hasta #B5249F</td>
</tr>
<tr>
<td>Titular repetido en el segundo 6</td>
<td>Se mostró una captura de la web cuyo texto era el mismo titular de la escena</td>
<td>Diseñar un gráfico propio en lugar de una captura: un anillo de progreso con el 8 y los ocho puntos de las semanas, con tres tarjetas con iconos</td>
</tr>
<tr>
<td>Voz acelerada hasta 1,3 y aún no cabe</td>
<td>El texto era demasiado largo para el hueco de la escena</td>
<td>Acortar el texto en vez de acelerar más (por encima de 1,2 suena apurado)</td>
</tr>
</table>
### Lección de este caso
- Una captura de la web dentro del video sirve para dar contexto, pero no debe repetir el texto que ya está escrito o dicho en esa escena. Si lo repite, es mejor un gráfico propio.
- Pedir una voz de mujer o de hombre cambia el ritmo: hay que ajustar los textos a esa voz.
### Prompt para un video promocional a partir de una grabación de pantalla
```plain text
Usa /hyperframes y crea un video promocional de unos 50 segundos para [NOMBRE DEL PRODUCTO], en español, 16:9 (1920×1080, 30 fps), con voz en off de [mujer/hombre], música de fondo suave y efectos de sonido.

=== MATERIAL ===
Adjunto una grabación de pantalla de la web (sin audio). Analízala con ffprobe y saca fotogramas con ffmpeg (cada 3 s y a tamaño completo en los momentos clave). De ahí sacas TODOS los datos reales: oferta, resultados, a quién va dirigido, fechas, precio y quién lo imparte. No inventes datos, y si falta algún dato (por ejemplo la dirección web o el WhatsApp), dímelo y no lo pongas.

=== MARCA ===
Mide los colores del fotograma (ffmpeg, recorte de 3×3 px a 1×1) y descubre las fuentes. Guárdalas en el proyecto (.woff2 de @fontsource con npm pack). Guarda también GSAP en el proyecto.

=== ESTRUCTURA (8 escenas) ===
1 gancho con el problema; 2 el programa (título y propuesta); 3 resultados; 4 para quién es; 5 módulos, fechas y qué incluye; 6 quién lo imparte; 7 precio; 8 cierre con llamada a la acción y fecha de inicio.
No repitas en una escena un texto que ya sale en una captura. Prefiere gráficos propios (anillos, tarjetas, iconos) y usa fotos solo si salen de mi material.

=== VOZ Y SONIDO ===
Una voz por escena con ElevenLabs (voz predeterminada, no de biblioteca), ajustada con atempo entre 1,0 y 1,2 como máximo: si no cabe, acorta el texto. Escribe los nombres como se pronuncian en el guión hablado (por ejemplo PyMEs como Pimes). Música y efectos sintetizados con ffmpeg.

=== TÉCNICA ===
Escenas como sub-composiciones con una línea de tiempo GSAP pausada cada una. Dos familias de transición (círculos y empujes). Letras separadas con color calculado si el texto tiene degradado. Contraste mínimo 4,5 a 1. Fija la versión: npx --yes hyperframes@0.8.96.

=== ENTREGA ===
Ejecuta hyperframes check, mira los fotogramas de cada escena antes de renderizar, renderiza, comprime una copia ligera (crf 24, aac 128k) y haz commit y push. Al terminar, dime qué datos usaste y cuáles faltaron.
```
## Errores que aparecieron y cómo se arreglaron
<table header-row="true">
<tr>
<td>Problema</td>
<td>Causa</td>
<td>Solución</td>
</tr>
<tr>
<td>`FFmpeg not found` al exportar</td>
<td>El contenedor no lo trae</td>
<td>`apt-get install -y ffmpeg`</td>
</tr>
<tr>
<td>`FFmpeg cannot start` una vez</td>
<td>Fallo temporal</td>
<td>Volver a lanzar el render</td>
</tr>
<tr>
<td>`gsap is not defined` en el render</td>
<td>El navegador del render no alcanza la CDN</td>
<td>Guardar GSAP dentro del proyecto (`assets/vendor/gsap.min.js`) y quitar las etiquetas de CDN</td>
</tr>
<tr>
<td>Escenas pegadas arriba de la pantalla</td>
<td>El contenedor de la escena no tenía tamaño</td>
<td>Darle `position: absolute; inset: 0`</td>
</tr>
<tr>
<td>Cuadro gris sobre un texto al hacer el brillo</td>
<td>La máscara de brillo cubría toda la caja</td>
<td>Aplicar el degradado al texto con `background-clip: text`</td>
</tr>
<tr>
<td>`root_missing_dimensions`</td>
<td>Faltaba `data-width` y `data-height` en la raíz de la sub-composición</td>
<td>Añadirlos</td>
</tr>
<tr>
<td>`font_family_without_font_face`</td>
<td>Se nombraba una fuente sin declarar su `@font-face`</td>
<td>Declarar `@font-face` con el `.woff2` local y no repetir el nombre en los respaldos</td>
</tr>
<tr>
<td>Lema pegado al logo</td>
<td>La cola de la letra y descendía sobre el texto</td>
<td>Más margen superior en el lema</td>
</tr>
<tr>
<td>Icono de verificación aplastado</td>
<td>El contenedor flex lo encogía</td>
<td>`flex: 0 0 26px` en el icono</td>
</tr>
<tr>
<td>Hueco vacío al entrar una escena</td>
<td>Sus elementos aparecían demasiado tarde y el titular anterior ya se había ido</td>
<td>Adelantar la entrada de los elementos para que lleguen con la transición</td>
</tr>
<tr>
<td>El reveal circular no se veía</td>
<td>La escena que entra era transparente</td>
<td>Darle un fondo opaco propio y desvanecerlo después</td>
</tr>
<tr>
<td>Dígitos del reloj cortados</td>
<td>La caja era más estrecha que el texto</td>
<td>Ensanchar la caja y bajar un poco el tamaño de letra</td>
</tr>
<tr>
<td>`content_overlap` entre el sello y la notificación</td>
<td>El sello está encima del mensaje a propósito</td>
<td>Marcarlo con `data-layout-allow-overlap`</td>
</tr>
<tr>
<td>Contraste bajo en textos grises</td>
<td>Gris demasiado claro sobre fondo claro</td>
<td>Oscurecer el gris hasta pasar 4,5 a 1</td>
</tr>
<tr>
<td>El MP4 pesa más de 30 MB y no se puede enviar</td>
<td>El render en alta calidad con muchos efectos pesa mucho</td>
<td>Hacer una copia comprimida con ffmpeg (crf 23)</td>
</tr>
<tr>
<td>Comprobación de permisos de la terminal falló</td>
<td>Fallo temporal del servidor</td>
<td>Reintentar; mientras tanto avanzar con archivos</td>
</tr>
<tr>
<td>No se puede leer [scalyai.dev](http://scalyai.dev)</td>
<td>Bloqueo de red del entorno</td>
<td>Permitir el dominio o dar una captura</td>
</tr>
<tr>
<td>El render falla con `E404 ... hyperframes-0.8.106.tgz`</td>
<td>`npx` intenta bajar una versión recién publicada que aún no está disponible</td>
<td>Fijar la versión: `npx --yes hyperframes@0.8.96 render ...`</td>
</tr>
<tr>
<td>`gsap_non_transform_motion` (letterSpacing, left)</td>
<td>Se animaron propiedades de diseño que saltan por píxeles enteros</td>
<td>Animar con transformaciones: `scaleX` en vez de `letterSpacing`, `x` en vez de `left`</td>
</tr>
<tr>
<td>Franja pálida que se queda a la derecha</td>
<td>El destello de luz termina su barrido pero sigue visible</td>
<td>Ponerlo invisible al empezar y desvanecerlo al terminar el barrido</td>
</tr>
<tr>
<td>El precio se ve como "1 .500"</td>
<td>La ventana de la cifra que gira es más ancha que el "1"</td>
<td>Margen negativo a la derecha de esa cifra</td>
</tr>
<tr>
<td>El MP4 de 60 s pesa unos 60 MB</td>
<td>Alta calidad con muchos efectos; GitHub avisa por encima de 50 MB</td>
<td>Subir solo lo necesario y compartir la copia de 12 MB (crf 24)</td>
</tr>
</table>
## Buenas prácticas que quedaron
- **Pide la identidad de marca primero**, antes de diseñar.
- **Define la historia antes que las escenas:** arco, ejemplo único, apertura que se cierra al final.
- **Que el color y la luz cuenten algo:** de la noche oscura al día claro.
- **Mira siempre los fotogramas**, no solo el resultado del `check`.
- **Guarda todo dentro del repo** (fuentes, GSAP, plan) para que se pueda volver a exportar en una sesión nueva.
- **Haz commit y push después de cada cambio importante**: el contenedor en la nube es temporal.
- **Un cambio por pedido**: colores, luego transiciones, luego entradas, luego celular, luego duración, luego historia. Se revisa y se exporta tras cada uno.
- **Tiempo de lectura:** en video, cada mensaje necesita casi un segundo completo en pantalla.
- **Avisa lo ilustrativo:** si una cifra no es real, que se vea escrito en pantalla.
## Los prompts, en orden
1. `npx skills add heygen-com/hyperframes`
2. `Using /hyperframes, make a 10-second product intro for http://scalyai.dev/ en español`
3. Usa los colores de la marca (con una captura de la web adjunta)
4. Mejora los efectos de pasada de fotograma
5. La forma en que aparecen los elementos sea distinta en cada parte
6. Incluye imágenes como un chatbot en un celular
7. Alarga el video a 12 segundos
8. Haz un copy para LinkedIn sobre la promoción del servicio, luego: con emojis, más interesante sin mencionar el video, y aplica humanizer
9. ¿En el video se puede colocar voz en off?
10. El video hazlo de 30 segundos, agrega frames de automatización
11. Juega con las transiciones al momento de pasar las letras
12. Juega con las animaciones, prueba diferentes y no lo hagas tan plano
13. Que tenga storytelling y coherencia
14. Una plantilla genérica de prompt para marcas (pidiendo antes qué mejoraría de mi prompt) y luego: "Hazlo con los datos de ScalyAI", que devolvió el guion y el storyboard de 60 s para aprobar, y "adelante" para construir (prompt 2)
15. Lo de la parte de arriba superior izquierda, no salga
16. Este es el logo de Scaly AI, reemplaza donde corresponda (con la guía de identidad adjunta)
17. Si deseo audio, ¿cómo lo haría sin salir de Claude? Después: "Haz la 3" (voz con API y credencial en el entorno), con Gemini primero y ElevenLabs después
18. "Usa la de George": montar la voz elegida en el video de 60 s y volver a renderizar
19. ¿Qué mejorarías del video? Después: mejoras 2 a 6 (sonido, voz sincronizada con menos texto, menos efectos, legibilidad y paleta oficial)
20. "PyMEs se pronuncia como pimes, corrige"
21. Adjunto de una grabación de pantalla de Warmi Academy: "ahora hacer un video promocionando esto, con voz de mujer"
22. "La parte del segundo 6 sale repetido" (se cambió la captura por un formulario, y luego por un gráfico propio)
23. "No coloca algo distinto, no un formulario, algo inventado" (gráfico diseñado: el anillo de 8 semanas)
## Dónde está el proyecto
- Repositorio: `jfernandez0296/animationclaude`
- Rama: `claude/heygen-hyperframes-skill-alphli`
- Proyecto: `videos/scalyai-intro/`
- Video final (maestro, unos 31 MB): `videos/scalyai-intro/renders/video.mp4`
- Copia para compartir (7 MB): `videos/scalyai-intro/renders/video-compartir.mp4`
- Versión de 60 s: `videos/scalyai-60s/` (completo de unos 55 MB en `renders/video.mp4`, copia de 12 MB en `renders/video-compartir.mp4`). Ambas versiones ya llevan el logo oficial. Con voz en off (George, ElevenLabs): `videos/scalyai-60s/renders/video-george-compartir.mp4` (13 MB, con audio) y el máster `video-george.mp4` (54 MB). Audios y scripts de voz en `videos/scalyai-60s/audio/`. Versión 2 (voz por escena, música, efectos, paleta oficial): `renders/video-v2-compartir.mp4` (14 MB) y el máster `video-v2.mp4` (55 MB).
- Promo de Warmi Academy (50 s, voz de mujer): `videos/warmi-promo/` con `renders/warmi-promo-compartir.mp4` (11 MB) y el máster `renders/warmi-promo.mp4` (42 MB). Las escenas se generan con `videos/warmi-promo/build/scenes.py`.