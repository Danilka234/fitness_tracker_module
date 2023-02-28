from typing import List


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # one step (m)
    M_IN_KM: int = 1000
    HOUR_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""

    COEFF_RUN_1: float = 18    # Коэф. для формулы(не менять)
    COEFF_RUN_2: float = 1.79  # Коэф. для формулы(не менять)
    HOUR_IN_MIN = 60           # Перевод час. в мин.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_colories_running = ((self.COEFF_RUN_1 * super().get_mean_speed()
                                  + self.COEFF_RUN_2) * self.weight
                                  / self.M_IN_KM * self.duration
                                  * self.HOUR_IN_MIN)
        return spent_colories_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WALK_1: float = 0.035
    COEFF_WALK_2: float = 0.029
    M_IN_SEC: float = 0.278    # перевод ед. измерения в м/с
    HOUR_IN_MIN: int = 60    # перевод час. в мин.
    HEIGHT_IN_M: int = 100   # перевод роста см. в м.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        spent_colories_walking = (
            (self.COEFF_WALK_1 * self.weight
             + ((super().get_mean_speed() * self.M_IN_SEC)**2
                / (self.height / self.HEIGHT_IN_M))
                * self.COEFF_WALK_2 * self.weight)
            * self.duration * self.HOUR_IN_MIN)
        return spent_colories_walking


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38      # One step (m).
    M_IN_KM: int = 1000         # Перевод час. в мин.
    COEFF_SWIM_1: float = 1.1   #
    COEFF_SWIM_2: float = 2     #
    HOUR_IN_MIN: int = 60       #

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        # Длина бассейна в метрах
        self.length_pool = length_pool
        # Сколько раз тренеруемый переплыл бассейн.
        self.count_pool = count_pool

        # Расчет скорости плавца.
    def get_mean_speed(self):
        mean_speed_swim = (self.length_pool * self.count_pool
                           / self.M_IN_KM / self.duration)
        return mean_speed_swim

    def get_spent_calories(self) -> float:
        spent_colories_swim = (
            (self.get_mean_speed() + self.COEFF_SWIM_1)
            * self.COEFF_SWIM_2 * self.weight
            * self.duration)
        return spent_colories_swim


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    data_a_training = {'SWM': Swimming,
                       'RUN': Running,
                       'WLK': SportsWalking}
    return data_a_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
