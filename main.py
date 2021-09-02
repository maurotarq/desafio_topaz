from random import choice


class Server:
    def __init__(self, task_time, max_users):
        self.active_ticks = 0
        self._users = {}
        self._task_time = task_time
        self._max_users = max_users

    @property
    def users(self):
        return self._users

    @property
    def task_time(self):
        return self._task_time

    def server_cost(self):
        return self.active_ticks

    def tick_advance(self):
        for key in self.users:
            self._users[key] += 1

        self.delete_users()

        if len(self.users) > 0:
            self.active_ticks += 1

    def get_users(self, users):
        users = users

        while len(self.users) < self._max_users and users > 0:
            if f'Task {len(self.users)}' not in self._users.keys():
                self._users[f'Task {len(self.users)}'] = 0
            else:
                self._users[f'Task {self.available_slots()}'] = 0
            users -= 1

        return users

    def available_slots(self):
        used_slots = []
        possible_slots = list(range(self._max_users))

        for key in self.users.keys():
            used_slots.append(int(key.strip('Task ')))
        possible_slots = list(set(possible_slots) - set(used_slots))

        return choice(possible_slots)

    def delete_users(self):
        delete = []

        for key in self.users:
            if self._users[key] > self.task_time:
                delete.append(key)

        for items in delete:
            del self._users[items]


def input_data(file):
    with open(file, 'r') as file:
        data = dict(task_time=int(file.readline()))
        data['max_users'] = int(file.readline())
        new_users = []

        for lines in file:
            new_users.append(int(lines))

        data['new_users'] = new_users

        if data['task_time'] > 10 or data['task_time'] < 1:
            raise ValueError('ttask só pode estrar entre 1 e 10, insira novo input')
        if data['max_users'] > 10 or data['max_users'] < 1:
            raise ValueError('umax só pode estar entre 1 e 10, insira novo input')

    return data


def create_servers(users, server_list, task_time, max_users):
    users = fill_servers(users, server_list)

    while users > 0:
        server_list.append(Server(task_time, max_users))
        users = fill_servers(users, server_list)

    return server_list


def fill_servers(users, server_list):
    if users > 0:
        for server in server_list:
            if not delete_check(server) and len(server.users) > 0:
                users = server.get_users(users)

        for server in server_list:
            users = server.get_users(users)

    return users


def delete_check(server):
    task_limit = server.task_time
    result = True

    for user in server.users.values():
        if user != task_limit:
            result = False
            break

    return result


def task_end(server_list):
    for server in server_list:
        if len(server.users) > 0:
            return True

    return False


def user_output(server_list):
    data = []

    for server in server_list:
        server.tick_advance()
        temp = len(server.users)

        if temp != 0:
            data.append(temp)

    return data


def total_cost(server_list):
    total_ticks = 0

    for server in server_list:
        total_ticks += server.server_cost()

    return total_ticks


def data_output(file, users_out, cost):
    with open(file, 'w+') as file:
        test_output = []

        for elements in users_out:
            line = ''
            test_output.append(elements)
            for elem in elements:
                line += str(elem) + ','
            file.write(f'{line[:-1]}\n')

        test_output.append(cost)
        file.write(str(cost))

    return test_output


def run_servers(new_users, task_time, max_users, output_file):
    servers = []
    output = []

    for user in new_users:
        servers = create_servers(user, servers, task_time, max_users)
        output.append(user_output(servers))

    while task_end(servers):
        output.append(user_output(servers))

    output = list(filter(None, output))

    test_output = data_output(output_file, output, total_cost(servers))
    return test_output


if __name__ == '__main__':
    data_input = input_data('input.txt')

    run_servers(data_input['new_users'], data_input['task_time'], data_input['max_users'], 'output.txt')
