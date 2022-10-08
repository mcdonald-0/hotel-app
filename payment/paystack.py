import requests

from django.conf import settings


class PayStack:
    secret_key = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co/'

    def initialize_payment(self, email, amount, subaccount):
        path = f'transaction/initialize'

        data = {
            'email': email,
            'amount': amount,
            'subaccount': subaccount,
        }

        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }

        url = self.base_url + path
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['message'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message'], response_data['data']

    def verify_payment(self, ref, *args, **kwargs):
        path = f'transaction/verify/{ref}'

        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']

    def create_hotel_sub_account(self, business_name, account_number, bank_code, percentage_charge):
        path = f'subaccount/'

        data = {
            'business_name': business_name,
            'account_number': account_number,
            'bank_code': bank_code,
            'percentage_charge': percentage_charge,
        }

        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }

        url = self.base_url + path
        response = requests.post(url, headers=headers, json=data)


        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['message'], response_data['data']
        response_data = response.json()
        response_data['data'] = 'Error'
        return response_data['status'], response_data['message'], response_data['data']

