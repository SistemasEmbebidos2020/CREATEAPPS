from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from jnius import autoclass, cast
from android.permissions import request_permissions, Permission
import threading

# Tamaño ventana
Window.size = (360, 800)

# Clases Java para BLE
PythonJavaClass = autoclass('org.kivy.android.PythonJavaClass')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothManager = autoclass('android.bluetooth.BluetoothManager')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothGatt = autoclass('android.bluetooth.BluetoothGatt')
BluetoothGattCallback = autoclass('android.bluetooth.BluetoothGattCallback')
Context = autoclass('android.content.Context')
UUID = autoclass('java.util.UUID')
ParcelUuid = autoclass('android.os.ParcelUuid')

# UUIDs
SERVICE_UUID = "12345678-1234-1234-1234-123456789abc"
CHARACTERISTIC_UUID = "abcdef01-1234-1234-1234-123456789abc"


class BLEManager:
    def __init__(self, callback):
        self.callback = callback
        self.adapter = None
        self.gatt = None
        self.device = None
        self.characteristic = None
        self.is_connected = False
        self.init_bluetooth()

    def init_bluetooth(self):
        try:
            activity = PythonActivity.mActivity
            context = cast(activity, Context)
            manager = context.getSystemService("bluetooth")
            self.adapter = manager.getAdapter()
        except Exception as e:
            print(f"Error inicializando Bluetooth: {e}")

    def start_scan(self):
        """Escanea dispositivos BLE disponibles"""
        if not self.adapter:
            self.callback("error", "Bluetooth no disponible")
            return

        try:
            self.adapter.startDiscovery()
            self.callback("scanning", "Buscando dispositivos...")
            Clock.schedule_once(lambda dt: self.check_devices(), 3)
        except Exception as e:
            self.callback("error", f"Error escaneo: {e}")

    def check_devices(self):
        """Verifica dispositivos encontrados"""
        try:
            bonded = self.adapter.getBondedDevices()
            for device in bonded:
                if device.getName() == "Chaleco_Masajeador":
                    self.connect(device)
                    return
            self.callback("error", "No se encontró Chaleco_Masajeador")
        except Exception as e:
            self.callback("error", f"Error: {e}")

    def connect(self, device):
        """Conecta a un dispositivo BLE"""
        try:
            self.device = device
            self.callback("connecting", f"Conectando a {device.getName()}...")
            
            # Simular conexión (en un app real usarías BluetoothGatt)
            Clock.schedule_once(lambda dt: self._simulate_connection(), 1)
        except Exception as e:
            self.callback("error", f"Error conexión: {e}")

    def _simulate_connection(self):
        """Simula conexión exitosa"""
        self.is_connected = True
        self.callback("connected", "Conectado a Chaleco_Masajeador")

    def send_command(self, cmd):
        """Envía comando BLE"""
        if not self.is_connected:
            self.callback("error", "No conectado")
            return

        try:
            # En Android real, usarías:
            # self.characteristic.setValue(cmd.encode())
            # self.gatt.writeCharacteristic(self.characteristic)
            
            # Para testing, solo imprimimos
            print(f"Enviando: {cmd}")
            self.callback("sent", f"Comando enviado: {cmd}")
        except Exception as e:
            self.callback("error", f"Error enviando: {e}")

    def disconnect(self):
        """Desconecta del dispositivo"""
        try:
            if self.gatt:
                self.gatt.disconnect()
                self.gatt.close()
            self.is_connected = False
            self.callback("disconnected", "Desconectado")
        except Exception as e:
            self.callback("error", f"Error desconectando: {e}")


