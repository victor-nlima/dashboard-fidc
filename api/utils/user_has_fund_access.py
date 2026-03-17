from common.models import FundAccess

def user_has_fund_access(user, fund):
    if user.is_superuser:
        return True
    user_groups = user.groups.all()
    return FundAccess.objects.filter(fund=fund, group__in=user_groups).exists()
