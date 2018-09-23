from symbol import SymbolTable


class Parser:
    symbol_base = 16
    type_a = 0
    type_c = 1
    CComp = {
        "0":"0101010", "1":"0111111", "-1":"0111010", "D":"0001100", "A":"0110000", "M":"1110000", "!D":"0001101",
        "!A":"0110001", "!M":"1110001","-D":"0001111", "-A":"0110011", "-M":"1110011", "D+1":"0011111", "A+1":"0110111",
        "M+1":"1110111", "D-1":"0001110", "A-1":"0110010", "M-1":"1110010", "D+A": "0000010", "D+M":"1000010",
        "D-A":"0010011", "D-M":"1010011", "A-D":"0000111", "M-D":"1000111", "D&A":"0000000",
        "D&M":"1000000", "D|A":"0010101", "D|M":"1010101"
    }
    CDest = {
        "":"000", "M":"001", "D":"010", "MD":"011" , "A":"100", "AM":"101", "AD":"110", "AMD":"111"
    }
    CJump = {
        "":"000", "JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"
    }

    CPrefix = "111"
    APrefix = "0"

    def __init__(self):
        self.table = SymbolTable()

    def _binary(self, number):
        return bin(number)[2:].zfill(15)

    def set_symbol(self, line):
        if not line.split("@")[1].isdigit() and line.split("@")[1] not in self.table:
            self.table[line.split("@")[1]] = self.symbol_base
            self.symbol_base += 1

    def set_label(self, line, value):
        self.table[line[line.find("(") + 1:line.find(")")]] = value

    def parse(self, line):
        result = self.get_type(line)
        if result == self.type_a:
            if line.split("@")[1].isdigit():
                code = self.APrefix + str(self._binary(int(line.split("@")[1])))
            else:
                code = self.APrefix + str(self._binary(self.table[line.split("@")[1]]))
        else:
            if ";" in line:
                jump = line.split(";")[1]
                other = line.split(";")[0]
                if "=" in line:
                    dest = other.split("=")[0]
                    comp = other.split("=")[1]
                else:
                    comp = other
                    dest = ""
            else:
                jump = ""
                dest = line.split("=")[0]
                comp = line.split("=")[1]
            code = self.CPrefix + self.CComp[comp] + self.CDest[dest]+self.CJump[jump]
        return code

    def get_type(self, line):
        if "@" in line:
            result = self.type_a
        else:
            result = self.type_c
        return result