class RoundButton(Widget):
    """Botón circular personalizado para ON/OFF"""
    def __init__(self, is_on=False, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.is_on = is_on
        self.callback = callback
        self.bind(size=self.update_canvas)
        self.draw_circle()

    def update_canvas(self, *args):
        self.canvas.clear()
        self.draw_circle()

    def draw_circle(self):
        with self.canvas:
            # Color según estado
            if self.is_on:
                Color(0.2, 0.8, 0.2, 1)  # Verde
            else:
                Color(0.6, 0.6, 0.6, 1)  # Gris

            # Círculo
            Ellipse(pos=self.pos, size=self.size)

            # Borde
            Color(1, 1, 1, 0.3)
            Line(ellipse=(self.pos[0], self.pos[1], self.size[0], self.size[1]),
                 width=2)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.callback:
            self.is_on = not self.is_on
            self.draw_circle()
            self.callback()
            return True
        return super().on_touch_down(touch)


class ChalecosApp(App):
    def build(self):
        # Solicitar permisos
        self.request_permissions()

        # BLE Manager
        self.ble = BLEManager(self.on_ble_event)

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título
        title = Label(
            text='[b]Chaleco Masajeador[/b]\n[size=12]Pensando en tu bienestar[/size]',
            markup=True,
            size_hint_y=0.1,
            font_size='20sp'
        )
        main_layout.add_widget(title)

        # Estado de conexión
        self.status_label = Label(
            text='[color=ff0000]Desconectado[/color]',
            markup=True,
            size_hint_y=0.08,
            font_size='14sp'
        )
        main_layout.add_widget(self.status_label)

        # Botones conexión
        connection_layout = BoxLayout(size_hint_y=0.08, spacing=10)
        self.connect_btn = Button(
            text='Conectar',
            background_color=(0.2, 0.6, 1, 1),
            size_hint_x=0.5
        )
        self.connect_btn.bind(on_press=self.on_connect_press)
        connection_layout.add_widget(self.connect_btn)

        self.disconnect_btn = Button(
            text='Desconectar',
            background_color=(1, 0.3, 0.3, 1),
            size_hint_x=0.5,
            disabled=True
        )
        self.disconnect_btn.bind(on_press=self.on_disconnect_press)
        connection_layout.add_widget(self.disconnect_btn)
        main_layout.add_widget(connection_layout)

        # Botón ON/OFF (circular)
        self.power_button = RoundButton(
            is_on=False,
            callback=self.on_power_toggle,
            size_hint_y=0.2
        )
        main_layout.add_widget(self.power_button)

        # Botón texto encima
        on_off_label = Label(
            text='[b]OFF[/b]',
            markup=True,
            size_hint_y=0.08,
            font_size='24sp'
        )
        self.on_off_label = on_off_label
        main_layout.add_widget(on_off_label)

        # ScrollView para sliders
        scroll = ScrollView(size_hint=(1, 0.5))
        sliders_layout = GridLayout(cols=1, spacing=20, size_hint_y=None, padding=10)
        sliders_layout.bind(minimum_height=sliders_layout.setter('height'))

        # Slider Cervical
        cervical_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        cervical_label = Label(text='[b]Cervical[/b]: 0%', markup=True, size_hint_y=0.3, font_size='14sp')
        self.cervical_label = cervical_label
        cervical_slider = Slider(min=0, max=100, value=0, size_hint_y=0.7)
        self.cervical_slider = cervical_slider
        cervical_slider.bind(value=self.on_cervical_change)
        cervical_box.add_widget(cervical_label)
        cervical_box.add_widget(cervical_slider)
        sliders_layout.add_widget(cervical_box)

        # Slider Dorsal
        dorsal_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        dorsal_label = Label(text='[b]Dorsal[/b]: 0%', markup=True, size_hint_y=0.3, font_size='14sp')
        self.dorsal_label = dorsal_label
        dorsal_slider = Slider(min=0, max=100, value=0, size_hint_y=0.7)
        self.dorsal_slider = dorsal_slider
        dorsal_slider.bind(value=self.on_dorsal_change)
        dorsal_box.add_widget(dorsal_label)
        dorsal_box.add_widget(dorsal_slider)
        sliders_layout.add_widget(dorsal_box)

        # Slider Lumbar
        lumbar_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        lumbar_label = Label(text='[b]Lumbar[/b]: 0%', markup=True, size_hint_y=0.3, font_size='14sp')
        self.lumbar_label = lumbar_label
        lumbar_slider = Slider(min=0, max=100, value=0, size_hint_y=0.7)
        self.lumbar_slider = lumbar_slider
        lumbar_slider.bind(value=self.on_lumbar_change)
        lumbar_box.add_widget(lumbar_label)
        lumbar_box.add_widget(lumbar_slider)
        sliders_layout.add_widget(lumbar_box)

        scroll.add_widget(sliders_layout)
        main_layout.add_widget(scroll)

        # Estado de los sliders
        self.is_on = False
        self.update_slider_states()

        return main_layout

    def request_permissions(self):
        """Solicita permisos necesarios para BLE"""
        permissions = [
            Permission.BLUETOOTH,
            Permission.BLUETOOTH_ADMIN,
            Permission.BLUETOOTH_SCAN,
            Permission.BLUETOOTH_CONNECT,
            Permission.ACCESS_FINE_LOCATION,
        ]
        request_permissions(permissions)

    def on_ble_event(self, event_type, message):
        """Callback para eventos BLE"""
        print(f"BLE Event: {event_type} - {message}")
        
        if event_type == "connected":
            self.status_label.text = '[color=00ff00]Conectado[/color]'
            self.connect_btn.disabled = True
            self.disconnect_btn.disabled = False
        elif event_type == "disconnected":
            self.status_label.text = '[color=ff0000]Desconectado[/color]'
            self.connect_btn.disabled = False
            self.disconnect_btn.disabled = True
            self.is_on = False
            self.power_button.is_on = False
            self.power_button.draw_circle()
            self.on_off_label.text = '[b]OFF[/b]'
            self.update_slider_states()
        elif event_type == "error":
            self.status_label.text = f'[color=ffff00]{message}[/color]'

    def on_connect_press(self, instance):
        """Botón Conectar presionado"""
        self.ble.start_scan()

    def on_disconnect_press(self, instance):
        """Botón Desconectar presionado"""
        self.ble.disconnect()

    def on_power_toggle(self):
        """Botón ON/OFF presionado"""
        if not self.ble.is_connected:
            self.status_label.text = '[color=ff0000]No conectado[/color]'
            self.power_button.is_on = False
            self.power_button.draw_circle()
            return

        self.is_on = self.power_button.is_on
        self.on_off_label.text = '[b]ON[/b]' if self.is_on else '[b]OFF[/b]'
        
        if self.is_on:
            self.ble.send_command('O' if not self.is_on else 'A')
        else:
            self.ble.send_command('O')
        
        self.update_slider_states()

    def update_slider_states(self):
        """Habilita/deshabilita sliders según estado ON/OFF"""
        self.cervical_slider.disabled = not self.is_on
        self.dorsal_slider.disabled = not self.is_on
        self.lumbar_slider.disabled = not self.is_on

    def pwm_to_command(self, zone, percent):
        """Convierte porcentaje a comando BLE"""
        if percent == 0:
            commands = {'cervical': 'c', 'dorsal': 'd', 'lumbar': 'l'}
        elif percent <= 33:
            commands = {'cervical': 'A', 'dorsal': 'D', 'lumbar': 'G'}
        elif percent <= 66:
            commands = {'cervical': 'B', 'dorsal': 'E', 'lumbar': 'H'}
        else:
            commands = {'cervical': 'C', 'dorsal': 'F', 'lumbar': 'I'}
        return commands.get(zone, '')

    def on_cervical_change(self, instance, value):
        """Slider Cervical cambió"""
        self.cervical_label.text = f'[b]Cervical[/b]: {int(value)}%'
        if self.is_on:
            cmd = self.pwm_to_command('cervical', value)
            self.ble.send_command(cmd)

    def on_dorsal_change(self, instance, value):
        """Slider Dorsal cambió"""
        self.dorsal_label.text = f'[b]Dorsal[/b]: {int(value)}%'
        if self.is_on:
            cmd = self.pwm_to_command('dorsal', value)
            self.ble.send_command(cmd)

    def on_lumbar_change(self, instance, value):
        """Slider Lumbar cambió"""
        self.lumbar_label.text = f'[b]Lumbar[/b]: {int(value)}%'
        if self.is_on:
            cmd = self.pwm_to_command('lumbar', value)
            self.ble.send_command(cmd)


if __name__ == '__main__':
    ChalecosApp().run()
