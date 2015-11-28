import socket

EOM = '---EOM'


def start_ir(host, port, ir, max_connections=1):
    # Setup socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(max_connections)
    conn, addr = s.accept()

    # Keep on listening
    while True:
        # accept new message
        newsock, address = s.accept()

        # receive questions from new connection
        message = recv_end(newsock)
        type, question = message.split(" ", 1)
        answers = ir.question(type, question)

        # formatting the answer
        '''
        12
        This is an example of a sentence all in one line .
        PathDep::nsubj::0::0::Forw::::|1|84|270|12
        PathDep::nsubj::0::0::Forw::::|1|84|271|12
        PathDep::nsubj::0::0::Forw::::|1|84|272|12
        PathDep::nsubj::0::0::Forw::::|1|84|273|12
        PathDep::nsubj::0::0::Forw::::|1|84|274|12
        PathDep::nsubj::0::0::Forw::::|1|84|275|12
        PathDep::nsubj::0::0::Forw::::|1|85|270|12
        PathDep::nsubj::0::0::Forw::::|1|85|271|12
        PathDep::nsubj::0::0::Forw::::|1|85|272|12
        ---
        13
        This is an example of a sentence all in one line .
        PathDep::nsubj::0::0::Forw::::|1|84|270|13
        ---
        14
        This is an example of a sentence all in one line .

        ---EOM
        '''
        formatted_answers = "\n---\n".join(
            ["\n".join([str(a[0]), a[1], a[2]])
                for a in answers]) + "\n---EOM"
        conn.send(formatted_answers)


# this makes sure that we receive a question in the following form:
#    any message here as long as it ends with---EOM
def recv_end(the_socket):
    total_data = []
    data = ''
    while True:
        data = the_socket.recv(8192)
        if EOM in data:
            total_data.append(data[:data.find(EOM)])
            break
        total_data.append(data)
        if len(total_data) > 1:

            # check if end_of_data was split
            last_pair = total_data[-2] + total_data[-1]
            if EOM in last_pair:
                total_data[-2] = last_pair[:last_pair.find(EOM)]
                total_data.pop()
                break

    return ''.join(total_data)
