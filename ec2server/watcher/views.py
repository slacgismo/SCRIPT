from django.shortcuts import render
from django.http import JsonResponse
import psycopg2

from watcher.tasks import my_task
from watcher.algorithms.load_controller.fit import load_control_fit

# Create your views here.

def progress_view(request):
    result = my_task.delay(100)
    return JsonResponse({'task_id': result.id})


def load_controller(request):
    if request.method == 'GET':
        return JsonResponse({'WARNING': 'This endpoint only support POST'})

    county = request.POST.get('county', '')
    rate_energy_peak = request.POST.get('rate_energy_peak', '')
    rate_energy_partpeak = request.POST.get('rate_energy_partpeak', '')
    rate_energy_offpeak = request.POST.get('rate_energy_offpeak', '')
    rate_demand_peak = request.POST.get('rate_demand_peak', '')
    rate_demand_partpeak = request.POST.get('rate_demand_partpeak', '')
    rate_demand_overall = request.POST.get('rate_demand_overall', '')

    # TODO: check if the config is in the database, get db config from env var
    conn = psycopg2.connect(
        host=db_host,
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
        port=db_port
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM script_config_load_controller" + \
        " WHERE county_id='{}' AND rate_energy_peak={} AND rate_energy_partpeak={} AND rate_energy_offpeak={}AND rate_demand_peak={} AND rate_demand_partpeak={} AND rate_demand_overall={})".format(
            county, rate_energy_peak, rate_energy_partpeak, rate_energy_offpeak,
            rate_demand_peak, rate_demand_partpeak, rate_demand_overall
        )
    )
    sql_result = cur.fetchone()
    if sql_result is None:
        res = JsonResponse({'Error': 'Config not found'})
    else:
        # TODO: check if the results is in the database
        cur.execute("SELECT * FROM script_algorithm_load_controller" + \
            " WHERE config_id={}".format(sql_result['id']))
        sql_result = cur.fetchone()
        if sql_result is not None:
            res = JsonResponse(sql_result)
        else:
            # It will take a while to compute(async)
            result = load_control_fit.delay(county, rate_energy_peak, rate_energy_partpeak, rate_energy_offpeak, rate_demand_peak, rate_demand_partpeak, rate_demand_overall)
            res = JsonResponse({'task_id': result.id})

    # Close communication with the database
    cur.close()
    conn.close()
    return res

