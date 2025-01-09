pipeline {
    agent any // Define el entorno de ejecución (puede ser "any", "docker", etc.)

    stages {

        stage('Instalar Dependencias') {
            steps {
                bat 'pip install requests pytest'
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                // Ejecuta las pruebas automatizadas
                bat 'python main.py'
            }
        }

        stage('Generar Reportes') {
            steps {
                // Aquí puedes agregar pasos para generar reportes de pruebas (opcional)
                echo 'Generando reportes de pruebas...'
                bat 'pytest backend/loginTest.py --html=report.html'
                bat 'pytest backend/rolesTest.py --html=report.html'
                bat 'pytest backend/usersTest.py --html=report.html'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizado.'
        }
        success {
            echo '¡Todas las pruebas pasaron exitosamente, felicidades! Revisa el archivo report.html en tu carpeta de trabajo para más detalles.'
        }
        failure {
            echo 'Alguna prueba falló. Revisa los logs para más detalles. Y para el resultado de las pruebas, revisa el archivo report.html en tu carpeta de trabajo.'
        }
    }
}