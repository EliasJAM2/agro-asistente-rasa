import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionAsesoriaRiego(Action):
    def name(self) -> Text:
        return "action_asesoria_riego"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        cultivo = tracker.get_slot('cultivo').lower()
        etapa_cruda = (tracker.get_slot('etapa_cultivo') or "").lower()

       
        etapa = etapa_cruda.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

        plan = {
            "arroz": {
                "germinacion": "🌱 Riego: Suelo saturado, no inundado profundamente. Cuidado: Controla la Mosquilla y evita pudrición de raíz.",
                "vegetativo": "🌿 Riego: Lámina de agua estable de 5 a 10 cm. Cuidado: Realiza el rameo para Novia del Arroz y abona con Nitrógeno.",
                "floracion": "🚨 ¡FASE CRÍTICA! Lámina de agua constante para llenado de granos. Vigila espigas blancas.",
                "cosecha": "✂️ Realiza la 'seca' 15 a 20 días antes de cortar para endurecer el grano."
            },
            "papa": {
                "germinacion": "💧 Riego: Ligero o machaco previo. Evita excesos que pudran la semilla. Cuidado: Gorgojo de los Andes.",
                "vegetativo": "🌿 Riego: Frecuentes pero cortos. Cuidado: Aporque alto para proteger de la polilla.",
                "floracion": "🌸 Mayor demanda hídrica. Si falta agua, las papas quedarán pequeñas. Cuidado: Tizón tardío.",
                "cosecha": "🚚 Suspender riego 15 días antes para que la piel endurezca. Selecciona papas sanas."
            },
            "cebolla": {
                "germinacion": "💧 Riegos diarios tras trasplante para asentar raíz. Usa enraizadores.",
                "vegetativo": "🌿 Riegos uniformes. Sensible al estrés hídrico. Control de Trips.",
                "bulbo": "🧅 Riego constante para evitar bulbos deformes. Vigila Raíz Rosada.",
                "cosecha": "✂️ Cortar agua 10 días antes. Realiza el doblado de hojas para maduración."
            },
            "ajo": {
                "germinacion": "🌱 Riego inicial ligero. Desinfecta la semilla con nematicida.",
                "vegetativo": "🌿 Riego por gravedad controlado. Evita anegamientos para no pudrir el cuello.",
                "floracion": "🌸 Mantener humedad para diferenciación de dientes. Vigila Mosca del Ajo.",
                 "cosecha": "✂️ Retirar agua cuando 50% de planta esté amarilla. Curado bajo sombra."
            },
            "maiz": {
                "germinacion": "💧 Riego para asegurar uniformidad. Controla gusanos cortadores.",
                "vegetativo": "🌿 Riego normal. No debe faltar urea. Aplica preventivo contra cogollero.",
                "floracion": "🚨 ETAPA CRÍTICA. Sin agua reduces 20% de producción. Revisa entrada de gusano elotero.",
                "cosecha": "🚚 Espaciar riegos hasta cortar con grano duro. Evita humedad para prevenir hongos."
            }
        }

        # Búsqueda flexible de etapa para cebolla
        if "floracion" in etapa or "bulbo" in etapa:
            etapa_buscar = "bulbo" if "cebolla" in cultivo else "floracion"
        elif "siembra" in etapa or "brotacion" in etapa:
            etapa_buscar = "germinacion"
        else:
            etapa_buscar = etapa

        # Obtener mensaje
        mensaje = plan.get(cultivo, {}).get(etapa_buscar, f"Lo siento, elige entre: germinación, vegetativo, floración o cosecha (Escribiste: {etapa_cruda}).")
        
        dispatcher.utter_message(text=mensaje)
        return []

