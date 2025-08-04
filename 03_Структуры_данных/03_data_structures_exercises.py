#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Структуры данных Python

Этот файл содержит практические упражнения для закрепления знаний:
- Работа со списками и их методами
- Использование кортежей и именованных кортежей
- Операции со словарями и множествами
- Выбор оптимальной структуры данных
- Работа с вложенными структурами

Каждое упражнение имеет описание задачи и закомментированное решение.
"""

import random
import time
from collections import namedtuple, defaultdict, Counter
import copy


def exercise_01():
    """
    Упражнение 1: Управление списком задач
    
    Создайте систему управления задачами с функциями:
    1. Добавление новой задачи
    2. Отметка задачи как выполненной
    3. Удаление задачи
    4. Вывод всех задач с их статусом
    5. Подсчет выполненных и невыполненных задач
    """
    print("=== Упражнение 1: Управление списком задач ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # class TaskManager:
    #     def __init__(self):
    #         self.tasks = []  # Список кортежей (task, completed)
    #     
    #     def add_task(self, task):
    #         """Добавить новую задачу"""
    #         self.tasks.append((task, False))
    #         print(f"Добавлена задача: '{task}'")
    #     
    #     def complete_task(self, task_index):
    #         """Отметить задачу как выполненную"""
    #         if 0 <= task_index < len(self.tasks):
    #             task, _ = self.tasks[task_index]
    #             self.tasks[task_index] = (task, True)
    #             print(f"Задача '{task}' выполнена!")
    #         else:
    #             print("Неверный номер задачи!")
    #     
    #     def remove_task(self, task_index):
    #         """Удалить задачу"""
    #         if 0 <= task_index < len(self.tasks):
    #             removed_task = self.tasks.pop(task_index)
    #             print(f"Удалена задача: '{removed_task[0]}'")
    #         else:
    #             print("Неверный номер задачи!")
    #     
    #     def show_tasks(self):
    #         """Показать все задачи"""
    #         if not self.tasks:
    #             print("Нет задач!")
    #             return
    #         
    #         print("Список задач:")
    #         for i, (task, completed) in enumerate(self.tasks):
    #             status = "✓" if completed else "○"
    #             print(f"{i+1}. {status} {task}")
    #     
    #     def get_statistics(self):
    #         """Получить статистику"""
    #         completed = sum(1 for _, done in self.tasks if done)
    #         total = len(self.tasks)
    #         pending = total - completed
    #         
    #         print(f"\nСтатистика:")
    #         print(f"Всего задач: {total}")
    #         print(f"Выполнено: {completed}")
    #         print(f"Осталось: {pending}")
    #         if total > 0:
    #             print(f"Прогресс: {completed/total*100:.1f}%")
    # 
    # # Демонстрация использования
    # tm = TaskManager()
    # tm.add_task("Изучить списки Python")
    # tm.add_task("Написать код")
    # tm.add_task("Протестировать приложение")
    # tm.show_tasks()
    # tm.complete_task(0)
    # tm.show_tasks()
    # tm.get_statistics()


def exercise_02():
    """
    Упражнение 2: Анализатор текста с множествами
    
    Создайте анализатор текста, который:
    1. Находит уникальные слова
    2. Определяет общие слова между текстами
    3. Находит слова, уникальные для каждого текста
    4. Подсчитывает частоту символов
    5. Анализирует использование знаков препинания
    """
    print("=== Упражнение 2: Анализатор текста с множествами ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # import string
    # 
    # def analyze_texts(text1, text2):
    #     """Анализ двух текстов"""
    #     
    #     # Предобработка текстов
    #     def preprocess(text):
    #         # Приводим к нижнему регистру и удаляем знаки препинания
    #         text = text.lower()
    #         text = text.translate(str.maketrans('', '', string.punctuation))
    #         return set(text.split())
    #     
    #     words1 = preprocess(text1)
    #     words2 = preprocess(text2)
    #     
    #     print(f"Текст 1: {len(words1)} уникальных слов")
    #     print(f"Текст 2: {len(words2)} уникальных слов")
    #     
    #     # Общие слова
    #     common_words = words1 & words2
    #     print(f"\nОбщие слова ({len(common_words)}): {sorted(common_words)}")
    #     
    #     # Уникальные для каждого текста
    #     unique_to_text1 = words1 - words2
    #     unique_to_text2 = words2 - words1
    #     
    #     print(f"\nУникальные для текста 1 ({len(unique_to_text1)}): {sorted(unique_to_text1)}")
    #     print(f"Уникальные для текста 2 ({len(unique_to_text2)}): {sorted(unique_to_text2)}")
    #     
    #     # Коэффициент похожести (Жаккара)
    #     jaccard_similarity = len(common_words) / len(words1 | words2)
    #     print(f"\nКоэффициент похожести Жаккара: {jaccard_similarity:.2f}")
    #     
    #     # Анализ символов
    #     def analyze_characters(text):
    #         chars = set(text.lower())
    #         letters = chars & set(string.ascii_lowercase)
    #         digits = chars & set(string.digits)
    #         punctuation = chars & set(string.punctuation)
    #         
    #         return {
    #             'letters': letters,
    #             'digits': digits,
    #             'punctuation': punctuation
    #         }
    #     
    #     chars1 = analyze_characters(text1)
    #     chars2 = analyze_characters(text2)
    #     
    #     print(f"\nАнализ символов:")
    #     print(f"Буквы в тексте 1: {len(chars1['letters'])}")
    #     print(f"Буквы в тексте 2: {len(chars2['letters'])}")
    #     print(f"Общие знаки препинания: {chars1['punctuation'] & chars2['punctuation']}")
    # 
    # # Тестовые тексты
    # text1 = "Python - это мощный язык программирования. Он прост в изучении."
    # text2 = "Java - популярный язык программирования. Он используется для создания приложений."
    # 
    # analyze_texts(text1, text2)


def exercise_03():
    """
    Упражнение 3: Система рекомендаций фильмов
    
    Создайте систему рекомендаций на основе словарей:
    1. Храните данные о пользователях и их оценках фильмов
    2. Найдите пользователей с похожими вкусами
    3. Рекомендуйте фильмы на основе оценок других пользователей
    4. Вычислите средний рейтинг фильмов
    5. Найдите самые популярные жанры
    """
    print("=== Упражнение 3: Система рекомендаций фильмов ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # class MovieRecommendationSystem:
    #     def __init__(self):
    #         # Структура: {user_id: {movie_id: rating}}
    #         self.user_ratings = {}
    #         # Структура: {movie_id: {'title': str, 'genres': set}}
    #         self.movies = {}
    #     
    #     def add_movie(self, movie_id, title, genres):
    #         """Добавить фильм"""
    #         self.movies[movie_id] = {
    #             'title': title,
    #             'genres': set(genres)
    #         }
    #     
    #     def add_rating(self, user_id, movie_id, rating):
    #         """Добавить оценку"""
    #         if user_id not in self.user_ratings:
    #             self.user_ratings[user_id] = {}
    #         self.user_ratings[user_id][movie_id] = rating
    #     
    #     def get_similar_users(self, user_id, min_common_movies=2):
    #         """Найти пользователей с похожими вкусами"""
    #         if user_id not in self.user_ratings:
    #             return []
    #         
    #         user_movies = set(self.user_ratings[user_id].keys())
    #         similar_users = []
    #         
    #         for other_user_id, other_ratings in self.user_ratings.items():
    #             if other_user_id == user_id:
    #                 continue
    #             
    #             other_movies = set(other_ratings.keys())
    #             common_movies = user_movies & other_movies
    #             
    #             if len(common_movies) >= min_common_movies:
    #                 # Вычисляем коэффициент корреляции (упрощенно)
    #                 user_ratings_common = [self.user_ratings[user_id][m] for m in common_movies]
    #                 other_ratings_common = [other_ratings[m] for m in common_movies]
    #                 
    #                 # Простая метрика похожести
    #                 similarity = 1 / (1 + sum(abs(r1 - r2) for r1, r2 in zip(user_ratings_common, other_ratings_common)))
    #                 
    #                 similar_users.append((other_user_id, similarity))
    #         
    #         return sorted(similar_users, key=lambda x: x[1], reverse=True)
    #     
    #     def recommend_movies(self, user_id, num_recommendations=5):
    #         """Рекомендовать фильмы"""
    #         if user_id not in self.user_ratings:
    #             return []
    #         
    #         user_movies = set(self.user_ratings[user_id].keys())
    #         similar_users = self.get_similar_users(user_id)
    #         
    #         # Собираем рекомендации от похожих пользователей
    #         recommendations = defaultdict(list)
    #         
    #         for similar_user_id, similarity in similar_users[:5]:  # Топ-5 похожих
    #             for movie_id, rating in self.user_ratings[similar_user_id].items():
    #                 if movie_id not in user_movies and rating >= 4:  # Хорошие оценки
    #                     recommendations[movie_id].append(rating * similarity)
    #         
    #         # Вычисляем средневзвешенный рейтинг
    #         avg_recommendations = []
    #         for movie_id, ratings in recommendations.items():
    #             avg_rating = sum(ratings) / len(ratings)
    #             movie_title = self.movies.get(movie_id, {}).get('title', f'Movie {movie_id}')
    #             avg_recommendations.append((movie_id, movie_title, avg_rating))
    #         
    #         return sorted(avg_recommendations, key=lambda x: x[2], reverse=True)[:num_recommendations]
    #     
    #     def get_movie_stats(self):
    #         """Статистика по фильмам"""
    #         movie_ratings = defaultdict(list)
    #         genre_popularity = defaultdict(int)
    #         
    #         for user_ratings in self.user_ratings.values():
    #             for movie_id, rating in user_ratings.items():
    #                 movie_ratings[movie_id].append(rating)
    #                 
    #                 # Подсчет популярности жанров
    #                 if movie_id in self.movies:
    #                     for genre in self.movies[movie_id]['genres']:
    #                         genre_popularity[genre] += 1
    #         
    #         # Средний рейтинг фильмов
    #         avg_ratings = {}
    #         for movie_id, ratings in movie_ratings.items():
    #             avg_ratings[movie_id] = sum(ratings) / len(ratings)
    #         
    #         # Топ фильмов
    #         top_movies = sorted(avg_ratings.items(), key=lambda x: x[1], reverse=True)[:5]
    #         
    #         # Популярные жанры
    #         popular_genres = sorted(genre_popularity.items(), key=lambda x: x[1], reverse=True)
    #         
    #         return {
    #             'top_movies': top_movies,
    #             'popular_genres': popular_genres,
    #             'total_movies': len(movie_ratings),
    #             'total_ratings': sum(len(ratings) for ratings in movie_ratings.values())
    #         }
    # 
    # # Демонстрация
    # rec_system = MovieRecommendationSystem()
    # 
    # # Добавляем фильмы
    # rec_system.add_movie(1, "Матрица", ["фантастика", "боевик"])
    # rec_system.add_movie(2, "Титаник", ["драма", "романтика"])
    # rec_system.add_movie(3, "Интерстеллар", ["фантастика", "драма"])
    # rec_system.add_movie(4, "Джон Уик", ["боевик", "триллер"])
    # rec_system.add_movie(5, "Начало", ["фантастика", "триллер"])
    # 
    # # Добавляем оценки пользователей
    # ratings_data = [
    #     ("user1", 1, 5), ("user1", 2, 3), ("user1", 3, 5),
    #     ("user2", 1, 4), ("user2", 4, 5), ("user2", 5, 4),
    #     ("user3", 2, 5), ("user3", 3, 4), ("user3", 1, 3),
    #     ("user4", 1, 5), ("user4", 3, 5), ("user4", 5, 5),
    # ]
    # 
    # for user_id, movie_id, rating in ratings_data:
    #     rec_system.add_rating(user_id, movie_id, rating)
    # 
    # # Получаем рекомендации
    # print("Рекомендации для user1:")
    # recommendations = rec_system.recommend_movies("user1")
    # for movie_id, title, score in recommendations:
    #     print(f"  {title}: {score:.2f}")
    # 
    # # Статистика
    # stats = rec_system.get_movie_stats()
    # print(f"\nСтатистика:")
    # print(f"Популярные жанры: {stats['popular_genres'][:3]}")


def exercise_04():
    """
    Упражнение 4: Инвентарь магазина с именованными кортежами
    
    Создайте систему управления инвентарем:
    1. Используйте именованные кортежи для товаров
    2. Отслеживайте количество, цену, категорию
    3. Вычисляйте общую стоимость инвентаря
    4. Найдите товары с низкими запасами
    5. Группируйте товары по категориям
    """
    print("=== Упражнение 4: Инвентарь магазина с именованными кортежами ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # Product = namedtuple('Product', ['id', 'name', 'category', 'price', 'quantity'])
    # 
    # class Inventory:
    #     def __init__(self):
    #         self.products = {}  # {product_id: Product}
    #     
    #     def add_product(self, product_id, name, category, price, quantity):
    #         """Добавить товар"""
    #         product = Product(product_id, name, category, price, quantity)
    #         self.products[product_id] = product
    #         print(f"Добавлен товар: {name}")
    #     
    #     def update_quantity(self, product_id, new_quantity):
    #         """Обновить количество товара"""
    #         if product_id in self.products:
    #             old_product = self.products[product_id]
    #             self.products[product_id] = old_product._replace(quantity=new_quantity)
    #             print(f"Обновлено количество {old_product.name}: {new_quantity}")
    #         else:
    #             print("Товар не найден!")
    #     
    #     def sell_product(self, product_id, quantity_sold):
    #         """Продать товар"""
    #         if product_id in self.products:
    #             product = self.products[product_id]
    #             if product.quantity >= quantity_sold:
    #                 new_quantity = product.quantity - quantity_sold
    #                 self.products[product_id] = product._replace(quantity=new_quantity)
    #                 total_price = product.price * quantity_sold
    #                 print(f"Продано {quantity_sold} шт. {product.name}. Выручка: {total_price:.2f}")
    #                 return total_price
    #             else:
    #                 print(f"Недостаточно товара! В наличии: {product.quantity}")
    #         else:
    #             print("Товар не найден!")
    #         return 0
    #     
    #     def get_low_stock_products(self, threshold=10):
    #         """Найти товары с низкими запасами"""
    #         low_stock = []
    #         for product in self.products.values():
    #             if product.quantity <= threshold:
    #                 low_stock.append(product)
    #         return sorted(low_stock, key=lambda p: p.quantity)
    #     
    #     def get_total_value(self):
    #         """Общая стоимость инвентаря"""
    #         total = sum(product.price * product.quantity for product in self.products.values())
    #         return total
    #     
    #     def group_by_category(self):
    #         """Группировка по категориям"""
    #         categories = defaultdict(list)
    #         for product in self.products.values():
    #             categories[product.category].append(product)
    #         return dict(categories)
    #     
    #     def get_category_stats(self):
    #         """Статистика по категориям"""
    #         categories = self.group_by_category()
    #         stats = {}
    #         
    #         for category, products in categories.items():
    #             total_value = sum(p.price * p.quantity for p in products)
    #             total_items = sum(p.quantity for p in products)
    #             avg_price = sum(p.price for p in products) / len(products)
    #             
    #             stats[category] = {
    #                 'total_value': total_value,
    #                 'total_items': total_items,
    #                 'avg_price': avg_price,
    #                 'product_count': len(products)
    #             }
    #         
    #         return stats
    #     
    #     def print_inventory(self):
    #         """Вывести весь инвентарь"""
    #         if not self.products:
    #             print("Инвентарь пуст!")
    #             return
    #         
    #         print("\nИнвентарь:")
    #         print("-" * 80)
    #         print(f"{'ID':<5} {'Название':<20} {'Категория':<15} {'Цена':<10} {'Количество':<10} {'Стоимость':<10}")
    #         print("-" * 80)
    #         
    #         for product in sorted(self.products.values(), key=lambda p: p.category):
    #             total_value = product.price * product.quantity
    #             print(f"{product.id:<5} {product.name:<20} {product.category:<15} "
    #                   f"{product.price:<10.2f} {product.quantity:<10} {total_value:<10.2f}")
    # 
    # # Демонстрация
    # inventory = Inventory()
    # 
    # # Добавляем товары
    # inventory.add_product(1, "iPhone 13", "Электроника", 80000, 5)
    # inventory.add_product(2, "MacBook Pro", "Электроника", 200000, 3)
    # inventory.add_product(3, "Кофе", "Напитки", 500, 50)
    # inventory.add_product(4, "Хлеб", "Еда", 30, 100)
    # inventory.add_product(5, "Молоко", "Напитки", 80, 25)
    # 
    # inventory.print_inventory()
    # 
    # # Продаем товары
    # inventory.sell_product(1, 2)
    # inventory.sell_product(3, 10)
    # 
    # # Проверяем товары с низкими запасами
    # low_stock = inventory.get_low_stock_products(threshold=20)
    # print(f"\nТовары с низкими запасами:")
    # for product in low_stock:
    #     print(f"  {product.name}: {product.quantity} шт.")
    # 
    # # Статистика по категориям
    # stats = inventory.get_category_stats()
    # print(f"\nСтатистика по категориям:")
    # for category, stat in stats.items():
    #     print(f"{category}: {stat['total_value']:.2f} руб. ({stat['total_items']} товаров)")
    # 
    # print(f"\nОбщая стоимость инвентаря: {inventory.get_total_value():.2f} руб.")


def exercise_05():
    """
    Упражнение 5: Граф социальной сети
    
    Создайте простую модель социальной сети:
    1. Используйте словарь словарей для представления графа
    2. Добавляйте пользователей и связи между ними
    3. Найдите общих друзей между пользователями
    4. Вычислите степень разделения (друзья друзей)
    5. Найдите самых популярных пользователей
    """
    print("=== Упражнение 5: Граф социальной сети ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # class SocialNetwork:
    #     def __init__(self):
    #         # Граф как словарь множеств: {user: {friends}}
    #         self.graph = defaultdict(set)
    #         self.users = {}  # Дополнительная информация о пользователях
    #     
    #     def add_user(self, user_id, name, age=None):
    #         """Добавить пользователя"""
    #         self.users[user_id] = {'name': name, 'age': age}
    #         if user_id not in self.graph:
    #             self.graph[user_id] = set()
    #         print(f"Добавлен пользователь: {name}")
    #     
    #     def add_friendship(self, user1, user2):
    #         """Добавить дружбу (двусторонняя связь)"""
    #         if user1 in self.users and user2 in self.users:
    #             self.graph[user1].add(user2)
    #             self.graph[user2].add(user1)
    #             name1 = self.users[user1]['name']
    #             name2 = self.users[user2]['name']
    #             print(f"{name1} и {name2} теперь друзья!")
    #         else:
    #             print("Один или оба пользователя не найдены!")
    #     
    #     def get_friends(self, user_id):
    #         """Получить список друзей"""
    #         return self.graph.get(user_id, set())
    #     
    #     def get_common_friends(self, user1, user2):
    #         """Найти общих друзей"""
    #         friends1 = self.graph.get(user1, set())
    #         friends2 = self.graph.get(user2, set())
    #         return friends1 & friends2
    #     
    #     def get_friends_of_friends(self, user_id, degree=2):
    #         """Получить друзей друзей (n-я степень разделения)"""
    #         visited = set()
    #         current_level = {user_id}
    #         visited.add(user_id)
    #         
    #         for _ in range(degree):
    #             next_level = set()
    #             for user in current_level:
    #                 for friend in self.graph.get(user, set()):
    #                     if friend not in visited:
    #                         next_level.add(friend)
    #                         visited.add(friend)
    #             current_level = next_level
    #             if not current_level:
    #                 break
    #         
    #         return current_level
    #     
    #     def find_path(self, start, end):
    #         """Найти кратчайший путь между пользователями (BFS)"""
    #         if start == end:
    #             return [start]
    #         
    #         queue = [(start, [start])]
    #         visited = {start}
    #         
    #         while queue:
    #             current, path = queue.pop(0)
    #             
    #             for friend in self.graph.get(current, set()):
    #                 if friend == end:
    #                     return path + [friend]
    #                 
    #                 if friend not in visited:
    #                     visited.add(friend)
    #                     queue.append((friend, path + [friend]))
    #         
    #         return None  # Путь не найден
    #     
    #     def get_popularity_stats(self):
    #         """Статистика популярности пользователей"""
    #         popularity = {}
    #         for user_id in self.users:
    #             popularity[user_id] = len(self.graph.get(user_id, set()))
    #         
    #         # Сортируем по популярности
    #         sorted_users = sorted(popularity.items(), key=lambda x: x[1], reverse=True)
    #         
    #         return [
    #             (user_id, self.users[user_id]['name'], friend_count)
    #             for user_id, friend_count in sorted_users
    #         ]
    #     
    #     def suggest_friends(self, user_id, max_suggestions=5):
    #         """Предложить друзей (друзья друзей, которые не являются друзьями)"""
    #         if user_id not in self.users:
    #             return []
    #         
    #         user_friends = self.graph.get(user_id, set())
    #         suggestions = defaultdict(int)
    #         
    #         # Считаем общих друзей с каждым кандидатом
    #         for friend in user_friends:
    #             for friend_of_friend in self.graph.get(friend, set()):
    #                 if (friend_of_friend != user_id and 
    #                     friend_of_friend not in user_friends):
    #                     suggestions[friend_of_friend] += 1
    #         
    #         # Сортируем по количеству общих друзей
    #         sorted_suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
    #         
    #         return [
    #             (user_id, self.users[user_id]['name'], common_count)
    #             for user_id, common_count in sorted_suggestions[:max_suggestions]
    #         ]
    #     
    #     def print_network_stats(self):
    #         """Вывести статистику сети"""
    #         total_users = len(self.users)
    #         total_connections = sum(len(friends) for friends in self.graph.values()) // 2
    #         avg_friends = total_connections * 2 / total_users if total_users > 0 else 0
    #         
    #         print(f"\nСтатистика социальной сети:")
    #         print(f"Пользователей: {total_users}")
    #         print(f"Дружеских связей: {total_connections}")
    #         print(f"Среднее количество друзей: {avg_friends:.1f}")
    #         
    #         # Топ популярных пользователей
    #         popular_users = self.get_popularity_stats()[:3]
    #         print(f"\nСамые популярные пользователи:")
    #         for user_id, name, friend_count in popular_users:
    #             print(f"  {name}: {friend_count} друзей")
    # 
    # # Демонстрация
    # network = SocialNetwork()
    # 
    # # Добавляем пользователей
    # users_data = [
    #     (1, "Алиса", 25), (2, "Боб", 30), (3, "Чарли", 28),
    #     (4, "Диана", 22), (5, "Ева", 26), (6, "Фрэнк", 32)
    # ]
    # 
    # for user_id, name, age in users_data:
    #     network.add_user(user_id, name, age)
    # 
    # # Создаем дружеские связи
    # friendships = [
    #     (1, 2), (1, 3), (2, 3), (2, 4),
    #     (3, 5), (4, 5), (4, 6), (5, 6)
    # ]
    # 
    # for user1, user2 in friendships:
    #     network.add_friendship(user1, user2)
    # 
    # network.print_network_stats()
    # 
    # # Найдем общих друзей
    # common = network.get_common_friends(1, 4)
    # common_names = [network.users[uid]['name'] for uid in common]
    # print(f"\nОбщие друзья Алисы и Дианы: {common_names}")
    # 
    # # Найдем путь между пользователями
    # path = network.find_path(1, 6)
    # if path:
    #     path_names = [network.users[uid]['name'] for uid in path]
    #     print(f"Путь от Алисы до Фрэнка: {' -> '.join(path_names)}")
    # 
    # # Предложения друзей
    # suggestions = network.suggest_friends(1)
    # print(f"\nПредложения друзей для Алисы:")
    # for user_id, name, common_count in suggestions:
    #     print(f"  {name} ({common_count} общих друзей)")


def exercise_06():
    """
    Упражнение 6: Оптимизация структур данных
    
    Сравните производительность разных подходов:
    1. Поиск элементов в разных структурах
    2. Группировка данных разными способами
    3. Подсчет уникальных элементов
    4. Кеширование результатов вычислений
    5. Выбор оптимальной структуры для задачи
    """
    print("=== Упражнение 6: Оптимизация структур данных ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # import time
    # import random
    # 
    # def benchmark_search(data_size=10000):
    #     """Сравнить производительность поиска"""
    #     print(f"\nБенчмарк поиска ({data_size} элементов):")
    #     
    #     # Подготовка данных
    #     data = list(range(data_size))
    #     search_items = random.sample(data, 100)  # 100 случайных элементов для поиска
    #     
    #     # Структуры данных
    #     test_list = data.copy()
    #     test_set = set(data)
    #     test_dict = {i: f"value_{i}" for i in data}
    #     
    #     # Тест поиска в списке
    #     start_time = time.perf_counter()
    #     for item in search_items:
    #         _ = item in test_list
    #     list_time = time.perf_counter() - start_time
    #     
    #     # Тест поиска в множестве
    #     start_time = time.perf_counter()
    #     for item in search_items:
    #         _ = item in test_set
    #     set_time = time.perf_counter() - start_time
    #     
    #     # Тест поиска в словаре
    #     start_time = time.perf_counter()
    #     for item in search_items:
    #         _ = item in test_dict
    #     dict_time = time.perf_counter() - start_time
    #     
    #     print(f"Список: {list_time:.6f} сек")
    #     print(f"Множество: {set_time:.6f} сек (быстрее в {list_time/set_time:.1f}x)")
    #     print(f"Словарь: {dict_time:.6f} сек (быстрее в {list_time/dict_time:.1f}x)")
    # 
    # def benchmark_grouping():
    #     """Сравнить способы группировки данных"""
    #     print(f"\nБенчмарк группировки данных:")
    #     
    #     # Генерируем данные
    #     data = [(random.randint(1, 10), f"item_{i}") for i in range(10000)]
    #     
    #     # Способ 1: Обычный словарь с проверками
    #     start_time = time.perf_counter()
    #     groups1 = {}
    #     for key, value in data:
    #         if key not in groups1:
    #             groups1[key] = []
    #         groups1[key].append(value)
    #     time1 = time.perf_counter() - start_time
    #     
    #     # Способ 2: defaultdict
    #     start_time = time.perf_counter()
    #     groups2 = defaultdict(list)
    #     for key, value in data:
    #         groups2[key].append(value)
    #     time2 = time.perf_counter() - start_time
    #     
    #     # Способ 3: setdefault
    #     start_time = time.perf_counter()
    #     groups3 = {}
    #     for key, value in data:
    #         groups3.setdefault(key, []).append(value)
    #     time3 = time.perf_counter() - start_time
    #     
    #     print(f"Обычный словарь: {time1:.6f} сек")
    #     print(f"defaultdict: {time2:.6f} сек (быстрее в {time1/time2:.1f}x)")
    #     print(f"setdefault: {time3:.6f} сек")
    # 
    # def benchmark_unique_counting():
    #     """Сравнить способы подсчета уникальных элементов"""
    #     print(f"\nБенчмарк подсчета уникальных элементов:")
    #     
    #     # Генерируем данные с повторениями
    #     data = [random.randint(1, 100) for _ in range(10000)]
    #     
    #     # Способ 1: Обычный словарь
    #     start_time = time.perf_counter()
    #     counts1 = {}
    #     for item in data:
    #         counts1[item] = counts1.get(item, 0) + 1
    #     time1 = time.perf_counter() - start_time
    #     
    #     # Способ 2: defaultdict
    #     start_time = time.perf_counter()
    #     counts2 = defaultdict(int)
    #     for item in data:
    #         counts2[item] += 1
    #     time2 = time.perf_counter() - start_time
    #     
    #     # Способ 3: Counter
    #     start_time = time.perf_counter()
    #     counts3 = Counter(data)
    #     time3 = time.perf_counter() - start_time
    #     
    #     print(f"Обычный словарь: {time1:.6f} сек")
    #     print(f"defaultdict: {time2:.6f} сек")
    #     print(f"Counter: {time3:.6f} сек (быстрее в {time1/time3:.1f}x)")
    # 
    # def caching_example():
    #     """Демонстрация кеширования"""
    #     print(f"\nДемонстрация кеширования:")
    #     
    #     # Имитируем дорогую функцию
    #     def expensive_calculation(n):
    #         time.sleep(0.01)  # Имитация сложных вычислений
    #         return sum(range(n))
    #     
    #     # Без кеширования
    #     start_time = time.perf_counter()
    #     results1 = []
    #     for i in [10, 20, 10, 30, 20, 10]:  # Повторяющиеся значения
    #         results1.append(expensive_calculation(i))
    #     time_no_cache = time.perf_counter() - start_time
    #     
    #     # С кешированием
    #     cache = {}
    #     def cached_calculation(n):
    #         if n not in cache:
    #             cache[n] = expensive_calculation(n)
    #         return cache[n]
    #     
    #     start_time = time.perf_counter()
    #     results2 = []
    #     for i in [10, 20, 10, 30, 20, 10]:
    #         results2.append(cached_calculation(i))
    #     time_with_cache = time.perf_counter() - start_time
    #     
    #     print(f"Без кеширования: {time_no_cache:.3f} сек")
    #     print(f"С кешированием: {time_with_cache:.3f} сек")
    #     print(f"Ускорение: {time_no_cache/time_with_cache:.1f}x")
    #     print(f"Размер кеша: {len(cache)} элементов")
    # 
    # def choose_optimal_structure():
    #     """Руководство по выбору оптимальной структуры"""
    #     print(f"\nРуководство по выбору структуры данных:")
    #     
    #     scenarios = [
    #         {
    #             "задача": "Нужен быстрый поиск элементов",
    #             "рекомендация": "set или dict",
    #             "причина": "O(1) поиск vs O(n) в списке"
    #         },
    #         {
    #             "задача": "Нужен порядок и индексация",
    #             "рекомендация": "list",
    #             "причина": "Поддерживает порядок и доступ по индексу"
    #         },
    #         {
    #             "задача": "Неизменяемые данные",
    #             "рекомендация": "tuple или frozenset",
    #             "причина": "Защита от изменений + можно использовать как ключи"
    #         },
    #         {
    #             "задача": "Связь ключ-значение",
    #             "рекомендация": "dict",
    #             "причина": "Оптимизирован для этой цели"
    #         },
    #         {
    #             "задача": "Подсчет элементов",
    #             "рекомендация": "Counter",
    #             "причина": "Специализированная структура с готовыми методами"
    #         },
    #         {
    #             "задача": "Группировка с автосозданием",
    #             "рекомендация": "defaultdict",
    #             "причина": "Автоматически создает значения по умолчанию"
    #         }
    #     ]
    #     
    #     for scenario in scenarios:
    #         print(f"\nЗадача: {scenario['задача']}")
    #         print(f"Рекомендация: {scenario['рекомендация']}")
    #         print(f"Причина: {scenario['причина']}")
    # 
    # # Запуск всех бенчмарков
    # benchmark_search(1000)
    # benchmark_search(10000)
    # benchmark_grouping()
    # benchmark_unique_counting()
    # caching_example()
    # choose_optimal_structure()


def exercise_07():
    """
    Упражнение 7: Работа с вложенными структурами
    
    Создайте систему для работы с JSON-подобными данными:
    1. Поиск значений по вложенным ключам
    2. Обновление значений в глубоко вложенных структурах
    3. Слияние двух вложенных словарей
    4. Валидация структуры данных
    5. Извлечение всех значений определенного типа
    """
    print("=== Упражнение 7: Работа с вложенными структурами ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # class NestedDataProcessor:
    #     @staticmethod
    #     def get_nested_value(data, path):
    #         """
    #         Получить значение по пути (например, 'user.profile.name')
    #         """
    #         keys = path.split('.')
    #         current = data
    #         
    #         try:
    #             for key in keys:
    #                 if isinstance(current, dict):
    #                     current = current[key]
    #                 elif isinstance(current, list):
    #                     current = current[int(key)]
    #                 else:
    #                     return None
    #             return current
    #         except (KeyError, IndexError, ValueError):
    #             return None
    #     
    #     @staticmethod
    #     def set_nested_value(data, path, value):
    #         """
    #         Установить значение по пути
    #         """
    #         keys = path.split('.')
    #         current = data
    #         
    #         # Проходим до предпоследнего ключа
    #         for key in keys[:-1]:
    #             if isinstance(current, dict):
    #                 if key not in current:
    #                     current[key] = {}
    #                 current = current[key]
    #             else:
    #                 raise ValueError(f"Невозможно установить значение по пути {path}")
    #         
    #         # Устанавливаем значение
    #         if isinstance(current, dict):
    #             current[keys[-1]] = value
    #         else:
    #             raise ValueError(f"Невозможно установить значение по пути {path}")
    #     
    #     @staticmethod
    #     def merge_dicts(dict1, dict2, deep=True):
    #         """
    #         Слияние двух словарей (с глубоким или поверхностным копированием)
    #         """
    #         if deep:
    #             result = copy.deepcopy(dict1)
    #         else:
    #             result = dict1.copy()
    #         
    #         for key, value in dict2.items():
    #             if (key in result and 
    #                 isinstance(result[key], dict) and 
    #                 isinstance(value, dict)):
    #                 result[key] = NestedDataProcessor.merge_dicts(result[key], value, deep)
    #             else:
    #                 if deep and isinstance(value, dict):
    #                     result[key] = copy.deepcopy(value)
    #                 else:
    #                     result[key] = value
    #         
    #         return result
    #     
    #     @staticmethod
    #     def find_all_values(data, target_type=None, key_name=None):
    #         """
    #         Найти все значения определенного типа или по имени ключа
    #         """
    #         results = []
    #         
    #         def _search(obj, path=""):
    #             if isinstance(obj, dict):
    #                 for key, value in obj.items():
    #                     current_path = f"{path}.{key}" if path else key
    #                     
    #                     # Проверяем по имени ключа
    #                     if key_name and key == key_name:
    #                         results.append((current_path, value))
    #                     
    #                     # Проверяем по типу значения
    #                     if target_type and isinstance(value, target_type):
    #                         results.append((current_path, value))
    #                     
    #                     # Рекурсивный поиск
    #                     _search(value, current_path)
    #             
    #             elif isinstance(obj, list):
    #                 for i, item in enumerate(obj):
    #                     current_path = f"{path}[{i}]" if path else f"[{i}]"
    #                     
    #                     if target_type and isinstance(item, target_type):
    #                         results.append((current_path, item))
    #                     
    #                     _search(item, current_path)
    #         
    #         _search(data)
    #         return results
    #     
    #     @staticmethod
    #     def validate_structure(data, schema):
    #         """
    #         Проверить соответствие данных схеме
    #         """
    #         errors = []
    #         
    #         def _validate(obj, schema_obj, path=""):
    #             if isinstance(schema_obj, dict):
    #                 if not isinstance(obj, dict):
    #                     errors.append(f"{path}: ожидался словарь, получен {type(obj).__name__}")
    #                     return
    #                 
    #                 for key, expected_type in schema_obj.items():
    #                     current_path = f"{path}.{key}" if path else key
    #                     
    #                     if key not in obj:
    #                         errors.append(f"{current_path}: отсутствует обязательный ключ")
    #                     else:
    #                         _validate(obj[key], expected_type, current_path)
    #             
    #             elif isinstance(schema_obj, list) and len(schema_obj) == 1:
    #                 # Схема для списка
    #                 if not isinstance(obj, list):
    #                     errors.append(f"{path}: ожидался список, получен {type(obj).__name__}")
    #                     return
    #                 
    #                 for i, item in enumerate(obj):
    #                     _validate(item, schema_obj[0], f"{path}[{i}]")
    #             
    #             elif isinstance(schema_obj, type):
    #                 # Проверка типа
    #                 if not isinstance(obj, schema_obj):
    #                     errors.append(f"{path}: ожидался {schema_obj.__name__}, получен {type(obj).__name__}")
    #         
    #         _validate(data, schema)
    #         return errors
    #     
    #     @staticmethod
    #     def flatten_dict(data, separator='.'):
    #         """
    #         Превратить вложенный словарь в плоский
    #         """
    #         result = {}
    #         
    #         def _flatten(obj, prefix=""):
    #             if isinstance(obj, dict):
    #                 for key, value in obj.items():
    #                     new_key = f"{prefix}{separator}{key}" if prefix else key
    #                     _flatten(value, new_key)
    #             else:
    #                 result[prefix] = obj
    #         
    #         _flatten(data)
    #         return result
    # 
    # # Демонстрация
    # processor = NestedDataProcessor()
    # 
    # # Тестовые данные
    # complex_data = {
    #     "user": {
    #         "id": 123,
    #         "profile": {
    #             "name": "Alice",
    #             "age": 30,
    #             "settings": {
    #                 "notifications": True,
    #                 "theme": "dark"
    #             }
    #         },
    #         "friends": [
    #             {"name": "Bob", "age": 25},
    #             {"name": "Charlie", "age": 35}
    #         ]
    #     },
    #     "config": {
    #         "version": "1.0",
    #         "features": ["feature1", "feature2"]
    #     }
    # }
    # 
    # # Получение вложенных значений
    # print("Получение значений по путям:")
    # print(f"user.profile.name: {processor.get_nested_value(complex_data, 'user.profile.name')}")
    # print(f"user.friends.0.name: {processor.get_nested_value(complex_data, 'user.friends.0.name')}")
    # print(f"config.version: {processor.get_nested_value(complex_data, 'config.version')}")
    # 
    # # Установка значений
    # processor.set_nested_value(complex_data, 'user.profile.email', 'alice@example.com')
    # processor.set_nested_value(complex_data, 'user.profile.settings.language', 'ru')
    # print(f"\nПосле добавления email: {processor.get_nested_value(complex_data, 'user.profile.email')}")
    # 
    # # Поиск всех строковых значений
    # string_values = processor.find_all_values(complex_data, target_type=str)
    # print(f"\nВсе строковые значения:")
    # for path, value in string_values[:5]:  # Показываем первые 5
    #     print(f"  {path}: {value}")
    # 
    # # Поиск по имени ключа
    # name_values = processor.find_all_values(complex_data, key_name="name")
    # print(f"\nВсе значения с ключом 'name':")
    # for path, value in name_values:
    #     print(f"  {path}: {value}")
    # 
    # # Схема для валидации
    # schema = {
    #     "user": {
    #         "id": int,
    #         "profile": {
    #             "name": str,
    #             "age": int
    #         }
    #     },
    #     "config": {
    #         "version": str
    #     }
    # }
    # 
    # # Валидация
    # errors = processor.validate_structure(complex_data, schema)
    # if errors:
    #     print(f"\nОшибки валидации:")
    #     for error in errors:
    #         print(f"  {error}")
    # else:
    #     print(f"\nДанные соответствуют схеме!")
    # 
    # # Сплющивание словаря
    # flat_data = processor.flatten_dict(complex_data)
    # print(f"\nСплющенный словарь (первые 5 элементов):")
    # for key, value in list(flat_data.items())[:5]:
    #     print(f"  {key}: {value}")


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Управление списком задач", exercise_01),
        ("Анализатор текста с множествами", exercise_02),
        ("Система рекомендаций фильмов", exercise_03),
        ("Инвентарь магазина с именованными кортежами", exercise_04),
        ("Граф социальной сети", exercise_05),
        ("Оптимизация структур данных", exercise_06),
        ("Работа с вложенными структурами", exercise_07),
    ]
    
    print("🏗️ Упражнения: Структуры данных Python")
    print("=" * 50)
    
    while True:
        print("\nДоступные упражнения:")
        for i, (name, _) in enumerate(exercises, 1):
            print(f"{i:2}. {name}")
        print(" 0. Выход")
        
        try:
            choice = int(input("\nВыберите упражнение (0-7): "))
            if choice == 0:
                print("До свидания!")
                break
            elif 1 <= choice <= len(exercises):
                print("\n" + "="*60)
                exercises[choice-1][1]()
                print("="*60)
                input("\nНажмите Enter для продолжения...")
            else:
                print("Неверный номер упражнения!")
        except ValueError:
            print("Введите корректный номер!")
        except KeyboardInterrupt:
            print("\n\nДо свидания!")
            break


if __name__ == "__main__":
    main() 