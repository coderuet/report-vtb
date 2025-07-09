from http.server import BaseHTTPRequestHandler, HTTPServer
from code.utils.vtb_service import get_transactions
from code.utils.gcloud import upload_many_blobs_with_transfer_manager
from code.utils.helper import clean_data, write_file
from code.constants.env_constants import EnvCons
from urllib.parse import urlparse, parse_qs


def main_func(start_date: str, end_date: str):
    transactions = get_transactions(
        start_date=start_date, end_date=end_date, limit=1000)
    clean_trans = clean_data(transactions=transactions)
    list_file = write_file(clean_trans)
    upload_many_blobs_with_transfer_manager(bucket_name=EnvCons.BUCKET_NAME,
                                            source_directory=EnvCons.PATH_FOLDER_SAVE, filenames=list_file)


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if 'start-date' not in query_params or 'end-date' not in query_params:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(
                b"400 Bad Request: missing params")
            return

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        main_func(
            start_date=query_params["start-date"], end_date=query_params["end-date"])
        response_text = f"response v1"
        self.wfile.write(response_text.encode("utf-8"))


def run():
    port = 8080  # Cloud Run requires the service to listen on port 8080
    httpd = HTTPServer(("", port), SimpleHandler)
    print(f"Listening on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
