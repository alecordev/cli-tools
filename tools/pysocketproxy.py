import sys
import time
import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG)


def clean_host(host_proxy):
    host_proxy = host_proxy.replace("Host: ", "")
    index_proxy_port = host_proxy.find(":")
    port_proxy = (
        host_proxy[index_proxy_port:].replace(":", "").replace("\r\n", "")
        if index_proxy_port != -1
        else 80
    )
    port_proxy = int(port_proxy)
    return (host_proxy, port_proxy)


def clean_data(data, webserver, port):
    data = data.decode()
    start = data[data.find("\r\n") + 2 :]
    host_proxy = start[: start.find("\r\n") + 2]
    new_host = "Host: "
    if port != 80:
        new_host += webserver + ":" + str(port)
    else:
        new_host += webserver
    new_host += "\r\n"

    addr_proxy = clean_host(host_proxy)
    return (data.replace(host_proxy, new_host), addr_proxy)


def clean_returned_data(data, webserver):
    data = data.decode()
    location = data[data.find("Location:") :]
    location = location[: location.find("\r\n")]
    location = location[location.find("http://") :]

    new_host = "Location: http://"
    new_host += webserver.replace("\r\n", "")
    new_host += location[7:][(location[7:].find("/")) :]

    return data.replace(location, new_host)


def proxy_server(webserver, port, conn, addr, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        data, addr_proxy = clean_data(data, webserver, port)
        logging.info("Data:", data)
        logging.info("For:", webserver)
        s.send(data.encode())

        while True:
            reply = s.recv(buffer_size)
            if len(reply) > 0:
                # falta tratar o retorno pelo proxy
                reply = clean_returned_data(reply, addr_proxy[0])
                conn.send(reply.encode())

                dar = float(len(reply))
                dar = float(dar / 1024.0)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)

                logging.info(
                    "[*] Request Done: %s => %s <= " % (str(addr[0]), str(dar))
                )
                time.sleep(0.001)
            else:
                break
        # s.close()
        # conn.close()
    except socket.error as e:
        logging.exception("Error in proxy_server")
        s.close()
        conn.close()
        sys.exit(1)
    finally:
        s.close()
        conn.close()


class Connection(threading.Thread):
    def __init__(self, conn, data, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.data = data
        self.addr = addr

    def run(self):
        conn = self.conn
        data = self.data
        addr = self.addr
        try:
            first_line = data.decode().split("\n")[0]
            url = first_line.split(" ")[1]

            http_pos = url.find("://")
            if http_pos == -1:
                temp = url
            else:
                temp = url[(http_pos + 3) :]

            port_pos = temp.find(":")

            webserver_pos = temp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(temp)
            webserver = ""
            port = -1
            if port_pos == -1 or webserver_pos < port_pos:
                port = 80
                webserver = temp[:webserver_pos]
            else:
                port = int((temp[(port_pos + 1) :])[: webserver_pos - port_pos - 1])
                webserver = temp[:port_pos]
            webserver = "www.google.com"
            port = 80
            proxy_server(webserver, port, conn, addr, data)
        except Exception as e:
            logging.exception("Error in run")
            conn.close()


def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", listening_port))
        s.listen(max_conn)
        logging.info("[*] Initializing Sockets ...Done")
        logging.info("[*] Sockets Binded Succefully ...")
        logging.info("[*] Sockets Started Succefully [%d]\n" % (listening_port))
    except Exception:
        logging.info("[*] Unable to Initialize Socket")
        sys.exit(2)
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            connection = Connection(conn, data, addr)
            connection.run()
        except KeyboardInterrupt:
            logging.info("\n[*] Proxy Server is Shuting Down ...")
            s.close()
            sys.exit(1)


try:
    listening_port = int(input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:
    logging.info("\n[*] User registration An Interrupt")
    logging.info("[*] Application Exiting")
    sys.exit()

max_conn = 5
buffer_size = 8129

start()
