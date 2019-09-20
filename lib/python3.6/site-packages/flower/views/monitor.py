from __future__ import absolute_import

from collections import defaultdict

from celery import states
from flower.utils import login_required_admin
from django.utils.decorators import method_decorator

from ..views import BaseHandler
from ..utils.broker import Broker
from ..api.control import ControlHandler


class Monitor(BaseHandler):

    @method_decorator(login_required_admin)
    def get(self, request):
        return self.render("flower/monitor.html")


class SucceededTaskMonitor(BaseHandler):

    @method_decorator(login_required_admin)
    def get(self, request):
        timestamp = self.get_argument('lastquery', type=float)

        state = self.settings.state

        data = defaultdict(int)
        for task_key in state.tasks.keys():
            task = state.tasks[task_key]
            if timestamp < task.timestamp and task.state == states.SUCCESS:
                data[task.worker.hostname] += 1
        for worker_key in state.workers.keys():
            if worker_key not in data:
                data[worker_key] = 0

        return self.write(data)


class TimeToCompletionMonitor(BaseHandler):

    @method_decorator(login_required_admin)
    def get(self, request):
        timestamp = self.get_argument('lastquery', type=float)
        state = self.settings.state

        execute_time = 0
        queue_time = 0
        num_tasks = 0
        for task_key in state.tasks.keys():
            task = state.tasks[task_key]
            if timestamp < task.timestamp and task.state == states.SUCCESS:
                # eta can make "time in queue" look really scary.
                if task.eta is not None:
                    continue

                if task.started is None or task.received is None or\
                        task.succeeded is None:
                    continue

                queue_time += task.started - task.received
                execute_time += task.succeeded - task.started
                num_tasks += 1

        avg_queue_time = (queue_time / num_tasks) if num_tasks > 0 else 0
        avg_execution_time = (execute_time / num_tasks) if num_tasks > 0 else 0

        result = {
            "Time in a queue": avg_queue_time,
            "Execution time": avg_execution_time,
        }
        return self.write(result)


class FailedTaskMonitor(BaseHandler):

    @method_decorator(login_required_admin)
    def get(self, request):
        timestamp = self.get_argument('lastquery', type=float)
        state = self.settings.state

        data = defaultdict(int)
        for task_key in state.tasks.keys():
            task = state.tasks[task_key]
            if timestamp < task.timestamp and task.state == states.FAILURE:
                data[task.worker.hostname] += 1
        for worker_key in state.workers.keys():
            if worker_key not in data:
                data[worker_key] = 0

        return self.write(data)


class BrokerMonitor(BaseHandler):

    @method_decorator(login_required_admin)
    def get(self, request):
        app = self.settings.app
        try:
            broker = Broker(app.connection().as_uri(include_password=True),
                            http_api=self.settings.broker_api)
        except NotImplementedError:
            return self.write({})

        queue_names = ControlHandler.get_active_queue_names()
        queues = broker.queues(queue_names)

        data = defaultdict(int)
        for queue in queues:
            data[queue['name']] = queue.get('messages', 0)

        return self.write(data)
