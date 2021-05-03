from forex_python.converter import CurrencyRates

from app.wrappers.financialservice_wrapper import get_bank_account, update_bank_account_balance


class AccountsController(object):
    """
    Contains the logic related to the account functionalities
    """

    @staticmethod
    def get_bank_account_balance(user_id, workflow_log=[]):
        """
        Retrieves a bank account to get its balance
        :param user_id: String, User identifier. Ie, "84572093457"
        :param workflow_log: List, contains the history of the workflow. Ie, ["Transaction 1", ...]
        """
        bank_account = get_bank_account(user_id)
        balance = bank_account.get('balance')
        account_user_id = bank_account.get('user_id')
        workflow_log.append("Balance: {} Account user id: {}".format(balance, account_user_id))

    @staticmethod
    def withdraw_or_deposit_money(user_id, amount, workflow_log=[], transaction='DB', currency='COP'):
        """
        Applies withdrawals or deposits to a bank account balance
        :param user_id: String, User identifier. Ie, "84572093457"
        :param amount: float, amount that is going to be withdraw or deposit. Ie, 200.0
        :param workflow_log: List, contains the history of the workflow. Ie, ["Transaction 1", ...]
        :param currency: string, Currency of the transaction to apply. Ie, "COP"
        :param transaction: string, type of transaction to apply. Ie, "DB"
        """
        bank_account = get_bank_account(user_id)
        balance = float(bank_account.get('balance'))
        cop_amount = amount
        workflow_log_message = 'Withdrawal of {} COP'.format(cop_amount)
        if currency == 'USD':
            currency_rates = CurrencyRates()
            cop_rates = currency_rates.get_rates('COP')
            usd_trm = float(cop_rates.get('USD', 1))
            cop_amount = float(amount) * usd_trm
            workflow_log_message = "Withdrawal of {} {} with a TRM of {} that represents {} COP".\
                format(float(amount), currency, cop_amount)
        new_balance = balance - cop_amount if transaction == 'DB' else balance + cop_amount
        update_bank_account_balance(user_id, new_balance, workflow_log)
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
