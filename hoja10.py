import sys
import math

class Grafo:
    def __init__(self, ciudades):
        self.ciudades = ciudades
        self.num_ciudades = len(ciudades)
        self.indices = {ciudad: idx for idx, ciudad in enumerate(ciudades)}
        # Matrices para diferentes condiciones climáticas
        self.distancias = {
            'normal': [[math.inf] * self.num_ciudades for _ in range(self.num_ciudades)],
            'lluvia': [[math.inf] * self.num_ciudades for _ in range(self.num_ciudades)],
            'nieve': [[math.inf] * self.num_ciudades for _ in range(self.num_ciudades)],
            'tormenta': [[math.inf] * self.num_ciudades for _ in range(self.num_ciudades)]
        }
        # Matrices de rutas
        self.rutas = [[None] * self.num_ciudades for _ in range(self.num_ciudades)]
        
        # Inicializar diagonales
        for i in range(self.num_ciudades):
            for clima in self.distancias:
                self.distancias[clima][i][i] = 0

    def agregar_arco(self, ciudad1, ciudad2, normal, lluvia, nieve, tormenta):
        i = self.indices[ciudad1]
        j = self.indices[ciudad2]
        self.distancias['normal'][i][j] = normal
        self.distancias['lluvia'][i][j] = lluvia
        self.distancias['nieve'][i][j] = nieve
        self.distancias['tormenta'][i][j] = tormenta
        self.rutas[i][j] = j  # Inicialmente la ruta directa

    def floyd_warshall(self, clima='normal'):
        dist = [row[:] for row in self.distancias[clima]]
        rutas = [row[:] for row in self.rutas]
        
        for k in range(self.num_ciudades):
            for i in range(self.num_ciudades):
                for j in range(self.num_ciudades):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        rutas[i][j] = rutas[i][k]
        
        return dist, rutas

    def obtener_ruta(self, origen, destino, rutas):
        if rutas[origen][destino] is None:
            return []
        
        camino = [origen]
        while origen != destino:
            origen = rutas[origen][destino]
            camino.append(origen)
        
        return camino

    def calcular_centro(self, dist):
        excentricidades = []
        for j in range(self.num_ciudades):
            max_dist = -math.inf
            for i in range(self.num_ciudades):
                if dist[i][j] > max_dist and dist[i][j] != math.inf:
                    max_dist = dist[i][j]
            excentricidades.append(max_dist if max_dist != -math.inf else math.inf)
        
        min_excentricidad = min(excentricidades)
        centro_idx = excentricidades.index(min_excentricidad)
        return self.ciudades[centro_idx]

def leer_archivo(nombre_archivo):
    ciudades = set()
    conexiones = []
    
    with open(nombre_archivo, 'r') as f:
        for linea in f:
            partes = linea.strip().split()
            if len(partes) == 6:
                ciudad1, ciudad2, normal, lluvia, nieve, tormenta = partes
                ciudades.add(ciudad1)
                ciudades.add(ciudad2)
                conexiones.append((ciudad1, ciudad2, int(normal), int(lluvia), int(nieve), int(tormenta)))
    
    return list(ciudades), conexiones

def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Consultar ruta más corta entre dos ciudades")
    print("2. Mostrar el centro del grafo")
    print("3. Modificar el grafo")
    print("4. Cambiar condición climática")
    print("5. Salir")

def menu_modificacion():
    print("\n--- Modificar Grafo ---")
    print("a. Interrumpir tráfico entre dos ciudades")
    print("b. Establecer nueva conexión entre ciudades")
    print("c. Volver al menú principal")

