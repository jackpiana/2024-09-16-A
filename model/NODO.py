from dataclasses import dataclass


@dataclass(order= True, frozen = True)
class Nodo():
    state: str
    pesoNodo: float

    def __repr__(self):
        return f"({self.state}, {self.pesoNodo})"
