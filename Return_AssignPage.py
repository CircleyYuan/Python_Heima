import socket

#接收每个客户进行服务
def request_handler(client_socket):
    recv_data = client_socket.recv(4096)
    if not recv_data:
        print("It has not link!")
        client_socket.close()
        return
    #对请求报文进行切割---》获取请求行 ----》 获取请求行中的用户请求资源的路径
    request_str_data = recv_data.decode()
    data_list = request_str_data.split("\r\n")
    #请求行就是第0个元素
    #print(data_list[0])
    path_info = data_list[0].split(' ')[1]
    #请求行的第一个数据 就是用户资源的请求路径
    print("User request line is %s "% path_info)
    if path_info == '/':
        path_info = '/grand.html'
    try:
        file = open("./static"+ path_info,"rb")
        file_data = file.read()
        file.close()

    except Exception as e:
        response_line = "HTTP/1.1 404 Not Found\r\n"
        response_head = "Server: CircleYuanWeb2.0\r\n"
        response_body = "ERROR!!!!"

        # 拼接报文
        response_data = (response_line + response_head + "\r\n").encode () + response_body
        client_socket.send (response_data)
    else:

        #print(recv_data)
        #给HTTP回复相应报文:响应行+响应头+空行+响应体

        #响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        #响应头
        response_head = "Server: CircleWeb2.0\r\n"
        #响应体
        response_body = file_data
    #拼接报文
        response_data = (response_line + response_head + "\r\n").encode() + response_body
        client_socket.send(response_data)

    finally:
        client_socket.close()
    # client_socket.send(response_data.encode())
    # client_socket.close()

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #套接字
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    server_socket.bind(('',9999))
    #监听被动套接字 设置已完成三次握手队列的长度
    server_socket.listen(128)
    #从队列中取出一个客户套接字用以服务
    while True:
        client_socket, client_addr = server_socket.accept()

        request_handler(client_socket)