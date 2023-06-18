pipeline{
    agent any
    
    stages{
        stage('Preparation'){
            steps{
                sh 'rm -rf imitation_game'
                sh 'git clone -b mlops --single-branch https://github.com/stibiumghost/imitation_game'
            }
        }
        
        stage ('Install Libraries') {
            steps{
                sh 'cd imitation_game'
                sh 'pip3 install -r requirements.txt'
            }
        }
        
        stage('Download Files'){
            steps{
                sh 'cd imitation_game'
                sh 'dvc pull'
            }
        }
        
        stage ('Run Tests'){
            steps{
                sh 'cd imitation_game'
                sh 'pytest'
            }
        }
        
        stage ('Docker Build'){
            steps{
                sh 'cd imitation_game'
                sh 'docker build -t imitation_game_image .'
            }
        }
    }
}