# main.py
# ESP32 WROOM – MicroPython 1.26+
# Unified WiFi manager + async web server
# AP config always available, even when STA is connected

import uasyncio as asyncio
import network
import socket
import machine
import time

# -------------------- CONFIG --------------------

AP_SSID = "WifiManager"
AP_PASS = "tayfunulu"
WIFI_FILE = "wifi.dat"
LED_PIN = 2
HTTP_PORT = 80

led = machine.Pin(LED_PIN, machine.Pin.OUT)

wlan_sta = network.WLAN(network.STA_IF)
wlan_ap = network.WLAN(network.AP_IF)

# -------------------- WIFI STORAGE --------------------

def load_wifi():
    """Read stored SSID/password from wifi.dat"""
    try:
        with open(WIFI_FILE) as f:
            ssid, pwd = f.read().strip().split(";")
            return ssid, pwd
    except Exception:
        return None, None


def save_wifi(ssid, password):
    """Store SSID/password in plaintext"""
    with open(WIFI_FILE, "w") as f:
        f.write("{};{}".format(ssid, password))

# -------------------- WIFI MANAGEMENT --------------------

async def connect_sta():
    """Attempt STA connection using stored credentials"""
    ssid, pwd = load_wifi()
    if not ssid:
        return False

    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return True

    print("Connecting to", ssid)
    wlan_sta.connect(ssid, pwd)

    for _ in range(50):  # ~5 seconds total
        if wlan_sta.isconnected():
            print("STA connected:", wlan_sta.ifconfig())
            return True
        await asyncio.sleep(0.1)

    print("STA connection failed")
    return False


def start_ap():
    """Start AP mode (always on)"""
    wlan_ap.active(True)
    wlan_ap.config(essid=AP_SSID, password=AP_PASS)
    print("AP active:", AP_SSID, "192.168.4.1")

# -------------------- HTTP HELPERS --------------------

def http_response(body, status="200 OK"):
    return (
        "HTTP/1.1 {}\r\n"
        "Content-Type: text/html\r\n"
        "Content-Length: {}\r\n"
        "Connection: close\r\n\r\n{}"
    ).format(status, len(body), body)


# -------------------- HTML PAGES --------------------

def page_clock():
    state = "ON" if led.value() else "OFF"
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: sans-serif;
                font-size: 1.2rem;
                padding: 1em;
            }}

            h1 {{
                font-size: 1.8rem;
            }}

            a {{
                display: block;
                font-size: 1.2rem;
                margin: 0.5em 0;
            }}
        </style>
    </head>
    <body>
        <h1>Clock Control</h1>
        <p>LED state: <b>{state}</b></p>
        <a href="/clock?led=on">ON</a>
        <a href="/clock?led=off">OFF</a>
        <a href="/apconfig">WiFi config</a>
    </body>
    </html>
    """

def page_apconfig(networks):
    radios = "".join(
        f'<input type="radio" name="ssid" value="{n}">{n}<br>'
        for n in networks
    )
    return f"""
    <html><body>
    <h1>WiFi setup</h1>
    <form method="POST">
    {radios}
    Password:<br>
    <input name="password" type="password"><br><br>
    <input type="submit" value="Save & Connect">
    </form>
    <a href="/clock">Back</a>
    </body></html>
    """

# -------------------- HTTP ROUTING --------------------

async def handle_client(reader, writer):
    try:
        request = await reader.read(1024)
        if not request:
            return

        request = request.decode()
        line = request.split("\r\n")[0]
        method, path, _ = line.split()

        # ---- /clock ----
        if path.startswith("/clock"):
            if "led=on" in path:
                led.value(1)
            elif "led=off" in path:
                led.value(0)

            body = page_clock()
            writer.write(http_response(body))

        # ---- /apconfig ----
        elif path.startswith("/apconfig"):
            if method == "POST":
                try:
                    data = request.split("\r\n\r\n", 1)[1]
                    ssid = data.split("ssid=")[1].split("&")[0]
                    pwd = data.split("password=")[1]
                    save_wifi(ssid, pwd)
                    await connect_sta()
                except Exception:
                    pass

            nets = [n[0].decode() for n in wlan_sta.scan()]
            body = page_apconfig(nets)
            writer.write(http_response(body))

        # ---- default ----
        else:
            writer.write(http_response(page_clock()))

        await writer.drain()

    except Exception as e:
        print("HTTP error:", e)
    finally:
        await writer.aclose()

# -------------------- BACKGROUND TASK STUBS --------------------
# Add your future tasks here safely

async def clock_task():
    while True:
        # update clock LEDs here
        await asyncio.sleep(1)


async def seconds_led_task():
    while True:
        # blink seconds LED here
        await asyncio.sleep(1)


# -------------------- MAIN --------------------

async def main():
    wlan_sta.active(True)
    start_ap()
    await connect_sta()

    asyncio.create_task(clock_task())
    asyncio.create_task(seconds_led_task())

    server = await asyncio.start_server(handle_client, "0.0.0.0", HTTP_PORT)
    print("HTTP server running on port", HTTP_PORT)

    await server.wait_closed()


asyncio.run(main())
