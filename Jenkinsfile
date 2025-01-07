pipeline {
    agent any // Define el entorno de ejecución (puede ser "any", "docker", etc.)

    stages {
        stage('Checkout') {
            steps {
                // Clona el repositorio de GitHub
                git branch: 'main', url: 'https://github.com/mdavila-2001/FOS-Elekta-Automation'
            }
        }

        stage('Instalar Dependencias') {
            steps {
                // Instala las dependencias necesarias (si tienes un requirements.txt)
                sh 'pip install requests pytest'
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                // Ejecuta las pruebas automatizadas
                sh 'python main.py'
            }
        }

        /* stage('Generar Reportes') {
            steps {
                // Aquí puedes agregar pasos para generar reportes de pruebas (opcional)
                echo 'Generando reportes de pruebas...'
            }
        } */
    }

    post {
        always {
            // Acciones que se ejecutarán siempre, independientemente del resultado
            echo 'Pipeline finalizado.'
        }
        success {
            // Acciones que se ejecutarán si el pipeline es exitoso
            echo '¡Todas las pruebas pasaron exitosamente!'
        }
        failure {
            // Acciones que se ejecutarán si el pipeline falla
            echo 'Alguna prueba falló. Revisa los logs para más detalles.'
        }
    }
}