class ActionPestDiagnostic(Action):
    def name(self) -> Text:
        return "action_pest_diagnostic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extraer slots y normalizar a minúsculas
        cultivo = (tracker.get_slot('cultivo') or "").lower()
        hoja = (tracker.get_slot('sintoma_hoja') or "").lower()
        raiz_fruto = (tracker.get_slot('sintoma_raiz_fruto') or "").lower()

        # Mensaje por defecto si no hay coincidencia
        res = f"Para tu cultivo de {cultivo}, no logré identificar la plaga exacta con esos síntomas. Intenta describiendo solo el color o el daño principal (ej: rosado, gusanos, huecos)."

        # --- 1. ARROZ ---
        if "arroz" in cultivo:
            if "blanca" in hoja or "seca" in hoja or "vacia" in hoja:
                res = "🍚Identificado: NOVIA DEL ARROZ. Solución: Realiza el 'chicoteo' (pasar ramas sobre el cultivo) para derribar larvas al agua."
            elif "mina" in hoja or "caminito" in hoja or "gris" in hoja:
                res = "🍚Identificado: MOSQUILLA DE LOS ALMÁCIGOS. Solución: Bajar el nivel de la lámina de agua en el almácigo para exponer larvas."

        # --- 2. PAPA ---
        elif "papa" in cultivo:
            if "agujero" in raiz_fruto or "suciedad" in raiz_fruto or "mina" in hoja:
                res = "🥔Identificado: POLILLA DE LA PAPA. Solución: Realiza un 'aporque' alto y compacto para proteger los tubérculos de la puesta de huevos."
            elif "larva" in raiz_fruto or "escarabajo" in hoja or "c" in raiz_fruto:
                res = "🥔Identificado: GORGOJO DE LOS ANDES. Solución: Colocación de barreras de plástico alrededor del campo para evitar el ingreso del insecto."

        # --- 3. CEBOLLA ---
        elif "cebolla" in cultivo:
            if "plata" in hoja or "plateada" in hoja or "brillante" in hoja:
                res = "🧅 Identificado: TRIPS. Solución: Aplicaciones de Spinosad o insecticidas a base de aceite de neem, rotando ingredientes."
        elif "rosada" in raiz_fruto or "púrpura" in raiz_fruto or "rojo" in raiz_fruto:
                res = "🧅 Identificado: RAÍZ ROSADA. Prevención: Solarización de suelos y rotación estricta de cultivos (no sembrar cebolla en 4-5 años)."
        # --- 4. AJO ---
        elif "ajo" in cultivo:
            if "gusano" in raiz_fruto or "blanco" in raiz_fruto or "marchita" in hoja:
                res = "🧄Identificado: MOSCA DEL AJO. Solución: Eliminación de residuos de cosecha y uso de trampas pegajosas amarillas."
            elif "retorcida" in hoja or "hinchada" in hoja or "esponjoso" in raiz_fruto:
                res = "🧄Identificado: NEMATODO DEL TALLO. Solución: Inmersión de los dientes de ajo en agua a 50°C por 20 minutos antes de sembrar."

        # --- 5. MAÍZ ---
        elif "maiz" in cultivo or "maíz" in cultivo:
            if "cogollo" in hoja or "aserrín" in hoja or "hueco" in hoja:
                res = "🌽Identificado: GUSANO COGOLLERO. Solución: Liberación de avispitas Trichogramma o aplicación de Bacillus thuringiensis en el cogollo."
            elif "mazorca" in raiz_fruto or "punta" in raiz_fruto or "grano" in raiz_fruto:
                res = "🌽Identificado: GUSANO DE LA MAZORCA. Solución: Aplicar una gota de aceite mineral en la 'barba' del maíz al secarse."

        dispatcher.utter_message(text=res)
        return []
    

class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text').lower()
        distrito = "Arequipa"
        
        # NUEVA LISTA DE 8 ZONAS FUNCIONALES
        zonas = ["camana", "islay", "yura", "la campiña", "santa rita", "la joya", "mollendo", "chuquibamba"]
        for z in zonas:
            if z in user_msg:
                distrito = z
                break

        api_key = "5b06cededa38a63021187b50754c4184"
        
        # Mapeo Simplificado para Respuesta Inmediata
        if distrito == "la campiña":
            busqueda = "Arequipa,PE"
        elif distrito == "santa rita":
            busqueda = "Santa Rita de Siguas,PE"
        else:
            busqueda = f"{distrito},PE"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={busqueda}&appid={api_key}&units=metric&lang=es"
        
        try:
            r = requests.get(url).json()
            if r.get("cod") != 200:
                raise Exception("Zona no encontrada")

            temp = r['main']['temp']
            hum = r['main']['humidity']
            clima_desc = r['weather'][0]['description'].lower()
            main_clima = r['weather'][0]['main'].lower()

            # Lógica dinámica para las consultas
            if "soleado" in user_msg or "sol" in user_msg:
                if "clear" in main_clima or "clear" in clima_desc:
                    msg = f"☀️Sí, estará soleado en {distrito.capitalize()} con una temperatura de {temp}°C."
                else:
                    msg = f"☁️No, el cielo en {distrito.capitalize()} estará {clima_desc} con una humedad del {hum}%."
            elif "lluvia" in user_msg or "llover" in user_msg:
                if "rain" in main_clima or "drizzle" in main_clima:
                    msg = f"☔ Sí, se esperan lluvias en {distrito.capitalize()} hoy. Toma tus precauciones."
                else:
                    msg = f"🌤️No se esperan lluvias en {distrito.capitalize()}, el cielo está {clima_desc}."
            elif "frío" in user_msg or "temperatura" in user_msg:
                alerta = " 🥶⚠️🥶 ¡Cuidado con las heladas!" if temp < 6 else ""
                msg = f"🌡️En {distrito.capitalize()} la temperatura es de {temp}°C.{alerta}"
            else:
                msg = f"El reporte para {distrito.capitalize()} indica: {clima_desc.capitalize()}, con {temp}°C y {hum}% de humedad."

        except:
            msg = f"🌐 Lo siento, no pude obtener el clima de {distrito}. Intenta con otra zona como Mollendo o Yura."

        dispatcher.utter_message(text=msg)
        return []
    