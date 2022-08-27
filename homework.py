from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    '''Информационное сообщение о тренировке.'''

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        '''Получить строку сообщения'''
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:0.3f} ч.; '
            f'Дистанция: {self.distance:0.3f} км; '
            f'Ср. скорость: {self.speed:0.3f} км/ч; '
            f'Потрачено ккал: {self.calories:0.3f}.'
        )


class Training:
    '''Базовый класс тренировки.'''

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOURS_TO_MINUTES: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        '''Получить дистанцию в км.'''
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        '''Получить среднюю скорость движения.'''
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        '''Получить количество затраченных калорий.'''
        raise NotImplementedError('Метод не определен')

    def show_training_info(self) -> InfoMessage:
        '''Получить объект информационного сообщения о тренировке.'''
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    '''Тренировка: бег.'''

    COEFF_CALORIES_1: int = 18
    COEFF_CALORIES_2: int = 20

    def get_spent_calories(self) -> float:
        '''Получить количество затраченных калорий.'''
        mean_speed = self.get_mean_speed()

        return (
            (self.COEFF_CALORIES_1 * mean_speed - self.COEFF_CALORIES_2)
            * self.weight / self.M_IN_KM
            * self.duration * self.HOURS_TO_MINUTES
        )


class SportsWalking(Training):
    '''Тренировка: спортивная ходьба.'''

    COEFF_CALORIES_1: float = 0.035
    COEFF_CALORIES_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        '''Получить количество затраченных калорий.'''
        mean_speed = self.get_mean_speed()

        return (
            (
                self.COEFF_CALORIES_1 * self.weight
                + (mean_speed ** 2 // self.height)
                * self.COEFF_CALORIES_2 * self.weight
            )
            * self.duration * self.HOURS_TO_MINUTES
        )


class Swimming(Training):
    '''Тренировка: плавание.'''

    LEN_STEP: float = 1.38
    COEFF_CALORIES_1: float = 1.1

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int
    ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        '''Получить среднюю скорость движения.'''
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        '''Получить количество затраченных калорий.'''
        mean_speed = self.get_mean_speed()
        return (mean_speed + self.COEFF_CALORIES_1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    '''Прочитать данные полученные от датчиков.'''
    traning_class: Dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    if workout_type not in traning_class:
        raise ValueError(f'Неизвестный вид тренировки {workout_type}')

    return traning_class[workout_type](*data)


def main(training: Training) -> None:
    '''Главная функция.'''
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        print(training)
        main(training)
