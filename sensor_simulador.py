import time
import json
import random
import paho.mqtt.client as mqtt

# Datos de conexión de EMQX Cloud
BROKER = "v7611a93.ala.us-east-1.emqxsl.com"
PORT = 8883
USER = "vinossensor"
PASSWORD = "vinos2026"
TOPIC_BASE = "vinosparry/bodega01"

def on_connect(client, userdata, flags, reason_code, properties):
    if not reason_code.is_failure:
        print("[+] Conexión exitosa a EMQX Cloud (TLS, puerto 8883)")
        client.subscribe(f"{TOPIC_BASE}/#")
        print(f"[+] Suscrito a {TOPIC_BASE}/#")
    else:
        print(f"[-] Error de conexión: {reason_code}")

def on_message(client, userdata, msg):
    print(f"[Recibido desde el broker] {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Codespaces_VinosParry")
client.username_pw_set(USER, PASSWORD)
client.tls_set()  # usa los certificados del sistema (TLS)

client.on_connect = on_connect
client.on_message = on_message

print("Conectando con EMQX Cloud...")
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

try:
    while True:
        lecturas = {
            "sensor01/temperatura": round(random.uniform(12.0, 18.0), 2),
            "sensor02/humedad": round(random.uniform(60.0, 80.0), 2),
            "sensor03/co2": round(random.uniform(400, 1200), 1),
            "sensor04/presion": round(random.uniform(1008.0, 1015.0), 2),
        }
        for sub_topic, valor in lecturas.items():
            full_topic = f"{TOPIC_BASE}/{sub_topic}"
            payload = json.dumps({"valor": valor, "timestamp": time.time()})
            client.publish(full_topic, payload)
            print(f"[Publicado] {full_topic} -> {payload}")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nSimulación detenida.")
    client.loop_stop()
    client.disconnect()