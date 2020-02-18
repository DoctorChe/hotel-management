import datetime
from decimal import Decimal


class Field(property):
    """
    Класс Field наследуется от property, т.е. класс будет являтся свойством
    Он становится дескриптором
    """
    def __init__(self):
        # В __init__ передаются функции для задания значения и получения
        super().__init__(self.get_value, self.set_value)
        self.name = None
        self.storage_name = None
        self.model_cls = None

    def bind_name(self, name):
        # Имя
        self.name = name
        # Имя для хранения данных
        self.storage_name = ''.join(('_', self.name))
        return self

    def bind_model_cls(self, model_cls):
        self.model_cls = model_cls
        return self

    def init_model(self, model, value):
        self.set_value(model, value)

    def get_value(self, model):
        # получаем значение из объекта модели
        return getattr(model, self.storage_name)

    def set_value(self, model, value):
        # Объекту модели свойству storage_name задаем преобразованное значение
        setattr(model, self.storage_name, self.__converter(value))

    def get_builtin_type(self, model):
        return self.get_value(model)

    def __converter(self, value):
        """
        Функция будет определена в наследниках для преобразования типа
        :param value:
        :return:
        """
        return value

    @staticmethod
    def _get_model_instance(model_cls, data):
        # возвращаем экземпляр класса если данные заданы словарем иначе возвращаем data
        return model_cls(**data) if isinstance(data, dict) else data


class Bool(Field):
    """
    Определяем как мы будем преобразовывать значение
    """
    def __converter(self, value):
        # Приводим к логическому типу
        return bool(value)


class Int(Field):
    def __converter(self, value):
        return int(value)


class Float(Field):
    def __converter(self, value):
        return float(value)


class DecimalField(Field):
    def __converter(self, value):
        return Decimal(value)


class String(Field):
    def __converter(self, value):
        return str(value)


class Date(Field):
    def __converter(self, value):
        if not isinstance(value, datetime.date):
            raise TypeError(f'{value} is not valid date')
        return value


class Model(Field):
    """
    Модель является полем, а зачит и дескриптором
    Создаем для того чтобы определить связанное поле аналог OneToOneField в django
    """
    def __init__(self, related_model_cls):
        super().__init__()
        # дополнительно храним класс связанного поля
        self.related_model_cls = related_model_cls

    def __converter(self, value):
        # Возвращает экземпляр связанного класса
        return self._get_model_instance(self.related_model_cls, value)

    def get_builtin_type(self, model):
        # У значения дополнительно вызываем метод get_data
        return self.get_value(model).get_data()


class FieldCollection(Field):
    """
    Аналог ForeignKey в django
    """
    def __init__(self, related_model_cls):
        super().__init__()
        # Запоминаем класс связанного поля
        self.related_model_cls = related_model_cls

    def get_builtin_type(self, model):
        # Возвращаем список данных из связанных полей
        return [item.get_data() if isinstance(item, self.related_model_cls)
                else item for item in self.get_value(model)]


class DomainModelMetaClass(type):
    """
    Метакласс для создания доменной модели
    """
    def __new__(cls, class_name, bases, attributes):
        """Class Factory"""
        # Создаем наши поля и задаем им имена
        # attributes - это свойства класса
        model_fields = cls.parse_fields(attributes)

        # Если установлено магическое свойство __slots_optimization__
        if attributes.get('__slots_optimization__', True):
            # То мы классу прописываем слоты и в них имена наших полей
            # Для ускорения работы
            # Т.е. динамически формируем слоты
            attributes['__slots__'] = cls.prepare_model_slots(model_fields)

        # создаем итоговый класс
        new_cls = type.__new__(cls, class_name, bases, attributes)

        # Для каждого поля сохраняем класс в котором он прописан как свойство
        new_cls.__fields__ = cls.bind_fields_to_model_cls(cls, model_fields)

        # Задаем уникальное поле (id например)
        new_cls.__unique_key__ = cls.prepare_fields_attribute(
            attribute_name='__unique_key__', attributes=attributes,
            class_name=class_name)

        # Задаем поля которые будут выводиться на печать
        new_cls.__view_key__ = cls.prepare_fields_attribute(
            attribute_name='__view_key__', attributes=attributes,
            class_name=class_name)

        return new_cls

    @staticmethod
    def parse_fields(attributes):
        # Создаем кортеж из наших полей
        # Используем метод bind_name
        return tuple(field.bind_name(name)
                     for name, field in attributes.items()
                     if isinstance(field, Field))

    @staticmethod
    def prepare_model_slots(model_fields):
        return tuple(field.storage_name for field in model_fields)

    @staticmethod
    def prepare_fields_attribute(attribute_name, attributes, class_name):
        attribute = attributes.get(attribute_name)
        if attribute:
            return tuple(attribute)
        else:
            return tuple()

    @staticmethod
    def bind_fields_to_model_cls(new_cls, model_fields):
        # Каждому полю field выставляем модель в которой он прописан
        return dict((field.name, field.bind_model_cls(new_cls)) for field in model_fields)


class DomainModel(metaclass=DomainModelMetaClass):
    # Эта наша доменная модель от неё будут наследоваться все остальные классы
    # Мы используем метакласс, а это значит что в этой модели свойствами наши поля - дескрипторы
    __fields__ = dict()
    __view_key__ = tuple()
    __unique_key__ = tuple()
    # По умолчанию слот - оптимизация включена
    __slots_optimization__ = True

    def __init__(self, **kwargs):
        """После того как сработает метаклсс
           в __fields__ будут наши поля - дескрипторы
           и мы задаем им значения
           значения приходят из kwargs
        """
        for name, field in self.__class__.__fields__.items():
            field.init_model(self, kwargs.get(name))

    def __eq__(self, other):
        """
        Метод по умолчанию для сравнения 2-х DomainModel
        :param other:
        :return:
        """
        # 1. Если это один и тот же объект Истина
        if self is other:
            return True
        # 2. Если это объекты разных классов Ложь
        if not isinstance(other, self.__class__):
            return False
        # 3. Если у них нет уникальных ключей
        if not self.__class__.__unique_key__:
            # Мы не можем сравнить
            return NotImplemented
        # 4. Сравниваем по значению всех полей (как в паттерне ValueObject)
        for field in self.__class__.__unique_key__:
            if field.get_value(self) != field.get_value(other):
                return False
        return True

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __str__(self):
        # Выводим те поля которые хранятся во __view_key__
        if not self.__class__.__view_key__:
            return self.__repr__()

        fields_values = ', '.join(
            '='.join((field.name, str(field.get_value(self)))) for field in self.__class__.__view_key__)
        return f'{self.__class__.__name__}({fields_values})'

    def get(self, field_name):
        # Получение поля по имени
        try:
            field = self.__class__.__fields__[field_name]
        except KeyError:
            raise AttributeError(f"Field {field_name} does not exist.")
        else:
            return field.get_value(self)

    def get_data(self):
        # возвращаем данные всех полей
        return dict((name, field.get_builtin_type(self))
                    for name, field in
                    self.__class__.__fields__.items())

    def set_data(self, data):
        # задаем данные полей
        for name, field in self.__class__.__fields__.items():
            field.init_model(self, data.get(name))
