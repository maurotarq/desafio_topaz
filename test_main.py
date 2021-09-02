from main import *
import pytest


def test_tick_advance():
    server1 = Server(4, 2)
    server1._users['Task 1'] = 0
    server1._users['Task 2'] = 1
    server1.tick_advance()

    assert server1._users['Task 1'] == 1 and server1._users['Task 2'] == 2 and server1.active_ticks == 1


def test_get_users_fill():
    server1 = Server(4, 2)
    server1.get_users(4)

    assert len(server1.users) == 2


def test_get_users_surplus():
    server1 = Server(4, 2)
    surplus = server1.get_users(4)

    assert surplus == 2


def test_delete_users():
    server1 = Server(4, 5)
    server1._users['Task 0'] = 4
    server1._users['Task 1'] = 3
    server1.tick_advance()

    assert len(server1.users) == 1


def test_input_data():
    data = input_data('test_input.txt')

    assert data['task_time'] == 4 and data['max_users'] == 2 and data['new_users'] == [1, 3, 0, 1, 0, 1]


def test_fill_servers():
    server1 = Server(4, 2)
    server2 = Server(4, 2)
    server3 = Server(4, 2)
    servers = [server1, server2, server3]

    server1.get_users(1)
    server2.get_users(1)

    fill_servers(2, servers)

    assert len(server1.users) == len(server2.users) and len(server3.users) == 0


def test_create_servers():
    server1 = Server(4, 2)
    server2 = Server(4, 2)
    servers = [server1, server2]

    servers = create_servers(7, servers, 4, 2)

    assert len(servers) == 4


def test_delete_check1():
    server1 = Server(4, 2)
    server2 = Server(4, 2)
    server2._users['Task 0'] = 4
    server2._users['Task 1'] = 1

    server1.get_users(2)
    for _ in range(4):
        server1.tick_advance()

    assert delete_check(server1) == True and delete_check(server2) == False


def test_user_output():
    servers = create_servers(6, [], 4, 2)

    data = user_output(servers)

    assert data == [2, 2, 2]


def test_total_cost():
    servers = create_servers(7, [], 4, 2)
    for server in servers:
        server.tick_advance()
        server.tick_advance()

    assert total_cost(servers) == 8


def test_run_servers1():
    data_input = input_data('test_input.txt')

    output = run_servers(data_input['new_users'], data_input['task_time'], data_input['max_users'], 'test_output.txt')
    assert output == [[1], [2, 2], [2, 2], [2, 2, 1], [1, 2, 1], [2], [2], [1], [1], 15]


def test_run_servers2():
    data_input = input_data('test_input2.txt')
    expected_output = [
        [3, 3, 1],
        [3, 3, 3],
        [3, 3, 3, 1],
        [3, 3, 3, 1],
        [3, 3, 3, 1],
        [2, 1],
        [3, 3, 1, 3],
        [3, 3, 2, 2],
        [3, 3, 2, 2],
        [3, 3, 2, 2],
        [3, 3, 2, 2],
        [2, 1],
        [2, 2],
        [3, 2],
        [2, 3, 3],
        [2, 3, 3],
        [2, 2, 2],
        [2, 1, 1],
        [2, 1],
        60
    ]

    output = run_servers(data_input['new_users'], data_input['task_time'], data_input['max_users'], 'test_output2.txt')
    assert output == expected_output
