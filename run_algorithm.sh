cd ~/SCRIPT/ec2setup/utils
python3 DataInfoSetup.py
cd ~/SCRIPT/ec2setup/algorithms/SmartCharging
python3 SmartChargingAlgorithm.py
cd ~/SCRIPT/ec2setup/algorithms/LoadForecasting
python3 LoadForecastingRunner.py
cd ~/SCRIPT/ec2setup/algorithms/CostBenefitAnalysis/cases/basecase/results/
python3 UploadToPostgres.py