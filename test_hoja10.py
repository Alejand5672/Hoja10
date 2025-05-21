import unittest
import math
from hoja10 import Grafo

class TestGrafo(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.ciudades = ['Guatemala', 'Mixco', 'Antigua', 'Escuintla']
        self.grafo = Grafo(self.ciudades)
        
        # Agregamos conexiones de prueba
        self.grafo.agregar_arco('Guatemala', 'Mixco', 10, 15, 20, 25)
        self.grafo.agregar_arco('Mixco', 'Antigua', 15, 20, 25, 30)
        self.grafo.agregar_arco('Antigua', 'Escuintla', 20, 25, 30, 35)
        self.grafo.agregar_arco('Escuintla', 'Guatemala', 25, 30, 35, 40)

    def test_agregar_arco(self):
        """Prueba que las conexiones se agreguen correctamente"""
        idx_guate = self.grafo.indices['Guatemala']
        idx_mixco = self.grafo.indices['Mixco']
        
        self.assertEqual(self.grafo.distancias['normal'][idx_guate][idx_mixco], 10)
        self.assertEqual(self.grafo.distancias['lluvia'][idx_guate][idx_mixco], 15)
        self.assertEqual(self.grafo.rutas[idx_guate][idx_mixco], idx_mixco)

    def test_floyd_warshall(self):
        """Prueba el algoritmo de Floyd-Warshall"""
        dist, rutas = self.grafo.floyd_warshall()
        idx_guate = self.grafo.indices['Guatemala']
        idx_antigua = self.grafo.indices['Antigua']
        
        # Distancia directa no existe, debe ser a través de Mixco
        self.assertEqual(dist[idx_guate][idx_antigua], 25)  # 10 (Guate-Mixco) + 15 (Mixco-Antigua)

    def test_obtener_ruta(self):
        """Prueba la reconstrucción de rutas"""
        _, rutas = self.grafo.floyd_warshall()
        idx_guate = self.grafo.indices['Guatemala']
        idx_escuintla = self.grafo.indices['Escuintla']
        
        ruta = self.grafo.obtener_ruta(idx_guate, idx_escuintla, rutas)
        ruta_ciudades = [self.ciudades[i] for i in ruta]
        
        self.assertEqual(ruta_ciudades, ['Guatemala', 'Mixco', 'Antigua', 'Escuintla'])

    def test_calcular_centro(self):
        """Prueba el cálculo del centro del grafo"""
        dist, _ = self.grafo.floyd_warshall()
        centro = self.grafo.calcular_centro(dist)
        
        # En este grafo de prueba, Mixco debería ser el centro
        self.assertEqual(centro, 'Mixco')

    def test_condiciones_climaticas(self):
        """Prueba que los diferentes climas afecten las distancias"""
        dist_normal, _ = self.grafo.floyd_warshall('normal')
        dist_lluvia, _ = self.grafo.floyd_warshall('lluvia')
        idx_guate = self.grafo.indices['Guatemala']
        idx_antigua = self.grafo.indices['Antigua']
        
        self.assertGreater(dist_lluvia[idx_guate][idx_antigua], dist_normal[idx_guate][idx_antigua])

class TestArchivoGrafo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Prueba la lectura del archivo guategrafo.txt"""
        try:
            from hoja10 import leer_archivo
            cls.ciudades, cls.conexiones = leer_archivo('guategrafo.txt')
        except FileNotFoundError:
            raise unittest.SkipTest("Archivo guategrafo.txt no encontrado, omitiendo pruebas de archivo")

    def test_lectura_archivo(self):
        """Prueba que el archivo se lea correctamente"""
        self.assertGreater(len(self.ciudades), 0)
        self.assertGreater(len(self.conexiones), 0)
        
        # Verifica que cada conexión tenga 6 elementos
        for conexion in self.conexiones:
            self.assertEqual(len(conexion), 6)

if _name_ == '_main_':
       unittest.main()