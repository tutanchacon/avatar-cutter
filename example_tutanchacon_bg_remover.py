"""
Ejemplo de uso de TutanchaconBgRemover
"""

from src.tutanchacon_bg_remover import TutanchaconBgRemover

def main():
    """Ejemplo de uso del removedor de fondos de tutanchacon."""
    
    print("🎨 Avatar Cutter - Removedor de Fondos Tutanchacon")
    print("=" * 55)
    
    # Crear instancia del removedor de fondos
    try:
        # Configuración optimizada para avatares
        bg_remover = TutanchaconBgRemover(
            model_name='isnet-general-use',  # Modelo más preciso
            min_alpha_threshold=20,          # Configuración óptima recomendada
            preserve_elements=True,          # Preservar accesorios y elementos
            smooth_edges=True               # Suavizar bordes
        )
        
        print(f"✅ {bg_remover}")
        
        # Ejemplo de procesamiento
        input_image = "avatar_formato ejemplo/avatar_136x234.png"
        output_image = "output/avatar_no_bg.png"
        
        print(f"\n📸 Procesando: {input_image}")
        print(f"💾 Salida: {output_image}")
        
        # Obtener estadísticas si está disponible
        stats = bg_remover.get_stats(input_image)
        if stats:
            print(f"📊 Estadísticas: {stats}")
        
        # Remover fondo
        bg_remover.remove_background(input_image, output_image)
        
        print("\n🎉 ¡Proceso completado!")
        print("💡 Consejos:")
        print("   - Si quedan objetos no deseados, prueba con umbral más bajo (10-15)")
        print("   - Para avatares complejos, el umbral 20 es óptimo")
        print("   - Para retoques finales, puedes usar umbral 50")
        
    except ImportError as e:
        print("❌ Error de importación:")
        print(str(e))
        print("\n🔧 Para resolver:")
        print("1. Clonar el repositorio bgremover:")
        print("   git clone https://github.com/tutanchacon/bgremover.git")
        print("2. Instalar dependencias:")
        print("   cd bgremover && pip install -r requirements.txt")
        print("3. Instalar como paquete:")
        print("   pip install -e .")
        print("4. O copiar los archivos necesarios a este proyecto")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
