import time

class SAP1:
    def __init__(self):
        self.PC = 0      # Licznik programowy (4-bit)
        self.IR = 0      # Rejestr instrukcji (8-bit)
        self.A = 0       # Akumulator (8-bit)
        self.OUT = 0     # Rejestr wyjściowy (8-bit)
        self.RAM = [0] * 16  # Pamięć RAM (16 komórek po 8-bitów)
        self.running = True

    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.RAM[i] = instruction
            print(f"RAM[{i}] = {instruction:08b}")  # Debugowanie RAM

    def fetch(self):
        """ Pobranie instrukcji z pamięci do IR """
        self.IR = self.RAM[self.PC]
        self.PC = (self.PC + 1) % 16  # 4-bitowy licznik programowy

    def decode_execute(self):
        """ Dekodowanie i wykonanie instrukcji """
        opcode = (self.IR & 0xF0) >> 4  # Pierwsze 4 bity to kod operacji
        operand = self.IR & 0x0F       # Ostatnie 4 bity to argument
        
        print(f"IR: {bin(self.IR)} -> opcode: {bin(opcode)}, operand: {bin(operand)}")
        
        if opcode == 0b0001:  # LDA
            print(f"LDA {operand}: RAM[{operand}] = {self.RAM[operand]}")
            self.A = self.RAM[operand]
        elif opcode == 0b0010:  # ADD
            print(f"ADD {operand}: {self.A} + {self.RAM[operand]}")
            self.A = (self.A + self.RAM[operand]) % 256
            print(f"Wynik w A: {self.A}")
        elif opcode == 0b0011:  # SUB (Odejmij od akumulatora)
            self.A = (self.A - self.RAM[operand]) % 256
        elif opcode == 0b1110:  # OUT (Zapisz do rejestru wyjściowego)
            self.OUT = self.A
        elif opcode == 0b1111:  # HLT (Zatrzymanie)
            print("HLT - zatrzymanie programu!")
            self.running = False
            self.PC = 15  # Zatrzymanie wykonania

    def step(self):
        """ Wykonuje jeden cykl maszynowy """
        if not self.running:
            print("SAP-1 zatrzymany. Brak dalszego wykonania.")
            return
        self.fetch()
        self.decode_execute()

    def run(self, update_display):
        """ Główna pętla wykonująca program """
        while self.running:
            print(f"PC: {self.PC:04b}, Running: {self.running}")  # Debug
            self.step()
            update_display(self.PC, self.IR, self.A, self.OUT)
            time.sleep(0.5)  # Opóźnienie dla wizualizacji zegara
        print("Program zakończył działanie.")  # Sprawdzenie, czy pętla się kończy

