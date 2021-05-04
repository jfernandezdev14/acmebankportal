
from app.utilities.utils.utils import get_cop_exchange_rate
from app.wrappers.financialservice_wrapper import get_bank_account, update_bank_account_balance


class Account(object):
    def __init__(self, user_id=None, balance=None):
        self.user_id = user_id
        self.balance = balance


class AccountsController(object):
    """
    Contains the logic related to the account functionalities
    """

    @staticmethod
    def get_bank_account(user_id, workflow_log=[]):
        """
        Retrieves a bank account
        :param user_id: String, User identifier. Ie, "84572093457"
        :param workflow_log: List, contains the history of the workflow. Ie, ["Transaction 1", ...]
        :return: Dict, Bank account information. Ie, {"user_id": "4852703", ...}
        """
        bank_account = get_bank_account(user_id)
        workflow_log.append("Bank account retrieved")
        return bank_account


    @staticmethod
    def get_bank_account_balance(params, workflow_log=[]):
        """
        Retrieves a bank account to get its balance
        :param params: Dict, contains the params information. Ie, {'user_id': '105398891'}
        :param workflow_log: List, contains the history of the workflow. Ie, ["Transaction 1", ...]
        """
        bank_account = get_bank_account(params.get('user_id'))
        balance = bank_account.get('balance')
        account_user_id = bank_account.get('user_id')
        workflow_log.append("Account user id: {} with a Balance: {} ".format(account_user_id, balance))
        return balance

    @staticmethod
    def withdraw_or_deposit_money(params, workflow_log=[], transaction='DB', currency='COP'):
        """
        Applies withdrawals or deposits to a bank account balance
        :param params: Dict, contains the params information. Ie, {'user_id': '105398891'}
        :param amount: float, amount that is going to be withdraw or deposit. Ie, 200.0
        :param workflow_log: List, contains the history of the workflow. Ie, ["Transaction 1", ...]
        :param currency: string, Currency of the transaction to apply. Ie, "COP"
        :param transaction: string, type of transaction to apply. Ie, "DB"
        """
        user_id = params.get('user_id')
        amount = params.get('money')
        bank_account = get_bank_account(user_id)
        balance = float(bank_account.get('balance'))
        cop_amount = amount
        workflow_log_message = 'Withdrawal of {} COP'.format(cop_amount)
        if currency == 'USD':
            usd_trm = get_cop_exchange_rate()
            cop_amount = float(amount) * usd_trm
            workflow_log_message = "Withdrawal of {} {} with a TRM of {} that represents {} COP".\
                format(float(amount), currency, usd_trm, cop_amount)
        new_balance = balance - cop_amount if transaction == 'DB' else balance + cop_amount
        AccountsController.update_bank_account_balance(user_id, new_balance, workflow_log)
        workflow_log.append(workflow_log_message)

    @staticmethod
    def update_bank_account_balance(user_id, new_balance, workflow_log=[]):
        """
        Updates a bank account balance
        :param user_id: String, User identifier. Ie, "84572093457"
        :param new_balance: float, New balance of the bank account. Ie, 200.0
        :param workflow_log: List, contains the history of the workflow. Ie, ["Transaction 1", ...]
        """
        update_bank_account_balance(user_id, new_balance)
        workflow_log.append("Bank account balance updated")
