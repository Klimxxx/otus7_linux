import subprocess
import datetime


current_datetime = datetime.datetime.now()
filename = current_datetime.strftime("%d-%m-%Y-%H-%M") + "-scan.txt"


def parse_ps_aux():
    result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    lines = output.splitlines()
    headers = lines[0].split()
    process_data = lines[1:]
    users = []
    total_mem = 0
    total_cpu = 0
    max_proc_name = ""
    max_memory = 0
    max_cpu_name = ""
    max_cpu = 0
    for line in process_data:
        parts = line.split(None, len(headers) - 1)
        mem_percentage = float(parts[3])
        cpu_percentage = float(parts[2])
        if mem_percentage > max_memory:
            max_memory = mem_percentage
            max_proc_name = str(parts[1])
        total_mem += mem_percentage
        total_cpu += cpu_percentage
        if cpu_percentage > max_cpu:
            max_cpu += cpu_percentage
            max_cpu_name = str(parts[1])
        users.append(parts[0])
    unique_users = set(users)
    with open(filename, "w") as file:
        file.write("Отчёт о состоянии системы:\n")
        # print('Отчёт о состоянии системы:')
        file.write("Пользователи системы: " + ", ".join(map(str, unique_users)) + "\n")
        # print("Пользователи системы: " + ", ".join(map(str, unique_users)))
        file.write(f"Процессов запущено: {len(lines)-1}\n")
        # print(f"Процессов запущено: {len(lines)-1}")
        file.write(f"Пользовательских процессов:\n")
        # print('Пользовательских процессов:')
        word_counts = {word: users.count(word) for word in set(users)}
        for word, count in word_counts.items():
            file.write(f"{word}: {count}")
            # print(f"{word}: {count}")
        file.write(f"Всего памяти используется: {round(total_mem, 1)}%\n")
        # print(f'Всего памяти используется: {round(total_mem, 1)}%')
        file.write(f"Всего CPU используется: {round(total_cpu, 1)}%\n")
        # print(f'Всего CPU используется: {round(total_cpu, 1)}%')
        file.write(f"Больше всего памяти использует: {max_proc_name[:20]}\n")
        # print(f'Больше всего памяти использует: {max_proc_name[:20]}')
        file.write(f"Больше всего CPU использует: {max_cpu_name[:20]}\n")
        # print(f'Больше всего CPU использует: {max_cpu_name[:20]}')


if __name__ == "__main__":
    parse_ps_aux()
