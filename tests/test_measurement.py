import pytest
from ..measurement import Measurement


@pytest.fixture
def empty_sensor_instance():
    return Measurement()


def test_produces_class(empty_sensor_instance):
    assert isinstance(empty_sensor_instance, Measurement)
    assert len(empty_sensor_instance.measurement_functions) == 0
    assert empty_sensor_instance.pins.__len__() == 0


def tf_0():
    pass


@pytest.fixture
def populated_sensor_instance():
    sensor = Measurement()
    sensor.register_function('test', tf_0, [1, 2, 3])
    return sensor


def test_register_function(populated_sensor_instance):
    assert isinstance(populated_sensor_instance, Measurement)
    assert list(populated_sensor_instance.measurement_functions) == ['test']
    assert callable(populated_sensor_instance.measurement_functions['test'])
    assert populated_sensor_instance.measurement_functions.__len__() == 1
    assert populated_sensor_instance.pins.__len__() == 3


def test_register_function_fails_on_non_callable(empty_sensor_instance):
    pytest.raises(
        ValueError,
        empty_sensor_instance.register_function, 'test', 1, [1, 2, 3]
        )


def test_register_function_fails_on_pins(populated_sensor_instance):
    pytest.raises(ValueError, populated_sensor_instance.register_function,
                  'test_repeat_pins',
                  tf_0,
                  [1, 2, 3])


def tf_1():
    return "pizza!"


def test_register_function_second_function(populated_sensor_instance):
    populated_sensor_instance.register_function('test2', tf_1, [4, 5, 6])
    

def tf_2(x, y):
    return x + y


def test_register_function_fails_on_arguments(empty_sensor_instance):
    pytest.raises(ValueError,
                  empty_sensor_instance.register_function,
                  'test',
                  tf_2,
                  [1, 2, 3]
                  )