def main():
    if len(sys.argv) != 2:
        print("Uso: python floyd_rutas.py guategrafo.txt")
        return
    
    archivo = sys.argv[1]
    ciudades_list, conexiones = leer_archivo(archivo)
    grafo = Grafo(ciudades_list)
    
    for conexion in conexiones:
        grafo.agregar_arco(*conexion)
    
    clima_actual = 'normal'
    dist, rutas = grafo.floyd_warshall(clima_actual)
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            ciudad1 = input("Ciudad origen: ")
            ciudad2 = input("Ciudad destino: ")
            
            if ciudad1 not in grafo.indices or ciudad2 not in grafo.indices:
                print("Una o ambas ciudades no existen en el grafo.")
                continue
            
            idx1 = grafo.indices[ciudad1]
            idx2 = grafo.indices[ciudad2]
            
            if dist[idx1][idx2] == math.inf:
                print(f"No hay ruta disponible entre {ciudad1} y {ciudad2} con clima {clima_actual}.")
            else:
                camino_indices = grafo.obtener_ruta(idx1, idx2, rutas)
                camino_ciudades = [grafo.ciudades[i] for i in camino_indices]
                print(f"\nRuta más corta de {ciudad1} a {ciudad2} (clima {clima_actual}):")
                print(f"Distancia total: {dist[idx1][idx2]} horas")
                print("Ruta:", " -> ".join(camino_ciudades))
        
        elif opcion == '2':
            centro = grafo.calcular_centro(dist)
            print(f"\nLa ciudad que queda en el centro del grafo es: {centro}")
        
        elif opcion == '3':
            while True:
                menu_modificacion()
                sub_opcion = input("Seleccione una opción: ").lower()
                
                if sub_opcion == 'a':
                    ciudad1 = input("Ciudad origen: ")
                    ciudad2 = input("Ciudad destino: ")
                    
                    if ciudad1 not in grafo.indices or ciudad2 not in grafo.indices:
                        print("Una o ambas ciudades no existen en el grafo.")
                        continue
                    
                    idx1 = grafo.indices[ciudad1]
                    idx2 = grafo.indices[ciudad2]
                    
                    for clima in grafo.distancias:
                        grafo.distancias[clima][idx1][idx2] = math.inf
                    grafo.rutas[idx1][idx2] = None
                    
                    print(f"Tráfico interrumpido entre {ciudad1} y {ciudad2} para todas las condiciones climáticas.")
                    dist, rutas = grafo.floyd_warshall(clima_actual)
                
                elif sub_opcion == 'b':
                    ciudad1 = input("Ciudad origen: ")
                    ciudad2 = input("Ciudad destino: ")
                    
                    if ciudad1 not in grafo.indices or ciudad2 not in grafo.indices:
                        print("Una o ambas ciudades no existen en el grafo.")
                        continue
                    
                    try:
                        normal = int(input("Tiempo normal (horas): "))
                        lluvia = int(input("Tiempo con lluvia (horas): "))
                        nieve = int(input("Tiempo con nieve (horas): "))
                        tormenta = int(input("Tiempo con tormenta (horas): "))
                    except ValueError:
                        print("Por favor ingrese valores numéricos válidos.")
                        continue
                    
                    grafo.agregar_arco(ciudad1, ciudad2, normal, lluvia, nieve, tormenta)
                    print(f"Nueva conexión establecida entre {ciudad1} y {ciudad2}.")
                    dist, rutas = grafo.floyd_warshall(clima_actual)
                
                elif sub_opcion == 'c':
                    break
                
                else:
                    print("Opción no válida.")
        
        elif opcion == '4':
            print("\nCondiciones climáticas disponibles:")
            print("1. Normal")
            print("2. Lluvia")
            print("3. Nieve")
            print("4. Tormenta")
            
            try:
                clima_opcion = int(input("Seleccione condición climática: "))
                climas = ['normal', 'lluvia', 'nieve', 'tormenta']
                if 1 <= clima_opcion <= 4:
                    clima_actual = climas[clima_opcion - 1]
                    dist, rutas = grafo.floyd_warshall(clima_actual)
                    print(f"Condición climática cambiada a: {clima_actual}")
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Por favor ingrese un número válido.")
        
        elif opcion == '5':
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción no válida. Por favor intente de nuevo.")

if __name__ == "__main__":
    main()