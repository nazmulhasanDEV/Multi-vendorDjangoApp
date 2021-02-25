from django.apps import AppConfig


class SellerAdminConfig(AppConfig):
    name = 'seller_admin'

    def ready(self):
        import seller_admin.signals
