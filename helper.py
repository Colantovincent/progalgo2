class Helper:
    @classmethod
    def inv(cls, c: list[list[int]]) -> int:
        conta = 0
        v = cls._flatter(c)
        for i in range(len(v)):
            el = v[i]
            if el == 0:
                continue

            for j in range(i - 1, -1, -1):
                if el < v[j]:
                    conta += 1
        return conta

    @classmethod
    def ind(cls, n: int, i: int) -> int:
        return n - i

    @classmethod
    def _flatter(cls, c: list[list[int]]) -> list[int]:
        linearizzata: list[int] = []
        for riga in c:
            for el in riga:
                linearizzata.append(el)
        return linearizzata