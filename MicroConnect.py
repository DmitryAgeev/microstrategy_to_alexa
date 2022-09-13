from mstrio.microstrategy import Connection


def getanswer(slot):
    metric = 0
    metric_pm = 0
    base_url = "https://env-270933.customer.cloud.microstrategy.com/MicroStrategyLibrary/api"  # change it
    mstr_username = "mstr"  # change it
    mstr_password = "kcTCSvc5RGG7"  # change it
    project_name = "MicroStrategy Tutorial"  # change it
    report_id = "4EFEBFC2004B9A3A2CA2A6A2E8CEC5A1"  # change it
    conn = Connection(base_url, mstr_username, mstr_password, project_name=project_name,
                      login_mode=16)
    conn.connect()

    report_dataframe = conn.get_report(report_id=report_id)
    columns = report_dataframe.columns
    if slot in columns:
        metric = report_dataframe[slot].agg('sum')
        if slot + "_PM" in columns:
            metric_pm = report_dataframe[slot + "_PM"].agg('sum')
        else:
            print("Error PM")
    else:
        print("Error")

    return metric, metric_pm


if __name__ == '__main__':
    slot = "Revenue"
    print(getanswer(slot=slot))
