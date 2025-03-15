from sap1 import SAP1
from nokia5110 import Nokia5110
import machine, time

# Konfiguracja fizycznego wejścia zegara
clock_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Zegar na GPIO15

# Inicjalizacja wyświetlacza
display = Nokia5110()

# Program dla SAP-1
program = [
    0b00010001,  # LDA 1  (Załaduj wartość z RAM[1] do akumulatora)
    0b00100010,  # ADD 2  (Dodaj wartość z RAM[2] do akumulatora)
    0b11100000,  # OUT    (Wyślij wartość akumulatora do OUT)
    0b11110000,  # HLT    (Zatrzymaj program)
    0b00000001,  # RAM[1] = 1 (Liczba 1)
    0b00000010   # RAM[2] = 2 (Liczba 2)
]

# Inicjalizacja emulatora
sap1 = SAP1()
sap1.load_program(program)
print("Pamięć RAM:", sap1.RAM)

def wait_for_clock():
    """ Czeka na narastające zbocze zegara na GPIO 15 """
    while clock_pin.value() == 0:  # Czekaj na stan wysoki
        pass
    time.sleep(0.01)  # Krótkie opóźnienie dla uniknięcia drgań styków
    while clock_pin.value() == 1:  # Czekaj, aż wróci do stanu niskiego
        pass

def update_display(pc, ir, a, out):
    """ Aktualizacja wyświetlacza i terminala """
    display.clear()
    
    def to_bin_str(value):
        return ("000000" + bin(int(value))[2:])[-6:]

    def to_bin_str_PC(value):
        return ("0000" + bin(int(value))[2:])[-4:]

    display.draw_text(0, 2,  "PC: " + to_bin_str_PC(pc))
    display.draw_text(0, 12, "IR: " + to_bin_str(ir))
    display.draw_text(0, 22, "A:  " + to_bin_str(a))
    display.draw_text(0, 32, "OUT:" + to_bin_str(out))
    
    display.show()

    # Wypisywanie rejestrów na ekran komputera
    print(f"PC:  {to_bin_str_PC(pc)}")
    print(f"IR:  {to_bin_str(ir)}")
    print(f"A:   {to_bin_str(a)}")
    print(f"OUT: {to_bin_str(out)}")
    print("-" * 20)  # Oddzielenie kolejnych cykli

update_display(sap1.PC, sap1.IR, sap1.A, sap1.OUT)

# Uruchomienie SAP-1 z zewnętrznym zegarem
while True:
    wait_for_clock()  # Czekaj na narastające zbocze zegara
    sap1.step()  # Wykonaj jeden cykl
    update_display(sap1.PC, sap1.IR, sap1.A, sap1.OUT)  # Aktualizacja ekranu i terminala
