from datetime import timedelta, datetime

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

# Slack bot for Google analytics about Users in Core.Today
from slack_bot import google_analytics_api as gaa
from slack_bot import make_plt_charts as mpc
from slack_bot import slack_bot as sb

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Daeyeop',
    'depends_on_past': False,
    'email': ['daeyeop@core.today'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


def is_daily():
    weekday = datetime.today().weekday()
    if weekday in [1,2,3,4]:
        return True
    else:
        return False

def google_analytics():
    if is_daily():
        gaa.daily()
    else:
        gaa.weekly()

def make_plt_charts():
    if is_daily():
        mpc.daily()
    else:
        mpc.weekly()

def send_slack():
    slack_bot = sb.SlackBot()
    if is_daily():
        slack_bot.send_daily()
    else:
        slack_bot.send_weekly()

import pendulum
KST = pendulum.timezone('Asia/Seoul')

with DAG(
    'send_report_to_slack',
    default_args=default_args,
    description='send google analytic report to slack',
    schedule_interval='* * * * *',
    start_date=datetime(2021,1,1, tzinfo = KST),
    tags=['slack bot'],
    catchup=False
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = PythonOperator(
        task_id='google_analytics',
        python_callable=google_analytics
    )

    t2 = PythonOperator(
        task_id='make_plt_charts',
        python_callable=make_plt_charts
    )

    t3 = PythonOperator(
        task_id='send_slack',
        python_callable=send_slack
    )

    t1 >> t2 >> t3
