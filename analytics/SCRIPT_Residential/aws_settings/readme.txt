SCRIPT github:
- https://github.com/malikmayank/SCRIPT

Login into SCRIPT AWS instance:
- if haven't done so do:
  chmod 400 'FILENAME.pem'
- Accessing instance
  ssh -i FILENAME.pem ec2-user@PUBLIC_IP

Install anaconda3:
- wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
- follow steps on https://docs.anaconda.com/anaconda/install/linux/

Run:
- check if "source /home/ec2-user/anaconda3/etc/profile.d/conda.sh" is added to your ~/.bashrc 
  (if not present, add it manually)
- source ~/.bashrc

Create a conda environment with python3:
- conda create -n ENV_NAME python=3


Install basic packages (conda):
- mysql.connector: conda install -c anaconda mysql-connector-python
- nb_conda: conda install -c anaconda nb_conda
- pandas: conda install -c anaconda pandas
- sqlalchemy: conda install -c anaconda sqlalchemy
- git: conda install -c anaconda git

Run:
- aws configure
- enter Access Key, Secret Key, and Region (usually us-west-2) 
  [if you don’t have access key and secret key got to IAM on AWS,
   select your user name and under Security credentials create Access Key]


Connecting to Jupyter Notebook from AWS:
- Type:
  jupyter notebook --no-browser --port=8888
- Open a new terminal and type:
  ssh -i FILENAME.pem -L 8000:localhost:8888 ec2-user@PUBLIC_IP
  example: ssh -i gustavoAWS.pem -L 8000:localhost:8888 ec2-user@34.222.137.103
- Open your browser and navigate to:
  localhost:8000
