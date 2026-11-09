from app.estructuras.arbol_categorias import ArbolCategorias
from app.modelos.enums import Categoria


def test_es_subtipo_de_casos_validos_e_invalidos():
    arbol = ArbolCategorias()

    assert arbol.es_subtipo_de("camiseta", Categoria.SUPERIOR) is True
    assert arbol.es_subtipo_de("jean", Categoria.SUPERIOR) is False
    assert arbol.es_subtipo_de("jean", Categoria.INFERIOR) is True
    assert arbol.es_subtipo_de("inexistente", Categoria.SUPERIOR) is False


def test_es_subtipo_de_acepta_categoria_como_string():
    arbol = ArbolCategorias()
    assert arbol.es_subtipo_de("tenis", "calzado") is True


def test_categoria_de_subtipo():
    arbol = ArbolCategorias()
    assert arbol.categoria_de("blazer") == "exterior"
    assert arbol.categoria_de("no_existe") is None


def test_subtipos_de_una_categoria_en_orden_alfabetico():
    arbol = ArbolCategorias()
    assert arbol.subtipos(Categoria.CALZADO) == ["bota", "sandalia", "tenis", "zapato_formal"]
    assert arbol.subtipos("categoria_inexistente") == []


def test_recorrido_dfs_incluye_todas_las_categorias_y_subtipos():
    arbol = ArbolCategorias()
    recorrido = arbol.recorrido_dfs()

    assert "superior" in recorrido
    assert "superior/camiseta" in recorrido
    assert "exterior/blazer" in recorrido
    # 5 categorias + 5+4+5+4+5=23 subtipos = 28 nodos
    assert len(recorrido) == 28


def test_arbol_personalizado_con_datos_propios():
    datos = {Categoria.SUPERIOR: ["camiseta"], Categoria.CALZADO: ["tenis"]}
    arbol = ArbolCategorias(datos)

    assert arbol.es_subtipo_de("camiseta", Categoria.SUPERIOR) is True
    assert arbol.es_subtipo_de("jean", Categoria.INFERIOR) is False  # no esta en estos datos
