import json

ADDRESS_DATA_FILE = "data.json"
MAX_CONN = 1
RECV_SIZE = 4096

def get_address_data():
    with open(ADDRESS_DATA_FILE, "r") as f:
        return json.load(f)


def get_master_address():
    address_data = get_address_data()
    return address_data["master"]

'''
This function processes the client data and separates out the essential information
'''
def parse_request_info(client_addr, client_data):
    try:
        lines = client_data.splitlines()
        while lines[len(lines)-1] == '':
            lines.remove('')
        first_line_tokens = lines[0].split()
        url = first_line_tokens[1]

        url_pos = url.find("://")
        if url_pos != -1:
            protocol = url[:url_pos]
            url = url[(url_pos+3):]
        else:
            protocol = "http"

        # get port if any
        # get url path
        port_pos = url.find(":")
        path_pos = url.find("/")
        if path_pos == -1:
            path_pos = len(url)


        # change request path accordingly
        if port_pos==-1 or path_pos < port_pos:
            server_port = 80
            server_url = url[:path_pos]
        else:
            server_port = int(url[(port_pos+1):path_pos])
            server_url = url[:port_pos]

        # build up request for server
        first_line_tokens[1] = url[path_pos:]
        lines[0] = ' '.join(first_line_tokens)
        client_data = "\r\n".join(lines) + '\r\n\r\n'

        return {
            "server_port" : server_port,
            "server_url" : server_url,
            "total_url" : url,
            "client_data" : str.encode(client_data),
            "protocol" : protocol,
            "method" : first_line_tokens[0],
        }

    except Exception as e:
        print(e)
        return None
