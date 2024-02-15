import logging
import random
import re
import socket
import threading
import time

localIP = "127.0.0.1"

localPort = 5353

bufferSize = 1024


file_address = "/etc/myhosts"       # myhosts is a file which has a list like:
                                    # server_ipaddr1    server_name1
                                    # server_ipaddr2    server_name2


print("UDP server up and listening")

class DNSServer():

    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((localIP, localPort))
        self.clients_list = []


    def listen_clients(self):
        while True:
            msg, client = self.sock.recvfrom(1024)
            logging.info('Received data from client %s: %s', client, msg)
            t = threading.Thread(target=self.talk_to_client, args=(msg,client))
            t.start()

    def talk_to_client(self,message,address):

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)

        # parsing the dns query
        transaction_id = message[0:2]
        questions = message[4:6]
        authority_RRs = message[8:10]
        additional_RRs = message[10:12]
        name_arr = []

        i = 12;
        while True:
            if message[i] == 0:
                break
            i = i + 1

        x = 12
        while True:
            if x == i:
                break
            number_of_bytes = message[x]
            name_arr.append(message[x + 1: x + 1 + number_of_bytes])
            x = x + number_of_bytes + 1

        name_arr_decoded = ""
        for k in name_arr:
            name_arr_decoded = name_arr_decoded + k.decode("utf-8") + "."
        name_arr_decoded = name_arr_decoded[:-1]
        i = i + 1

        type_a = message[i: i + 2]
        class_in = message[i + 2: i + 4]
        queries = message[12: i + 4]


        # stage 2: create answer dns-packet
        transaction_id_ans = transaction_id
        flags_ans = 0x8180.to_bytes(2, 'big')
        questions_ans = questions
        answer_RRs_ans = questions
        authority_RRs_ans = authority_RRs
        additional_RRs_ans = additional_RRs
        queries_ans = queries
        additional_records_ans = 0x0000290200000000000000.to_bytes(11, 'big')
        name_ans = 0xc00c.to_bytes(2, 'big')
        type_a_ans = type_a
        class_in_ans = class_in
        ttl_ans = 0x0000003c.to_bytes(4, 'big')
        data_length_ans = 0x0004.to_bytes(2, 'big')

        # read the file based on name_arr
        with open(file_address, "r") as f:
            content = f.readlines()

        flag = 0
        for line in content:
            if name_arr_decoded in line:
                flag = 1
                chosen_str = line
                break

        if flag == 0:
            time.sleep(random.uniform(0, 0.1))
            flags_ans = 0x81a3.to_bytes(2, 'big')
            authoritative_nameservers_ans = 0x00000600010001517a004001610c726f6f742d73657276657273036e657400056e73746c640c766572697369676e2d67727303636f6d00789639bd000007080000038400093a8000015180.to_bytes(
                75, 'big')

            not_found_answer = transaction_id_ans + flags_ans + questions_ans + answer_RRs_ans + authority_RRs_ans + additional_RRs_ans + queries_ans + authoritative_nameservers_ans + additional_records_ans
            self.sock.sendto(not_found_answer, address)
            return

        ip_ans_string = re.split(' |\t', chosen_str)[0]
        ip_arr = ip_ans_string.split(".")
        ip0 = int(ip_arr[0]).to_bytes(1, 'big')
        ip1 = int(ip_arr[1]).to_bytes(1, 'big')
        ip2 = int(ip_arr[2]).to_bytes(1, 'big')
        ip3 = int(ip_arr[3]).to_bytes(1, 'big')

        final_answer = transaction_id_ans + flags_ans + questions_ans + answer_RRs_ans + authority_RRs_ans + additional_RRs_ans + queries_ans + name_ans + type_a_ans + class_in_ans + ttl_ans + data_length_ans + ip0 + ip1 + ip2 + ip3 + additional_records_ans

        self.sock.sendto(final_answer, address)