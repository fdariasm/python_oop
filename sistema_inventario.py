class Producto:
    """Representa un producto con nombre, precio y cantidad."""

    def __init__(self, nombre: str, precio: float, cantidad: int):
        # Validación del nombre: no puede estar vacío ni ser solo espacios
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")

        self.nombre = nombre.strip()
        # Delegar validación a los métodos para no duplicar lógica
        self.actualizar_precio(precio)
        self.actualizar_cantidad(cantidad)

    def actualizar_precio(self, nuevo_precio: float) -> None:
        """Actualiza el precio del producto validando que sea >= 0."""
        if not isinstance(nuevo_precio, (int, float)):
            raise TypeError("El precio debe ser un valor numérico.")
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.precio = float(nuevo_precio)

    def actualizar_cantidad(self, nueva_cantidad: int) -> None:
        """Actualiza la cantidad del producto validando que sea >= 0."""
        if not isinstance(nueva_cantidad, int):
            raise TypeError("La cantidad debe ser un número entero.")
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.cantidad = nueva_cantidad

    def calcular_valor_total(self) -> float:
        """Devuelve el valor total del producto (precio x cantidad)."""
        return self.precio * self.cantidad

    def __str__(self) -> str:
        """Representación legible del producto."""
        return (
            f"Producto: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | "
            f"Cantidad: {self.cantidad} | "
            f"Valor total: ${self.calcular_valor_total():.2f}"
        )


class Inventario:
    """Gestiona una colección de productos."""

    def __init__(self):
        self.productos: list[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        """Añade un producto a la lista del inventario."""
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar objetos de tipo Producto.")
        self.productos.append(producto)

    def buscar_producto(self, nombre: str) -> Producto | None:
        """Busca un producto por nombre (insensible a mayúsculas/minúsculas).
        Devuelve el producto si lo encuentra, None si no existe."""
        nombre_lower = nombre.strip().lower()
        return next(
            (p for p in self.productos if p.nombre.lower() == nombre_lower),
            None
        )

    def calcular_valor_inventario(self) -> float:
        """Calcula la suma del valor total de todos los productos."""
        return sum(p.calcular_valor_total() for p in self.productos)

    def listar_productos(self) -> None:
        """Muestra todos los productos del inventario."""
        if not self.productos:
            print("El inventario está vacío.")
            return
        print(f"\n{'='*60}")
        print(f"  INVENTARIO ({len(self.productos)} productos)")
        print(f"{'='*60}")
        for i, producto in enumerate(self.productos, start=1):
            print(f"  {i}. {producto}")
        print(f"{'='*60}")


def menu_principal(inventario: Inventario) -> None:
    """Menú interactivo para operar el sistema de inventario."""
    while True:
        print("\n--- SISTEMA DE INVENTARIO ---")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Listar productos")
        print("4. Calcular valor total del inventario")
        print("5. Salir")

        opcion = input("\nSeleccione una opción (1-5): ").strip()

        if opcion == "1":
            try:
                nombre = input("Nombre del producto: ")
                precio = float(input("Precio del producto: "))
                cantidad = int(input("Cantidad del producto: "))
                producto = Producto(nombre, precio, cantidad)
                inventario.agregar_producto(producto)
                print(f"\nProducto '{producto.nombre}' agregado exitosamente.")
            except ValueError as e:
                print(f"\nError: {e}")
            except TypeError as e:
                print(f"\nError de tipo: {e}")

        elif opcion == "2":
            try:
                nombre = input("Nombre del producto a buscar: ").strip()
                if not nombre:
                    print("\nError: Debe ingresar un nombre para buscar.")
                    continue
                producto = inventario.buscar_producto(nombre)
                if producto:
                    print(f"\nProducto encontrado:\n  {producto}")
                else:
                    print(f"\nNo se encontró ningún producto con el nombre '{nombre}'.")
            except ValueError as e:
                print(f"\nError: {e}")

        elif opcion == "3":
            inventario.listar_productos()

        elif opcion == "4":
            valor = inventario.calcular_valor_inventario()
            print(f"\nValor total del inventario: ${valor:.2f}")

        elif opcion == "5":
            print("\nSaliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("\nOpción no válida. Por favor seleccione una opción del 1 al 5.")


if __name__ == "__main__":
    inventario = Inventario()
    menu_principal(inventario)
