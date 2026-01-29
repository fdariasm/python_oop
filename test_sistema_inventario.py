import unittest
from sistema_inventario import Producto, Inventario


class TestProducto(unittest.TestCase):
    """Pruebas para la clase Producto."""

    # --- Creación válida ---

    def test_crear_producto_valido(self):
        p = Producto("Laptop", 999.99, 5)
        self.assertEqual(p.nombre, "Laptop")
        self.assertEqual(p.precio, 999.99)
        self.assertEqual(p.cantidad, 5)

    def test_crear_producto_precio_cero(self):
        p = Producto("Gratis", 0, 10)
        self.assertEqual(p.precio, 0.0)

    def test_crear_producto_cantidad_cero(self):
        p = Producto("Agotado", 50.0, 0)
        self.assertEqual(p.cantidad, 0)

    def test_nombre_se_recorta_espacios(self):
        p = Producto("  Teclado  ", 30.0, 2)
        self.assertEqual(p.nombre, "Teclado")

    def test_precio_entero_se_convierte_a_float(self):
        p = Producto("Mouse", 25, 3)
        self.assertIsInstance(p.precio, float)

    # --- Validaciones del constructor ---

    def test_nombre_vacio_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto("", 10.0, 1)

    def test_nombre_solo_espacios_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto("   ", 10.0, 1)

    def test_nombre_no_string_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto(123, 10.0, 1)

    def test_precio_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto("Test", -1.0, 1)

    def test_cantidad_negativa_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto("Test", 10.0, -1)

    def test_precio_string_lanza_error(self):
        with self.assertRaises(TypeError):
            Producto("Test", "diez", 1)

    def test_cantidad_float_lanza_error(self):
        with self.assertRaises(TypeError):
            Producto("Test", 10.0, 2.5)

    # --- Métodos de actualización ---

    def test_actualizar_precio_valido(self):
        p = Producto("Laptop", 100.0, 1)
        p.actualizar_precio(200.0)
        self.assertEqual(p.precio, 200.0)

    def test_actualizar_precio_negativo_lanza_error(self):
        p = Producto("Laptop", 100.0, 1)
        with self.assertRaises(ValueError):
            p.actualizar_precio(-50.0)
        self.assertEqual(p.precio, 100.0)  # no debe cambiar

    def test_actualizar_cantidad_valida(self):
        p = Producto("Laptop", 100.0, 1)
        p.actualizar_cantidad(10)
        self.assertEqual(p.cantidad, 10)

    def test_actualizar_cantidad_negativa_lanza_error(self):
        p = Producto("Laptop", 100.0, 5)
        with self.assertRaises(ValueError):
            p.actualizar_cantidad(-3)
        self.assertEqual(p.cantidad, 5)  # no debe cambiar

    # --- Cálculo y representación ---

    def test_calcular_valor_total(self):
        p = Producto("Laptop", 999.99, 5)
        self.assertAlmostEqual(p.calcular_valor_total(), 4999.95)

    def test_calcular_valor_total_cantidad_cero(self):
        p = Producto("Agotado", 50.0, 0)
        self.assertEqual(p.calcular_valor_total(), 0.0)

    def test_str_formato(self):
        p = Producto("Mouse", 29.99, 10)
        texto = str(p)
        self.assertIn("Mouse", texto)
        self.assertIn("$29.99", texto)
        self.assertIn("10", texto)
        self.assertIn("$299.90", texto)


class TestInventario(unittest.TestCase):
    """Pruebas para la clase Inventario."""

    def setUp(self):
        """Crea un inventario fresco antes de cada test."""
        self.inventario = Inventario()

    # --- Agregar productos ---

    def test_agregar_producto(self):
        p = Producto("Laptop", 999.99, 5)
        self.inventario.agregar_producto(p)
        self.assertEqual(len(self.inventario.productos), 1)

    def test_agregar_varios_productos(self):
        self.inventario.agregar_producto(Producto("A", 10, 1))
        self.inventario.agregar_producto(Producto("B", 20, 2))
        self.inventario.agregar_producto(Producto("C", 30, 3))
        self.assertEqual(len(self.inventario.productos), 3)

    def test_agregar_no_producto_lanza_error(self):
        with self.assertRaises(TypeError):
            self.inventario.agregar_producto("no soy un producto")

    # --- Buscar productos ---

    def test_buscar_producto_existente(self):
        p = Producto("Laptop", 999.99, 5)
        self.inventario.agregar_producto(p)
        encontrado = self.inventario.buscar_producto("Laptop")
        self.assertEqual(encontrado, p)

    def test_buscar_producto_case_insensitive(self):
        p = Producto("Laptop", 999.99, 5)
        self.inventario.agregar_producto(p)
        self.assertEqual(self.inventario.buscar_producto("laptop"), p)
        self.assertEqual(self.inventario.buscar_producto("LAPTOP"), p)
        self.assertEqual(self.inventario.buscar_producto("LaPtOp"), p)

    def test_buscar_producto_con_espacios(self):
        p = Producto("Laptop", 999.99, 5)
        self.inventario.agregar_producto(p)
        self.assertEqual(self.inventario.buscar_producto("  Laptop  "), p)

    def test_buscar_producto_no_existente(self):
        self.inventario.agregar_producto(Producto("Laptop", 999.99, 5))
        resultado = self.inventario.buscar_producto("Monitor")
        self.assertIsNone(resultado)

    def test_buscar_en_inventario_vacio(self):
        resultado = self.inventario.buscar_producto("Laptop")
        self.assertIsNone(resultado)

    # --- Valor del inventario ---

    def test_calcular_valor_inventario(self):
        self.inventario.agregar_producto(Producto("Laptop", 1000, 2))   # 2000
        self.inventario.agregar_producto(Producto("Mouse", 50, 10))     # 500
        self.assertAlmostEqual(self.inventario.calcular_valor_inventario(), 2500.0)

    def test_calcular_valor_inventario_vacio(self):
        self.assertEqual(self.inventario.calcular_valor_inventario(), 0.0)

    def test_calcular_valor_inventario_un_producto(self):
        self.inventario.agregar_producto(Producto("Teclado", 49.99, 3))
        self.assertAlmostEqual(self.inventario.calcular_valor_inventario(), 149.97)

    # --- Listar productos ---

    def test_listar_inventario_vacio(self, capsys=None):
        # Verificamos que no lanza excepción
        self.inventario.listar_productos()

    def test_listar_inventario_con_productos(self):
        self.inventario.agregar_producto(Producto("A", 10, 1))
        self.inventario.agregar_producto(Producto("B", 20, 2))
        # Verificamos que no lanza excepción
        self.inventario.listar_productos()


if __name__ == "__main__":
    unittest.main()
