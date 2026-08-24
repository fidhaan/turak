import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .storage import WalletStorage

wallet_storage = WalletStorage()


@method_decorator(csrf_exempt, name="dispatch")
class BalancesView(View):
    """GET /api/balances/ - returns both wallet balances."""

    def get(self, request):
        online, offline = wallet_storage.read_balances()
        return JsonResponse({"online": online, "offline": offline})


@method_decorator(csrf_exempt, name="dispatch")
class DeductView(View):
    """Base class for deducting from a wallet.
    Subclasses just set `wallet_type` to 'online' or 'offline'."""

    wallet_type = None

    def post(self, request):
        try:
            body = json.loads(request.body.decode("utf-8"))
            amount = float(body.get("amount"))
        except Exception:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        if amount < 0:
            return JsonResponse(
                {"error": 'Enter an amount which is "> 0".'}, status=400
            )

        online, offline = wallet_storage.read_balances()

        if self.wallet_type == "online":
            updated = online - amount
            online = updated if updated > 0 else 0.0
        else:
            updated = offline - amount
            offline = updated if updated > 0 else 0.0

        wallet_storage.write_balances(online, offline)
        return JsonResponse({"online": online, "offline": offline})


class DeductOnlineView(DeductView):
    wallet_type = "online"


class DeductOfflineView(DeductView):
    wallet_type = "offline"