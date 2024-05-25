"""
PROYECTO FINAL DE FUNDAMENTOS DE LOS SISTEMAS OPERATIVOS
Realizado por:
    - María González Gómez
    - Lydia Ruiz Martínez
"""

import time
import json
import hashlib


class Transaccion:
    def __init__(self, origen, destino, cantidad, tiempo):
        """
        Constructor de la clase `Transaccion`.
        :param origen: El origen de la transacción.
        :param destino: El destino de la transacción.
        :param cantidad: La cantidad de la transacción.
        :param tiempo: Tiempo de la transacción (por defecto, actual si no se proporciona).
        """
        self.origen = origen
        self.destino = destino
        self.cantidad = cantidad
        self.tiempo = time.time()
        self.lista_transacciones = []


class Bloque:
    def __init__(
        self,
        indice: int,
        transacciones: list,
        timestamp: int,
        hash_previo: str,
        hash: str,
        prueba: int,
    ):
        """
        Constructor de la clase `Bloque`.
        :param indice: ID unico del bloque.
        :param transacciones: Lista de transacciones.
        :param timestamp: Momento en que el bloque fue generado.
        :param hash_previo hash previo
        :param prueba: prueba de trabajo"""
        self.indice = indice
        self.transacciones = transacciones
        self.timestamp = timestamp
        self.hash_previo = hash_previo
        self.hash = None
        self.prueba = prueba

    def calcular_hash(self):
        """
        Metodo que devuelve el hash de un bloque
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def toDict(self):
        dict_bloque = {
            "hash": self.hash,
            "hash_previo": self.hash_previo,
            "indice": self.indice,
            "prueba": self.prueba,
            "timestamp": self.timestamp,
            "transacciones": self.transacciones,
        }
        return dict_bloque


class Blockchain(object):
    def __init__(self):
        self.dificultad = 4
        self.transacciones_no_confirmadas = []
        self.bloques = [self.primer_bloque()]

    def primer_bloque(self):
        """
        Crear un bloque vacío cuyo índice sea 1, sin transacciones y un hash_previo de 1.
        El objetivo de este primer bloque es ser simplemente el primero de la cadena para que luego puedan añadirse más bloques a dicha cadena.
        """
        bloque = Bloque(1, [], time.time(), "1", None, 0)
        bloque.hash = bloque.calcular_hash()
        return bloque

    def last_block(self):
        """
        Devuelve el último bloque de una lista de bloques.
        El objetivo de este último bloque es ser simplemente el último de la cadena.
        """
        return self.bloques[-1]

    def nuevo_bloque(self, hash_previo: str) -> Bloque:
        """
        Crea un nuevo bloque a partir de las transacciones que no estan confirmadas
        :param hash_previo: el hash del bloque anterior de la cadena
        :return: el nuevo bloque
        """
        nuevo_bloque = Bloque(
            len(self.bloques) + 1,
            self.transacciones_no_confirmadas,
            time.time(),
            hash_previo,
            hash,
            0,
        )
        self.bloques.append(nuevo_bloque)
        self.transacciones_no_confirmadas = []
        return nuevo_bloque

    def nueva_transaccion(self, origen: str, destino: str, cantidad: int) -> int:
        """
        Crea una nueva transaccion a partir de un origen, un destino y una cantidad y la incluye en las listas de transacciones
        :param origen: <str> el que envia la transaccion
        :param destino: <str> el que recibe la transaccion
        :param cantidad: <int> la candidad
        :return: <int> el indice del bloque que va a almacenar la transaccion
        """
        nueva_transaccion = {
            "origen": origen,
            "destino": destino,
            "cantidad ": cantidad,
            "tiempo": time.time(),
        }

        self.transacciones_no_confirmadas.append(nueva_transaccion)
        return len(self.bloques) + 1

    def prueba_valida(self, bloque: Bloque, hash_bloque: str) -> bool:
        """
        Metodo que comprueba si el hash_bloque comienza con tantos ceros como la dificultad estipulada en el blockchain
        Ademas comprobara que hash_bloque coincide con el valor devuelto del metodo de calcular hash del bloque.
        Si cualquiera de ambas comprobaciones es falsa, devolvera falso y en caso contrario, verdarero
        :param bloque:
        :param hash_bloque:
        :return:
        """
        hash = bloque.calcular_hash()
        if (
            hash == hash_bloque
            and hash_bloque[: self.dificultad] == "0" * self.dificultad
        ):
            return True
        else:
            return False

    def prueba_trabajo(self, bloque: Bloque) -> str:
        """
        Algoritmo simple de prueba de trabajo:
        - Calculara el hash del bloque hasta que encuentre un hash que empiece por tantos ceros como dificultad.
        - Cada vez que el bloque obtenga un hash que no sea adecuado, incrementara en uno el campo de prueba del bloque
        :param bloque: objeto de tipo bloque
        :return: el hash del nuevo bloque (dejara el campo de hash del bloque sin modificar)
        """

        bloque.prueba = 0
        hash_bloque = bloque.calcular_hash()
        while not self.prueba_valida(bloque, hash_bloque):
            bloque.prueba += 1
            hash_bloque = bloque.calcular_hash()
        return hash_bloque

    def prueba_valida(self, bloque: Bloque, hash_bloque: str) -> bool:
        """
        Metodo que comprueba si el hash_bloque comienza con tantos ceros como la dificultad estipulada en el blockchain
        Ademas comprobara que hash_bloque coincide con el valor devuelto del metodo de calcular hash del bloque.
        Si cualquiera de ambas comprobaciones es falsa, devolvera falso y en caso contrario, verdarero
        :param bloque:
        :param hash_bloque:
        :return:
        """
        hash = bloque.calcular_hash()
        if (
            hash == hash_bloque
            and hash_bloque[: self.dificultad] == "0" * self.dificultad
        ):
            return True
        else:
            return False

    def integra_bloque(self, bloque_nuevo: Bloque, hash_prueba: str) -> bool:
        """
        Metodo para integrar correctamente un bloque a la cadena de bloques.
        Debe comprobar que hash_prueba es valida y que el hash del bloque ultimo de la cadena coincida con el hash_previo del bloque que se va a integrar.
        Si pasa las comprobaciones, actualiza el hash del bloque nuevo a integrar con hash_prueba, lo inserta en la cadena y
        hace un reset de las transacciones no confirmadas (vuelve a dejar la lista de transacciones no confirmadas a una lista vacia)
        :param bloque_nuevo: el nuevo bloque que se va a integrar
        :param hash_prueba: la prueba de hash
        :return: True si se ha podido ejecutar bien y False en caso contrario (si no ha pasado alguna prueba)
        """

        if self.last_block().hash == bloque_nuevo.hash_previo:
            nuevo = Bloque(
                bloque_nuevo.indice,
                bloque_nuevo.transacciones,
                bloque_nuevo.timestamp,
                bloque_nuevo.hash_previo,
                bloque_nuevo.hash,
                bloque_nuevo.prueba,
            )

            nuevo.hash = nuevo.calcular_hash()
            if nuevo.hash == hash_prueba:
                self.bloques.append(nuevo)
                self.transacciones_no_confirmadas = []
                return True
            else:
                return False
        else:
            return False
