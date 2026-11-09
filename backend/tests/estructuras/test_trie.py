from app.estructuras.trie import Trie


def test_trie_vacio_no_encuentra_nada():
    trie = Trie()
    assert trie.buscar_prefijo("cam") == []


def test_insertar_y_buscar_prefijo_basico():
    trie = Trie()
    trie.insertar("Camiseta blanca", 1)
    trie.insertar("Camisa azul", 2)
    trie.insertar("Pantalon negro", 3)

    assert trie.buscar_prefijo("cam") == [2, 1]  # orden alfabetico: "camisa" < "camiseta"
    assert trie.buscar_prefijo("pan") == [3]
    assert trie.buscar_prefijo("zzz") == []


def test_busqueda_ignora_mayusculas_y_tildes():
    trie = Trie()
    trie.insertar("Pantalón de Lino", 5)

    assert trie.buscar_prefijo("pantalon") == [5]
    assert trie.buscar_prefijo("PANTALÓN") == [5]


def test_varias_prendas_pueden_compartir_nombre():
    trie = Trie()
    trie.insertar("camiseta blanca", 1)
    trie.insertar("camiseta blanca", 2)

    assert trie.buscar_prefijo("camiseta") == [1, 2]


def test_limite_de_resultados_se_respeta():
    trie = Trie()
    for i in range(5):
        trie.insertar(f"camiseta {i}", i)

    assert len(trie.buscar_prefijo("camiseta", limite=3)) == 3
    assert trie.buscar_prefijo("camiseta", limite=0) == []


def test_eliminar_una_entre_varias_prendas_compartidas():
    trie = Trie()
    trie.insertar("camiseta blanca", 1)
    trie.insertar("camiseta blanca", 2)

    assert trie.eliminar("camiseta blanca", 1) is True
    assert trie.buscar_prefijo("camiseta") == [2]
    assert trie.eliminar("camiseta blanca", 1) is False  # ya no esta


def test_eliminar_la_ultima_prenda_poda_el_camino():
    trie = Trie()
    trie.insertar("gorra", 1)
    trie.insertar("gorro", 2)  # comparte prefijo "gorr"

    assert trie.eliminar("gorra", 1) is True
    assert trie.buscar_prefijo("gorra") == []
    assert trie.buscar_prefijo("gorro") == [2]  # el prefijo compartido sigue intacto


def test_eliminar_palabra_inexistente_devuelve_false():
    trie = Trie()
    trie.insertar("camisa", 1)

    assert trie.eliminar("pantalon", 1) is False
    assert trie.eliminar("camisa", 999) is False
