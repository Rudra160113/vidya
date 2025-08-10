# File location: vidya/tests/testing_dependency_injector.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.core.dependency_injector import DependencyInjector

class ServiceA:
    pass

class ServiceB:
    def __init__(self, service_a: ServiceA):
        self.service_a = service_a

class TestingDependencyInjector:
    """
    A suite of tests to verify the functionality of the DependencyInjector.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.injector = DependencyInjector()
        logging.info("TestingDependencyInjector initialized.")
    
    def test_register_and_get_instance(self) -> bool:
        """Tests if a service can be registered and retrieved."""
        self.injector.register('service_a_key', ServiceA)
        instance = self.injector.get('service_a_key')
        
        return isinstance(instance, ServiceA)

    def test_singleton_behavior(self) -> bool:
        """Tests if the injector returns the same instance for a singleton."""
        self.injector.register('service_a_key', ServiceA)
        instance1 = self.injector.get('service_a_key')
        instance2 = self.injector.get('service_a_key')
        
        return instance1 is instance2

    def test_dependency_injection(self) -> bool:
        """Tests if a service with dependencies can be instantiated correctly."""
        self.injector.register(ServiceA, ServiceA)
        self.injector.register(ServiceB, ServiceB)
        
        instance_b = self.injector.get(ServiceB)
        
        return isinstance(instance_b, ServiceB) and isinstance(instance_b.service_a, ServiceA)

    def test_get_unregistered_service(self) -> bool:
        """Tests if requesting an unregistered service raises an error."""
        try:
            self.injector.get('unregistered_service')
            return False # Should have raised an error
        except KeyError:
            return True

    def run_all_tests(self):
        """Runs all dependency injector tests."""
        self.test_runner.run_test("Register and Get Instance Test", self.test_register_and_get_instance)
        self.test_runner.run_test("Singleton Behavior Test", self.test_singleton_behavior)
        self.test_runner.run_test("Dependency Injection Test", self.test_dependency_injection)
        self.test_runner.run_test("Get Unregistered Service Test", self.test_get_unregistered_service)
        self.test_runner.print_summary()
