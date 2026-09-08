class Helper:
    @classmethod
    def inv(cls, c: list[list[int]]) -> int:
        conta = 0
        massimo = c[0][0]
        for riga in c:
            for el in riga:
                if el == 0:
                    continue
                if massimo > el:
                    conta += 1
                    continue

                massimo = el
        return conta

    @classmethod
    def ind(cls, n: int, i: int) -> int:
        return n - i