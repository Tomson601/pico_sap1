from machine import Pin, SPI
from time import sleep
import framebuf

class Nokia5110:
    def __init__(self):
        self.sck = Pin(2)    # GPIO2 - SCK
        self.mosi = Pin(3)   # GPIO3 - MOSI
        self.dc = Pin(4)     # GPIO4 - Data/Command
        self.rst = Pin(5)    # GPIO5 - Reset
        self.cs = Pin(6)     # GPIO6 - Chip Select
        self.led = Pin(7, Pin.OUT)  # GPIO7 - Podświetlenie

        self.spi = SPI(0, baudrate=500000, polarity=0, phase=0, sck=self.sck, mosi=self.mosi)
        self.dc.init(self.dc.OUT)
        self.rst.init(self.rst.OUT)
        self.cs.init(self.cs.OUT)
        self.led.value(1)  # Domyślnie podświetlenie włączone

        self.width = 84
        self.height = 48
        self.buffer = bytearray((self.width * self.height) // 8)
        self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)

        self.reset()
        self.init_display()
    
    def set_backlight(self, state):
        """ Włącza lub wyłącza podświetlenie (1 = ON, 0 = OFF) """
        self.led.value(state)

    def reset(self):
        self.rst.value(0)
        sleep(0.1)
        self.rst.value(1)

    def init_display(self):
        self.command(0x21)  # Tryb rozszerzony
        self.command(0xBF)  # Ustawienie kontrastu (spróbuj 0xBF jeśli ekran jest blady)
        self.command(0x04)  # Regulacja temperatury
        self.command(0x13)  # Bias mode (0x13 często działa lepiej niż 0x14)
        self.command(0x20)  # Tryb podstawowy
        self.command(0x0C)  # Tryb normalny

    def command(self, cmd):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def data(self, data_bytes):
        self.dc.value(1)
        self.cs.value(0)
        if isinstance(data_bytes, int):  # Jeśli pojedyncza liczba, konwertuj na bajt
            data_bytes = bytearray([data_bytes])
        self.spi.write(data_bytes)
        self.cs.value(1)

    def clear(self):
        self.fb.fill(0)
        self.show()

    def show(self):
        self.command(0x40)  # Ustawienie początku rzędu
        self.command(0x80)  # Ustawienie początku kolumny
        for i in range(0, len(self.buffer), self.width):
            self.dc.value(1)  # Przełączenie w tryb danych
            self.cs.value(0)
            self.spi.write(self.buffer[i:i+self.width])  # Wysłanie danych
            self.cs.value(1)


    def draw_text(self, x, y, text):
        self.fb.text(text, x, y, 1)

    def update_display(self, pc, ir, a, out):
        """ Aktualizacja ekranu z wartościami rejestrów """
        self.clear()
        self.draw_text(0, 0, f"PC:  {pc:04b}")
        self.draw_text(0, 10, f"IR:  {ir:08b}")
        self.draw_text(0, 20, f"A:   {a:08b}")
        self.draw_text(0, 30, f"OUT: {out:08b}")
        self.show()
