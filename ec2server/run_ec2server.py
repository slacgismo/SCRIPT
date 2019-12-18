from watcher.algorithms.load_controller.load_control_algorithm import LoadControlAlgorithm

db_host = 'localhost'
db_port = 5433
table_name = 'script_config_load_controller'
postgres_db = 'scriptdb'
postgres_user = 'script_admin'
postgres_password = 'script_passwd'

# CRITICAL: MUST start local webserver(create tables) and insert all counties before inserting configs
# TODO: save model config to database
LoadControlAlgorithm.upload_config(db_host, db_port, table_name, postgres_db, postgres_user, postgres_password)

# TODO: start server
