from collections import namedtuple

from app.controllers.accounts_controller import AccountsController, Account
from app.controllers.users_controller import UsersController, User
from app.utilities.utils.utils import ConditionValidator


class AcmeBankController(object):
    """
    Contains the logic related to the users functionalities
    """

    def __init__(self, json_data):
        self.json_data = json_data
        self.trigger = json_data.get('trigger')
        self.steps = json_data.get('steps')
        self.steps_dict = {}
        for step in self.steps:
            self.steps_dict[step.get("id")] = step
        self.start = None
        self.account = None
        self.action = ''
        self.validator = None
        self.workflow_log = []

    def process_json(self):
        """
        Validates if the user data received matches with an existing user
        :param user_data: Dict, Contains the user information. Ie, {"user_id": "user123", "pin": "pass123"}
        :return: Bool, Returns True if the user is a valid user, otherwise returns False
        """
        self.execute_workflow()
        return self.workflow_log

    def execute_workflow(self):
        if self.trigger:

            params = self.trigger.get('params')

            user_id = params.get("user_id")
            pin = params.get("pin")
            self.start = User(user_id, pin)

            transitions = self.trigger.get('transitions')
            target = transitions[0].get("target") if len(transitions) > 0 else None

            while target is not None:
                step = self.steps_dict.get(target)
                params.update(step.get("params"))
                target = self.execute_action(step, params)

            self.workflow_log.append('Execution process finished.')

    def retrieve_params(self, step_params):
        params = {}
        for key, step_param in step_params.items():
            from_id = step_param.get('from_id')
            param_id = step_param.get('param_id')
            if from_id:
                param_value = getattr(getattr(self, str(from_id)), str(param_id))
            else:
                param_value = step_param.get('value')
            params[key] = param_value
        return params

    def perform_transition(self, transition, step):
        if len(transition.get("condition", [])) == 0:
            target = transition.get("target")
            return target, True

        condition = transition.get("condition", [])[0]
        operator = condition.get("operator")
        field_id = condition.get("field_id")
        value = condition.get("value")
        valid = self.validator.validate(
            operator, field_id, value
        )
        self.workflow_log.append("Validation for step id {} - field: {}, operator: {}, value: {}, result: {}"
                                 .format(step.get("id"), field_id, operator, value, valid))

        if valid:
            target = transition.get("target")
            self.workflow_log.append('Executing next target: {}'.format(target))
            return target, valid

        return None, False

    def execute_action(self, step, params):
        retrieved_params = self.retrieve_params(params)
        action = step.get("action")
        targets = {
            "validate_account": self.validate_account,
            "withdraw_in_dollars": self.withdraw_in_dollars,
            "withdraw_in_pesos": self.withdraw_in_pesos,
            "deposit_money": self.deposit_money,
            "get_account_balance": self.get_account_balance
        }
        func = targets.get(action, lambda: self.workflow_log.append('Invalid target, process finished abruptly'))
        func(retrieved_params)

        if self.account:

            step_transitions = step.get("transitions", [])
            if len(step_transitions) == 0:
                return None

            transitions_counter = 0
            for transition in step_transitions:
                target, valid = self.perform_transition(transition, step)
                if len(step_transitions) == transitions_counter + 1 or valid:
                    break
                transitions_counter += 1

            return target

        self.workflow_log.append('Account not found, process finished')
        return None

    def validate_account(self, params):
        self.start.is_valid = UsersController.validate_user(params, self.workflow_log)
        if self.start.is_valid:
            bank_account = AccountsController.get_bank_account(params.get('user_id'), self.workflow_log)
            self.account = Account(bank_account.get('user_id'), bank_account.get('balance'))
            condition_obj = namedtuple('obj', ['balance', 'is_valid'])(self.account.balance, self.start.is_valid)
            self.validator = ConditionValidator(condition_obj)

    def withdraw_in_pesos(self, params):
        AccountsController.withdraw_or_deposit_money(params, self.workflow_log, transaction='DB', currency='COP')

    def withdraw_in_dollars(self, params):
        AccountsController.withdraw_or_deposit_money(params, self.workflow_log, transaction='DB', currency='USD')

    def deposit_money(self, params):
        AccountsController.withdraw_or_deposit_money(params, self.workflow_log, transaction='CR', currency='COP')

    def get_account_balance(self, params):
        AccountsController.get_bank_account_balance(params, self.workflow_log)
