from app.controllers.accounts_controller import AccountsController
from app.controllers.users_controller import UsersController


class AcmeBankController(object):
    """
    Contains the logic related to the users functionalities
    """

    def __init__(self, json_data):
        self.json_data = json_data
        self.trigger = json_data.get('trigger')
        self.steps = json_data.get('steps')
        self.trigger_id = ''
        self.user_id = ''
        self.pin = None
        self.action = ''
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
            transitions = self.trigger.get('transitions')
            for transition in transitions:
                self.action = transition.get('target')
                conditions = transition.get('conditions', [])
                if conditions:
                    self.execute_conditions(conditions)
                self.execute_target(self.action, params)

            if self.user_id:
                self.execute_steps()

    def execute_condition(self, conditions):
        pass

    def execute_steps(self):
        # for step in self.steps:
        #     if self.action == step.get('id'):
        #         transitions = step.get('transitions', [])
        #         for transition in transitions:
        #             conditions = transition.get('condition')
        #             if conditions:
        #                 self.execute_condition(conditions)
        #
        #         self.action = step.get('id')

        pass

    def execute_target(self, target, params):
        targets = {
            "validate_account": self.validate_account,
            "withdraw_in_dollars": self.withdraw_in_dollars,
            "deposit_money": self.deposit_money,
            "get_account_balance": self.get_account_balance
        }
        func = targets.get(target, lambda: "invalid target")
        func(params)

    def validate_account(self, params):

        user = UsersController.validate_user(params, self.workflow_log)
        if user:
            self.user_id = user.get('user_id', '')

    def withdraw_in_dollars(self, params):
        AccountsController.withdraw_or_deposit_money(params, self.workflow_log, transaction='DB', currency='USD')

    def deposit_money(self, params):

        AccountsController.withdraw_or_deposit_money(params, self.workflow_log, transaction='CR', currency='COP')

    def get_account_balance(self, params):

        AccountsController.get_bank_account_balance(params, self.workflow_log)

