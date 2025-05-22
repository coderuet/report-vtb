from .utils.vtb_service import get_transactions
from .utils.error import error_handler
from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from .constants.env_constants import EnvCons
import json
import os
from .utils.gcloud import upload_many_blobs_with_transfer_manager


@error_handler
def clean_data(transactions: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Remove unnecessary fields and group transactions by formatted processDate.

    Args:
        transactions (List): List of transactions from VTB.

    Returns:
        Dict: Transactions grouped by processDate in 'YYYY-MM-DD' format.
    """
    allowed_keys = {
        'remark', 'amount', 'processDate', 'trxId', 'dorC',
        'corresponsiveAccount', 'corresponsiveName', 'receivingBranchName', 'sendingBranchName'
    }

    grouped = defaultdict(list)

    for trx in transactions:
        filtered_trx = {k: v for k, v in trx.items() if k in allowed_keys}
        formatted_date = str(datetime.strptime(
            filtered_trx["processDate"], "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d"))
        # Grouped by year-month
        grouped[formatted_date[:-3]].append(filtered_trx)

    return dict(grouped)


@error_handler
def write_file(grouped_transactions: Dict) -> List[str]:
    """Save file with grouped transactions

    Args:
        grouped_transactions (Dict): Transactions grouped by month with key is YYYY-MM 
        and key is list of transactions in that month
    Returns:
        List[str]: List file name
    """
    list_file: List[str] = []
    for key in grouped_transactions:
        print(key)
        file_path = os.path.join(EnvCons.PATH_FOLDER_SAVE, f"{key}.json")
        f = open(file_path, "w")
        f.write(json.dumps(grouped_transactions[key]))
        f.close()
        list_file.append(key)
    return list_file


if __name__ == "__main__":
    # Get argument
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--start-date", dest="start_date", required=True)
    # parser.add_argument("--end-date", dest="end_date", required=True)
    # args = parser.parse_args()
    # start_date = args.start_date
    # end_date = args.end_date

    start_date = "2025-03-30"
    end_date = "2025-04-30"

    transactions = get_transactions(
        start_date=start_date, end_date=end_date, limit=1000)
    clean_trans = clean_data(transactions=transactions)
    list_file = write_file(clean_trans)
    upload_many_blobs_with_transfer_manager
