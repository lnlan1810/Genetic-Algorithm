#генетический алгоритм
import requests
import random
import folium


# Получение матрицы расстояний из API 2ГИС
def fetch_distance_matrix(api_key, points):
    """
    Функция отправляет запрос к API 2ГИС для получения матрицы расстояний между точками.

    :param api_key: API-ключ для доступа к сервису 2ГИС.
    :param points: Список точек (координат) в формате [{"lat": ..., "lon": ...}, ...].
    :return: Матрица расстояний или None в случае ошибки.
    """
    url = f"https://routing.api.2gis.com/get_dist_matrix?key={api_key}&version=2.0"
    payload = {"points": points, "sources": list(range(len(points))), "targets": list(range(len(points)))}
    headers = {"Content-Type": "application/json"}

    try:
        # Отправляем POST-запрос к API
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  
        data = response.json()  

        # Инициализируем матрицу расстояний бесконечными значениями
        num_points = len(points)
        distance_matrix = [[float('inf')] * num_points for _ in range(num_points)]

        # Заполняем матрицу значениями из ответа API
        for route in data.get("routes", []):
            source_id = route["source_id"]
            target_id = route["target_id"]
            distance = route["distance"]
            distance_matrix[source_id][target_id] = distance

        return distance_matrix
    except requests.exceptions.RequestException as e:
        print(f"Error fetching distance matrix: {e}")
        return None


# Генерация начальной популяции
def start_population(size, cities):
    """
    Создает начальную популяцию случайных маршрутов.

    :param size: Размер популяции.
    :param cities: Количество городов (точек).
    :return: Список маршрутов (каждый маршрут - это список индексов городов).
    """
    return [random.sample(range(cities), cities) for _ in range(size)]


# Кроссовер
def crossover(parents):
    """
    Генерирует потомков на основе родительских маршрутов с использованием кроссовера.

    :param parents: Список родительских маршрутов.
    :return: Список потомков.
    """
    offspring = []
    for i in range(len(parents)):
        for j in range(i + 1, len(parents)):
            offspring.append(make_child(parents[i], parents[j]))
            offspring.append(make_child(parents[j], parents[i]))
    return offspring


def make_child(parent1, parent2):
    """
    Создает потомка, комбинируя гены двух родителей.

    :param parent1: Первый родитель.
    :param parent2: Второй родитель.
    :return: Потомок.
    """
    cut = len(parent1) // 2 
    child = parent1[:cut] + [gene for gene in parent2 if gene not in parent1[:cut]]
    return child


# Мутация
def mutation(generations, mutation_rate):
    """
    Применяет случайные мутации к поколениям с заданной вероятностью.

    :param generations: Список маршрутов.
    :param mutation_rate: Вероятность мутации.
    :return: Мутированные поколения.
    """
    for generation in generations:
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(generation)), 2)  
            generation[i], generation[j] = generation[j], generation[i]  
    return generations


# Селекция
def selection(path_costs, generations):
    """
    Отбирает маршруты для создания нового поколения на основе их стоимости.

    :param path_costs: Список стоимостей маршрутов.
    :param generations: Список маршрутов.
    :return: Список выбранных маршрутов (родителей).
    """
    total_cost = sum(path_costs)
    probabilities = [(1 / cost) / total_cost for cost in path_costs]  
    return random.choices(generations, probabilities, k=4)


# Оценка стоимости путей
def evaluation(generations, distance_matrix):
    """
    Вычисляет стоимость (длину) каждого маршрута в популяции.

    :param generations: Список маршрутов.
    :param distance_matrix: Матрица расстояний между точками.
    :return: Список стоимостей маршрутов.
    """
    path_costs = []
    for generation in generations:
        cost = sum(distance_matrix[generation[i]][generation[i + 1]] for i in range(len(generation) - 1))
        cost += distance_matrix[generation[-1]][generation[0]]  
        path_costs.append(cost)
    return path_costs


# Отображение пути на карте
def plot_path_on_map(points, best_path):
    """
    Визуализирует лучший маршрут на карте и сохраняет его в файл HTML.

    :param points: Список точек (координат).
    :param best_path: Лучший маршрут (индексы точек).
    """
    map_center = points[0] 
    m = folium.Map(location=[map_center["lat"], map_center["lon"]], zoom_start=13)

    # Отображение точек
    for idx, point in enumerate(points):
        folium.Marker([point["lat"], point["lon"]], popup=f"Point {idx}").add_to(m)

    # Отображение маршрута
    path_coordinates = [(points[idx]["lat"], points[idx]["lon"]) for idx in best_path + [best_path[0]]]
    folium.PolyLine(path_coordinates, color="blue", weight=2.5, opacity=0.8).add_to(m)

    m.save("tsp_route.html")  
    print("Path plotted on map and saved as 'tsp_route.html'.")


# Основная программа
if __name__ == '__main__':
    API_KEY = "3f45ee79-34ae-45f2-9e2c-39f2bc266f03" 
    points = [
        {"lat": 55.799551, "lon": 49.105407}, # 0. Казанский кремль 
        {"lat": 55.787632, "lon": 49.122169}, # 1. Площадь Тукая
        {"lat": 55.820708, "lon": 49.157401}, # 2. Ак Барс Арена 
        {"lat": 55.801506, "lon": 49.125469}, # 3. Национальная библиотека Республики Татарстан 
        {"lat": 55.812824, "lon": 49.10825}, # 4. Казан, центр семьи 
        {"lat": 55.783055, "lon": 49.117727 }, # 5. Площадь у театра им. Г. Камала 
    ]

    print("Fetching distance matrix from 2GIS...")
    distance_matrix = fetch_distance_matrix(API_KEY, points)

    if not distance_matrix:
        print("Failed to fetch distance matrix. Exiting.")
        exit()

    # Параметры генетического алгоритма
    population_size = 200
    mutation_rate = 0.001
    max_generations = 500
    num_cities = len(points)

    # Запуск генетического алгоритма
    population = start_population(population_size, num_cities)
    best_cost = float('inf')
    best_path = []

    for generation in range(max_generations):
        path_costs = evaluation(population, distance_matrix) 
        min_cost = min(path_costs) 
        if min_cost < best_cost:
            best_cost = min_cost
            best_path = population[path_costs.index(min_cost)]
            print(f"Generation {generation}: Best Cost = {best_cost}")

        parents = selection(path_costs, population)  
        offspring = crossover(parents) 
        population = mutation(offspring, mutation_rate)  

    print("\n=== Final Result ===")
    print(f"Best path: {best_path}")
    print(f"Cost: {best_cost}")

    # Отобразить путь на карте
    plot_path_on_map(points, best_path)
